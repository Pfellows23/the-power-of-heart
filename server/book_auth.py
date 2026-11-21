"""Sign-in gate for the private book area (book-preview*).

Runs next to Caddy inside the same container, on 127.0.0.1:9000.
  GET  /book-auth   called by Caddy's forward_auth for every book-preview* request.
                    200 if the visitor has a valid sign-in cookie, otherwise a
                    redirect to the sign-in page.
  GET  /book-login  the styled sign-in page (book-login.html, made by build.py).
  POST /book-login  checks the shared password, sets a signed cookie, and emails
                    Pamela who signed in (through FormSubmit, like the book
                    request form).

Settings (Railway variables):
  BOOK_PASS_HASH     "pbkdf2_sha256$<iterations>$<salt hex>$<hash hex>" of the
                     shared password. If missing, nobody can sign in.
  BOOK_COOKIE_SECRET random string used to sign cookies. If missing, a random one
                     is made at start-up (visitors then sign in again after a deploy).
  BOOK_NOTIFY_EMAIL  where sign-in notices go (default pamela@thepowerofheart.com).
"""
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SITE_ROOT = os.environ.get("SITE_ROOT", "/srv")
PASS_HASH = os.environ.get("BOOK_PASS_HASH", "")
SECRET = (os.environ.get("BOOK_COOKIE_SECRET") or secrets.token_hex(32)).encode()
NOTIFY = os.environ.get("BOOK_NOTIFY_EMAIL", "pamela@thepowerofheart.com")
COOKIE = "book_access"
MAX_AGE = 30 * 24 * 3600
DEFAULT_NEXT = "/book-preview.html"
EMAIL_RE = re.compile(r"^[^@\s<>]{1,64}@[^@\s<>]{1,190}\.[^@\s<>]{2,}$")


def check_password(pw):
    try:
        algo, iters, salt, want = PASS_HASH.split("$")
        if algo != "pbkdf2_sha256":
            return False
        got = hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), int(iters)).hex()
        return hmac.compare_digest(got, want)
    except Exception:
        return False


def make_token(email):
    exp = str(int(time.time()) + MAX_AGE)
    body = urllib.parse.quote(email, safe="") + "|" + exp
    sig = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    return body + "|" + sig


def token_ok(token):
    try:
        email_q, exp, sig = token.split("|")
        body = email_q + "|" + exp
        good = hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, good) and int(exp) > time.time()
    except Exception:
        return False


def safe_next(n):
    # Only send people back into the book area on this site.
    return n if re.fullmatch(r"/book-preview[\w\-./]*(#[\w\-]*)?", n or "") else DEFAULT_NEXT


def notify(email):
    data = {
        "_subject": "Book preview opened: The Hearts of Mauna Kea",
        "_template": "table",
        "_captcha": "false",
        "Visitor email": email,
        "Signed in at (UTC)": time.strftime("%Y-%m-%d %H:%M", time.gmtime()),
    }
    req = urllib.request.Request(
        "https://formsubmit.co/ajax/" + NOTIFY,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "Origin": "https://www.thepowerofheart.com",
                 "Referer": "https://www.thepowerofheart.com/book-login"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print("notify", r.status, r.read(300).decode(errors="replace"), flush=True)
    except Exception as e:
        print("notify failed:", e, flush=True)


def login_page(error="", next_url=DEFAULT_NEXT, email=""):
    try:
        with open(os.path.join(SITE_ROOT, "book-login.html"), encoding="utf-8") as f:
            page = f.read()
    except OSError:
        page = '<form method="post" action="/book-login"><!--BOOK_ERROR--><input type="hidden" name="next" value="/book-preview.html"><input name="email" type="email"><input name="password" type="password"><button>Enter</button></form>'
    msg = f'<p class="login-error" role="alert">{html.escape(error, quote=False)}</p>' if error else ""
    page = page.replace("<!--BOOK_ERROR-->", msg)
    page = page.replace('name="next" value="/book-preview.html"', f'name="next" value="{html.escape(next_url)}"')
    if email:
        page = page.replace('name="email" ', f'name="email" value="{html.escape(email)}" ', 1)
    return page.encode()


class Handler(BaseHTTPRequestHandler):
    server_version = "book-auth"

    def log_message(self, fmt, *args):
        print("book-auth:", fmt % args, flush=True)

    def _send(self, code, body=b"", headers=None):
        self.send_response(code)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _cookie(self):
        for part in (self.headers.get("Cookie") or "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == COOKIE:
                return urllib.parse.unquote(v)
        return ""

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/book-auth":
            if token_ok(self._cookie()):
                return self._send(200)
            orig = self.headers.get("X-Forwarded-Uri") or DEFAULT_NEXT
            loc = "/book-login?next=" + urllib.parse.quote(safe_next(orig.split("?")[0]), safe="")
            return self._send(303, headers={"Location": loc})
        if path in ("/book-login", "/book-login.html"):
            q = urllib.parse.parse_qs(query)
            nxt = safe_next((q.get("next") or [""])[0])
            if token_ok(self._cookie()):
                return self._send(303, headers={"Location": nxt})
            return self._send(200, login_page(next_url=nxt), {"Content-Type": "text/html; charset=utf-8"})
        return self._send(404, b"Not found", {"Content-Type": "text/plain"})

    def do_POST(self):
        path = self.path.partition("?")[0]
        if path not in ("/book-login", "/book-login.html"):
            return self._send(404, b"Not found", {"Content-Type": "text/plain"})
        length = min(int(self.headers.get("Content-Length") or 0), 10000)
        form = urllib.parse.parse_qs(self.rfile.read(length).decode(errors="replace"))
        email = (form.get("email") or [""])[0].strip()[:254]
        pw = (form.get("password") or [""])[0]
        nxt = safe_next((form.get("next") or [""])[0])
        if not EMAIL_RE.match(email):
            return self._send(400, login_page("Please enter a valid email address.", nxt, ""), {"Content-Type": "text/html; charset=utf-8"})
        if not check_password(pw):
            time.sleep(1)
            return self._send(401, login_page("That password isn't right. Please try again.", nxt, email), {"Content-Type": "text/html; charset=utf-8"})
        threading.Thread(target=notify, args=(email,), daemon=True).start()
        cookie = f"{COOKIE}={urllib.parse.quote(make_token(email), safe='')}; Max-Age={MAX_AGE}; Path=/; HttpOnly; Secure; SameSite=Lax"
        return self._send(303, headers={"Location": nxt, "Set-Cookie": cookie})


if __name__ == "__main__":
    port = int(os.environ.get("BOOK_AUTH_PORT", "9000"))
    print(f"book-auth listening on 127.0.0.1:{port}; password set: {bool(PASS_HASH)}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

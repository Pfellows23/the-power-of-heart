# Serves the static site with Caddy. Railway sets $PORT; Caddy listens on it.
# A small Python helper (server/book_auth.py) runs alongside for the book sign-in.
FROM caddy:2.8.4-alpine
RUN apk add --no-cache python3
COPY Caddyfile /etc/caddy/Caddyfile
COPY . /srv
RUN rm -f /srv/Caddyfile && mkdir -p /app && mv /srv/server/book_auth.py /srv/server/start.sh /app/ && rm -rf /srv/server && chmod +x /app/start.sh
CMD ["/app/start.sh"]

#!/bin/sh
# Start the book sign-in helper, then Caddy in the foreground.
python3 /app/book_auth.py &
exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile

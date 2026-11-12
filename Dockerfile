# Serves the static site with Caddy. Railway sets $PORT; Caddy listens on it.
FROM caddy:2.8.4-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY . /srv
RUN rm -f /srv/Caddyfile

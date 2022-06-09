
# FROM nginx:1.19.0-alpine
FROM nginx:1.21.6

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

STOPSIGNAL STGQUIT
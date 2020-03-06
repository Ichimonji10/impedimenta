FROM nginx:1.17.9

RUN rm /etc/nginx/conf.d/default.conf
COPY docs-portal.conf /etc/nginx/conf.d/
COPY collected-docs /usr/share/nginx/docs-portal/

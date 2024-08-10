FROM debian:12

RUN --mount=type=cache,target=/var/cache/apt \
    export DEBIAN_FRONTEND=noninteractive &&\
    apt update && apt dist-upgrade -y --no-install-recommends &&\
    apt install -y --no-install-recommends python3 python3-bcrypt python3-dateutil python3-psycopg2 python3-fuzzywuzzy python3-flask &&\
    apt install -y --no-install-recommends python3-flask-babel python3-flask-login python3-flaskext.wtf python3-markdown python3-numpy &&\
    apt install -y --no-install-recommends python3-pandas python3-jinja2 python3-flask-cors python3-flask-restful p7zip-full &&\
    apt install -y --no-install-recommends python3-wand python3-rdflib python3-requests python3-dicttoxml python3-flasgger &&\
    apt install -y --no-install-recommends apache2 libapache2-mod-wsgi-py3 brotli python3-coverage python3-nose exiftran &&\
    apt install -y --no-install-recommends iipimage-server libvips-tools python3-email-validator python3-svgwrite python3-shapely &&\
    apt install -y --no-install-recommends gettext npm python3-pip git postgresql-client-15 &&\
    apt install -y --no-install-recommends dos2unix locales locales-all vim w3c-sgml-lib nano python3-xmltodict &&\
    mkdir -p /var/www/openatlas /var/www/.cache /var/www/.local /var/www/.npm &&\
    chown -R www-data:www-data /var/www/.cache /var/www/.local /var/www/.npm /var/log/apache2 /var/run/apache2
RUN cp -rp /usr/lib/iipimage-server/ /var/www/iipsrv/ &&\
    mkdir /var/www/iipsrv/tests &&\
    chown -R www-data /var/www/iipsrv/ &&\
    chmod 777 -R /var/www/iipsrv/
RUN rm /etc/apache2/mods-available/iipsrv.conf
COPY /install/iipsrv.conf /etc/apache2/mods-available/iipsrv.conf
COPY --chown=www-data:www-data / /var/www/openatlas/
RUN cd /var/www/openatlas && cp install/docker/entrypoint.sh /entrypoint.sh &&\
    cp install/example_apache.conf /etc/apache2/sites-available/000-default.conf &&\
    chmod a+x /entrypoint.sh &&\
    dos2unix /entrypoint.sh &&\
    sed -i 's~^Listen.*~Listen 8080~' /etc/apache2/ports.conf &&\
    sed -i 's~^<VirtualHost \*:80>~<VirtualHost *:8080>~' /etc/apache2/sites-available/000-default.conf &&\
    sed -i 's~ServerName.*~~' /etc/apache2/sites-available/000-default.conf &&\
    sed -i 's~</VirtualHost>~ErrorLogFormat "{ \\"time\\":\\"%{%Y-%m-%d}tT%{%T}t.%{msec_frac}tZ\\", \\"function\\" : \\"[%-m:%l]\\" , \\"process\\" : \\"[pid %P:tid %T]\\" , \\"message\\" : \\"%M\\" ,\ \\"referer\\"\ : \\"%{Referer}i\\" },"\nLogFormat "{ \\"time\\":\\"%{%Y-%m-%d}tT%{%T}t.%{msec_frac}tZ\\", \\"process\\":\\"%D\\", \\"filename\\":\\"%f\\", \\"remoteIP\\":\\"%a\\", \\"host\\":\\"%V\\", \\"request\\":\\"%U\\", \\"query\\":\\"%q\\", \\"method\\":\\"%m\\", \\"status\\":\\"%>s\\", \\"userAgent\\":\\"%{User-agent}i\\", \\"referer\\":\\"%{Referer}i\\" }," OpenAtlasLog\nCustomLog /dev/stdout OpenAtlasLog\nErrorLog /dev/stdout\n</VirtualHost>~' /etc/apache2/sites-available/000-default.conf &&\
    sed -i 's~</VirtualHost>~<IfModule mod_brotli.c>\nAddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/xml text/css text/javascript application/javascript application/x-javascript application/json application/xml\nBrotliCompressionQuality 4\n</IfModule>\n</VirtualHost>~' /etc/apache2/sites-available/000-default.conf
RUN a2enmod iipsrv &&\
    a2enmod fcgid &&\
    a2enmod brotli
USER www-data
RUN cd /var/www/openatlas/openatlas/static &&\
    npm install \ &&\
    service apache2 restart

EXPOSE 8080
ENV APACHE_CONFDIR /etc/apache2
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/usr/sbin/apache2", "-D", "FOREGROUND" ]

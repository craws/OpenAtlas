FROM debian:11

RUN --mount=type=cache,target=/var/cache/apt \
    export DEBIAN_FRONTEND=noninteractive &&\
    apt update && apt dist-upgrade -y --no-install-recommends &&\
    apt install -y --no-install-recommends python3 python3-bcrypt python3-dateutil python3-psycopg2 python3-fuzzywuzzy python3-flask &&\
    apt install -y --no-install-recommends python3-flask-babel python3-flask-login python3-flaskext.wtf python3-markdown python3-numpy &&\
    apt install -y --no-install-recommends python3-pandas python3-jinja2 python3-flask-cors python3-flask-restful p7zip-full &&\
    apt install -y --no-install-recommends python3-wand python3-rdflib python3-requests python3-dicttoxml python3-rdflib-jsonld python3-flasgger &&\
    apt install -y --no-install-recommends apache2 libapache2-mod-wsgi-py3 python3-coverage python3-nose exiftran &&\
    apt install -y --no-install-recommends iipimage-server libvips-tools &&\
    apt install -y --no-install-recommends gettext npm python3-pip git postgresql-client-13 &&\
    apt install -y --no-install-recommends dos2unix locales locales-all &&\
    mkdir -p /var/www/openatlas /var/www/.cache /var/www/.local /var/www/.npm &&\
    chown -R www-data:www-data /var/www/.cache /var/www/.local /var/www/.npm /var/log/apache2 /var/run/apache2
RUN cp -rp /usr/lib/iipimage-server/ /var/www/iipsrv/ &&\
    chown -R www-data /var/www/iipsrv/ &&\
    chmod 777 -R /var/www/iipsrv/
RUN rm /etc/apache2/mods-available/iipsrv.conf
COPY /install/iipsrv.conf /etc/apache2/mods-available/iipsrv.conf
COPY --chown=www-data:www-data / /var/www/openatlas/
RUN cd /var/www/openatlas && cp install/entrypoint.sh /entrypoint.sh &&\
    cp install/example_apache.conf /etc/apache2/sites-available/000-default.conf &&\
    chmod a+x /entrypoint.sh &&\
    dos2unix /entrypoint.sh &&\
    sed -i 's~^Listen.*~Listen 8080~' /etc/apache2/ports.conf &&\
    sed -i 's~^<VirtualHost \*:80>~<VirtualHost *:8080>~' /etc/apache2/sites-available/000-default.conf &&\
    sed -i 's~ServerName.*~~' /etc/apache2/sites-available/000-default.conf
USER www-data
RUN cd /var/www/openatlas &&\
    pip3 install calmjs &&\
    cd openatlas/static &&\
    pip3 install -e ./ &&\
    ~/.local/bin/calmjs npm --install openatlas
RUN a2enmod iipsrv &&\
    a2enmod fcgid &&\
    service apache2 restart

EXPOSE 8080
ENV APACHE_CONFDIR /etc/apache2
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/usr/sbin/apache2", "-D", "FOREGROUND" ]

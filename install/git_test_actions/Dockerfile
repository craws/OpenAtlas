FROM debian:11

RUN export DEBIAN_FRONTEND=noninteractive &&\
    apt update && apt dist-upgrade -y --no-install-recommends &&\
    apt install -y --no-install-recommends python3 python3-bcrypt python3-dateutil python3-psycopg2 python3-fuzzywuzzy python3-flask &&\
    apt install -y --no-install-recommends python3-flask-babel python3-flask-login python3-flaskext.wtf python3-markdown python3-numpy &&\
    apt install -y --no-install-recommends python3-pandas python3-jinja2 python3-flask-cors python3-flask-restful p7zip-full &&\
    apt install -y --no-install-recommends python3-wand python3-rdflib python3-dicttoxml python3-rdflib-jsonld python3-flasgger &&\
    apt install -y --no-install-recommends apache2 libapache2-mod-wsgi-py3 &&\
    apt install -y --no-install-recommends gettext npm python3-pip git postgresql-client-13 &&\
    apt install -y --no-install-recommends dos2unix locales locales-all python3-nose &&\
    mkdir -p /var/www/openatlas /var/www/.cache /var/www/.local /var/www/.npm &&\
    chown -R www-data:www-data /var/www/openatlas /var/www/.cache /var/www/.local /var/www/.npm /var/log/apache2 /var/run/apache2

COPY entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh &&\
    dos2unix /entrypoint.sh &&\

USER www-data
RUN cd /var/www &&\
    git clone https://github.com/craws/OpenAtlas.git openatlas &&\
    cd openatlas &&\
    pip3 install calmjs &&\
    cd openatlas/static &&\
    pip3 install -e ./ &&\
    ~/.local/bin/calmjs npm --install openatlas

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENTRYPOINT [ "/entrypoint.sh" ]
# Created by Alexander Watzinger and others. Please see README.md for licensing information
import subprocess
from flask import g

from openatlas import app
from openatlas.models.date import DateMapper


class Export:

    @staticmethod
    def export_to_csv():
        f = open(r'/tmp/sql.csv', 'w')
        g.cursor.copy_expert("COPY model.class TO STDOUT DELIMITER ',' CSV HEADER FORCE QUOTE *", f)
        return

    # COPY model.class TO '/tmp/model_class.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    # COPY model.class_inheritance TO '{path}model_class_inheritance.csv' {arguments};
    # COPY model.entity TO '{path}model_entity.csv' {arguments};
    # COPY model.link TO '{path}model_link.csv' {arguments};
    # COPY model.link_property TO '{path}model_link_property.csv' {arguments};
    # COPY model.property TO '{path}model_property.csv' {arguments};
    # COPY model.property_inheritance TO '{path}model_property_inheritance.csv' {arguments};
    # COPY gis.point TO '{path}gis_point.csv' {arguments};
    # COPY gis.polygon TO '{path}gis_polygon.csv' {arguments};

    @staticmethod
    def export_sql():
        """ Creates a pg_dump file in the export/sql folder, filename begins with current date."""
        # Todo: prevent exposing the database password to the process list
        file_path = '{path}/sql/{date}_dump.sql'.format(
            path=app.config['EXPORT_FOLDER_PATH'],
            date=DateMapper.current_date_for_filename())
        command = '''pg_dump -h {host} -d {database} -U {user} -p {port} -f {file}'''.format(
            host=app.config['DATABASE_HOST'],
            database=app.config['DATABASE_NAME'],
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            file=file_path)
        try:
            subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                             env={'PGPASSWORD': app.config['DATABASE_PASS']}).wait()
        except Exception:
            return False
        return True

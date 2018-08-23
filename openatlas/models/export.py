# Created by Alexander Watzinger and others. Please see README.md for licensing information
import subprocess
from flask import g

from openatlas import app
from openatlas.models.date import DateMapper


class Export:

    @staticmethod
    def export_csv(form):
        for name, value in form.data.items():
            if value and name != 'save':
                path = '{path}/csv/{date}_{name}.csv'.format(
                    path=app.config['EXPORT_FOLDER_PATH'],
                    date=DateMapper.current_date_for_filename(),
                    name=name)
                file = open(path, 'w')
                sql = "COPY {table} TO STDOUT DELIMITER ',' CSV HEADER FORCE QUOTE *;".format(
                    table=name.replace('_', '.',1))
                g.cursor.copy_expert(sql, file)
        return

    @staticmethod
    def export_sql():
        """ Creates a pg_dump file in the export/sql folder, filename begins with current date."""
        # Todo: prevent exposing the database password to the process list
        path = '{path}/sql/{date}_dump.sql'.format(path=app.config['EXPORT_FOLDER_PATH'],
                                                   date=DateMapper.current_date_for_filename())
        command = '''pg_dump -h {host} -d {database} -U {user} -p {port} -f {file}'''.format(
            host=app.config['DATABASE_HOST'],
            database=app.config['DATABASE_NAME'],
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            file=path)
        try:
            subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                             env={'PGPASSWORD': app.config['DATABASE_PASS']}).wait()
        except Exception:
            return False
        return True

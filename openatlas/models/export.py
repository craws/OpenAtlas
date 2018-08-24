# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os
import shutil
import subprocess
from flask import g, request
from flask_login import current_user

from openatlas import app
from openatlas.models.date import DateMapper


class Export:

    @staticmethod
    def export_csv(form):
        date_string = DateMapper.current_date_for_filename()
        if form.zip.data:
            path = '/tmp/' + date_string + '_openatlas_csv_export'
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)
        else:
            path = app.config['EXPORT_FOLDER_PATH'] + '/csv/'
        for name, value in form.data.items():
            if value and name not in ['save', 'zip']:
                file_path = path + '/{date}_{name}.csv'.format(date=date_string, name=name)
                file = open(file_path, 'w')
                sql = "COPY {table} TO STDOUT DELIMITER ',' CSV HEADER FORCE QUOTE *;".format(
                    table=name.replace('_', '.', 1))
                g.cursor.copy_expert(sql, file)
        if form.zip.data:
            info = 'CSV export from: {host}\n'. format(host=request.headers['Host'])
            info += 'Created: {date} by {user}\nOpenAtlas version: {version}'.format(
                date=date_string, user=current_user.username, version=app.config['VERSION'])
            with open(path + '/info.txt', "w") as file:
                print(info, file=file)
            zip_file = app.config['EXPORT_FOLDER_PATH'] + '/csv/' + date_string + '_csv'
            shutil.make_archive(zip_file, 'zip', path)
            shutil.rmtree(path)
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

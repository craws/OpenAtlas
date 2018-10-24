# Created by Alexander Watzinger and others. Please see README.md for licensing information
import os

import pandas.io.sql as psql
import shutil
import subprocess
from flask import g, request
from flask_login import current_user

from openatlas import app
from openatlas.models.date import DateMapper


class Export:

    @staticmethod
    def export_csv(form):
        """ Creates CSV file(s) in the export/csv folder, filename begins with current date."""
        date_string = DateMapper.current_date_for_filename()
        if form.zip.data:
            path = '/tmp/' + date_string + '_openatlas_csv_export'
            if os.path.exists(path):
                shutil.rmtree(path)  # pragma: no cover
            os.makedirs(path)
        else:
            path = app.config['EXPORT_FOLDER_PATH'] + '/csv/'
        for table in ['model_class_inheritance', 'model_entity', 'model_link',
                      'model_link_property', 'model_property_inheritance','model_property',
                      'model_class','gis_point', 'gis_polygon']:
            if getattr(form, table).data:
                fields = ['id']
                if table in ['model_entity']:
                    fields.append('name')
                    fields.append('description')
                    fields.append('class_code')
                    fields.append("COALESCE(to_char(value_timestamp, 'MM-DD-YYYY'), '') AS value_timestamp")
                    fields.append('created')
                    fields.append('modified')

                sql = "SELECT {fields} FROM {table};".format(
                    fields=','.join(fields), table=table.replace('_', '.', 1))
                data_frame = psql.read_sql(sql, g.db)
                file_path = path + '/{date}_{name}.csv'.format(date=date_string, name=table)
                data_frame.to_csv(file_path, index=False)
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
        except Exception:  # pragma: no cover
            return False
        return True

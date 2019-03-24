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
        """ Creates CSV file(s) in the export/csv folder, filename begins with current date."""
        import pandas.io.sql as psql
        import geopandas as gpd
        date_string = DateMapper.current_date_for_filename()
        path = app.config['EXPORT_FOLDER_PATH'] + '/csv/'
        if form.zip.data:
            path = '/tmp/' + date_string + '_openatlas_csv_export'
            if os.path.exists(path):
                shutil.rmtree(path)  # pragma: no cover
            os.makedirs(path)
        tables = {
            'model_class': ['id', 'name', 'code'],
            'model_class_inheritance': ['id', 'super_code', 'sub_code'],
            'model_entity': ['id', 'name', 'description', 'class_code', 'begin_from', 'begin_to',
                             'begin_comment', 'end_from', 'end_to', 'end_comment'],
            'model_link': ['id', 'property_code', 'domain_id', 'range_id', 'type_id', 'description',
                           'begin_from', 'begin_to', 'begin_comment', 'end_from', 'end_to',
                           'end_comment'],
            'model_property': ['id', 'code', 'range_class_code', 'domain_class_code', 'name',
                               'name_inverse'],
            'model_property_inheritance': ['id', 'super_code', 'sub_code'],
            'gis_point': ['id', 'entity_id', 'name', 'description', 'type'],
            'gis_linestring': ['id', 'entity_id', 'name', 'description', 'type'],
            'gis_polygon': ['id', 'entity_id', 'name', 'description', 'type']}
        for table, fields in tables.items():
            if getattr(form, table).data:
                if form.timestamps.data:
                    fields.append('created')
                    fields.append('modified')
                if table in ['gis_point'] and form.gis_format.data == 'coordinates':
                    fields.append("ST_X(geom) || ' ' || ST_Y(geom) AS coordinates")
                if table in ['gis_polygon'] and form.gis_format.data == 'coordinates':
                    fields.append("""
                        ST_X(public.ST_PointOnSurface(geom)) || ' ' ||
                        ST_Y(public.ST_PointOnSurface(geom)) AS polygon_center_point""")
                elif table in ['gis_point', 'gis_linestring', 'gis_polygon']:
                    fields.append('geom')
                sql = "SELECT {fields} FROM {table};".format(
                    fields=','.join(fields), table=table.replace('_', '.', 1))
                if table in ['gis_point', 'gis_linestring', 'gis_polygon'] \
                    and form.gis_format.data == 'wkt':
                    data_frame = gpd.read_postgis(sql, g.db)
                else:
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
        if os.name != "posix":  # pragma: no cover
            return False  # For other operating systems e.g. Windows, we would need adaptions here
        path = '{path}/sql/{date}_dump.sql'.format(path=app.config['EXPORT_FOLDER_PATH'],
                                                   date=DateMapper.current_date_for_filename())
        command = """pg_dump -h {host} -d {database} -U {user} -p {port} -f {file}""".format(
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

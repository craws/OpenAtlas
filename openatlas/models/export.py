# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g


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

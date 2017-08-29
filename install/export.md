## Export Data

Some examples to extract data from the database

### Database Structure

    pg_dump -sc --if-exists -n model -n gis -n log -n web openatlas > structure.sql

add "CREATE EXTENSION postgis;" and uncomment after installation for unittests

### Model Data

    pg_dump -a -n model openatlas > data/install/data_model.sql

### Web Schema

    pg_dump -n web openatlas > /tmp/openatlas_web.sql

### CSV Export

    COPY model.class TO '/tmp/model_class.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.class_inheritance TO '/tmp/model_class_inheritance.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.entity TO '/tmp/model_entity.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.link TO '/tmp/model_link.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.link_property TO '/tmp/model_link_property.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.property TO '/tmp/model_property.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY model.property_inheritance TO '/tmp/model_property_inheritance.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY gis.point TO '/tmp/gis_point.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;
    COPY gis.polygon TO '/tmp/gis_polygon.csv' DELIMITER ',' CSV HEADER FORCE QUOTE *;

## Export Data

Some examples to extract data from the database

### Database Structure

    pg_dump -sc --if-exists -n model -n gis -n log -n web openatlas > install/structure.sql

add "CREATE EXTENSION postgis;" and uncomment after installation for unittests

### Model Data

    pg_dump openatlas --inserts -a -t model.class -t model.class_i18n -t model.class_inheritance -t model.property -t model.property_i18n -t model.property_inheritance > data_model.sql 

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

-- Upgrade 7.2.0 to 7.3.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.3.0' WHERE name = 'database_version';

-- #1631: Join GIS tables
CREATE TABLE model.gis (
    id integer NOT NULL,
    entity_id integer NOT NULL,
    name text,
    description text,
    type text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    geom_point public.geometry(Point,4326),
    geom_polygon public.geometry(Polygon,4326),
    geom_linestring public.geometry(LineString,4326),
    CONSTRAINT check_only_one_is_not_null CHECK ((num_nonnulls(geom_point, geom_linestring, geom_polygon) = 1))
);
ALTER TABLE model.gis OWNER TO openatlas;
CREATE SEQUENCE model.gis_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE model.gis_id_seq OWNER TO openatlas;
ALTER SEQUENCE model.gis_id_seq OWNED BY model.gis.id;
ALTER TABLE ONLY model.gis ALTER COLUMN id SET DEFAULT nextval('model.gis_id_seq'::regclass);
ALTER TABLE ONLY model.gis ADD CONSTRAINT gis_pkey PRIMARY KEY (id);
ALTER TABLE ONLY model.gis ADD CONSTRAINT gis_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;

INSERT INTO model.gis(entity_id, name, description, type, created, modified, geom_point)      SELECT entity_id, name, description, type, created, modified, geom FROM gis.point;
INSERT INTO model.gis(entity_id, name, description, type, created, modified, geom_linestring) SELECT entity_id, name, description, type, created, modified, geom FROM gis.linestring;
INSERT INTO model.gis(entity_id, name, description, type, created, modified, geom_polygon)    SELECT entity_id, name, description, type, created, modified, geom FROM gis.polygon;

UPDATE model.gis SET type = lower(type); -- Clean up type names that are (wrongly) capitalized
CREATE TRIGGER update_modified BEFORE UPDATE ON model.gis FOR EACH ROW EXECUTE FUNCTION model.update_modified();
DROP SCHEMA gis CASCADE;

END;

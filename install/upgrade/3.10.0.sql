-- Upgrade 3.9.0 to 3.10.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Remove all property links to node roots because not needed anymore
DELETE FROM model.link_property WHERE property_code = 'P2' AND range_id IN (SELECT id FROM web.hierarchy);

-- Remove IP logging
ALTER TABLE web.system_log DROP COLUMN ip;

-- Add some comments to the schemas
COMMENT ON SCHEMA gis IS 'All geospatial information is stored here';
COMMENT ON SCHEMA model IS 'The main schema, storing CIDOC CRM itself and model related project data';
COMMENT ON SCHEMA web IS 'User interface and user account related information';

-- Add the import schema
CREATE SCHEMA import;
ALTER SCHEMA import OWNER TO openatlas;
COMMENT ON SCHEMA import IS 'Information about data imports';

CREATE TABLE import.project (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);
ALTER TABLE import.project OWNER TO openatlas;

CREATE TABLE import.project_entity (
    id integer NOT NULL,
    project_id integer NOT NULL,
    origin_id text NOT NULL,
    entity_id integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL
);
ALTER TABLE import.project_entity OWNER TO openatlas;

CREATE SEQUENCE import.project_entity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE import.project_entity_id_seq OWNER TO openatlas;
ALTER SEQUENCE import.project_entity_id_seq OWNED BY import.project_entity.id;

CREATE SEQUENCE import.project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE import.project_id_seq OWNER TO openatlas;

ALTER SEQUENCE import.project_id_seq OWNED BY import.project.id;
ALTER TABLE ONLY import.project ALTER COLUMN id SET DEFAULT nextval('import.project_id_seq'::regclass);
ALTER TABLE ONLY import.project_entity ALTER COLUMN id SET DEFAULT nextval('import.project_entity_id_seq'::regclass);
ALTER TABLE ONLY import.project_entity ADD CONSTRAINT project_entity_pkey PRIMARY KEY (id);
ALTER TABLE ONLY import.project_entity ADD CONSTRAINT project_entity_project_id_origin_id_key UNIQUE (project_id, origin_id);
ALTER TABLE ONLY import.project ADD CONSTRAINT project_name_key UNIQUE (name);
ALTER TABLE ONLY import.project ADD CONSTRAINT project_pkey PRIMARY KEY (id);

CREATE TRIGGER update_modified BEFORE UPDATE ON import.project FOR EACH ROW EXECUTE PROCEDURE model.update_modified();
ALTER TABLE ONLY import.project_entity ADD CONSTRAINT project_entity_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY import.project_entity ADD CONSTRAINT project_entity_project_id_fkey FOREIGN KEY (project_id) REFERENCES import.project(id) ON UPDATE CASCADE ON DELETE CASCADE;

COMMIT;

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.5.0' WHERE name = 'database_version';

-- #2129: Attributions for files
CREATE SEQUENCE model.file_info_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
ALTER TABLE model.file_info_id_seq OWNER TO openatlas;

CREATE TABLE model.file_info (
    id integer DEFAULT nextval('model.file_info_id_seq'::regclass) NOT NULL,
    entity_id integer,
    public boolean DEFAULT false,
    creator text,
    license_holder text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp,
    CONSTRAINT file_info_pkey PRIMARY KEY ("id")
);
COMMENT ON TABLE model.file_info IS 'Indicates if public sharing of corresponding file is allowed.';
ALTER TABLE model.file_info OWNER TO openatlas;

ALTER TABLE model.file_info ADD CONSTRAINT entity_id_key UNIQUE (entity_id);
ALTER TABLE model.file_info ADD CONSTRAINT file_info_entity_id_fkey
    FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TRIGGER update_modified BEFORE
UPDATE ON model.file_info
FOR EACH ROW EXECUTE FUNCTION model.update_modified();

END;

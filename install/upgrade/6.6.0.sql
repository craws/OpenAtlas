-- Upgrade 6.5.0 to 6.6.0
-- Be sure to backup the database and read the upgrade notes before executing!

BEGIN;

-- #1563: OpenAtlas model to database
ALTER TABLE model.class RENAME TO cidoc_class;
ALTER TABLE model.class_i18n RENAME TO cidoc_class_i18n;
ALTER TABLE model.class_inheritance RENAME TO  cidoc_class_inheritance;

ALTER SEQUENCE model.class_id_seq RENAME TO cidoc_class_id_seq;
ALTER SEQUENCE model.class_i18n_id_seq RENAME to cidoc_class_i18n_id_seq;
ALTER SEQUENCE model.class_inheritance_id_seq RENAME TO cidoc_class_inheritance_id_seq;

ALTER TABLE ONLY web."group" ADD CONSTRAINT group_name_key UNIQUE (name);

CREATE TABLE model.openatlas_class (
    id integer NOT NULL,
    name text NOT NULL,
    cidoc_class_code text NOT NULL,
    standard_type_id integer,
    alias_possible boolean DEFAULT false,
    write_access_group_name text,
    layout_color integer NOT NULL,
    layout_icon integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE model.openatlas_class OWNER TO openatlas;
COMMENT ON TABLE model.openatlas_class IS 'A more fine grained use of CIDOC classes';
COMMENT ON COLUMN model.openatlas_class.layout_color IS 'For e.g. network vizualistaion';
COMMENT ON COLUMN model.openatlas_class.layout_icon IS 'for Bootstrap icons';

CREATE SEQUENCE model.openatlas_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE model.openatlas_class_id_seq OWNER TO openatlas;
ALTER SEQUENCE model.openatlas_class_id_seq OWNED BY model.openatlas_class.id;

ALTER TABLE ONLY model.openatlas_class ALTER COLUMN id SET DEFAULT nextval('model.openatlas_class_id_seq'::regclass);
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_name_key UNIQUE (name);
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_pkey PRIMARY KEY (id);
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_cidoc_class_code_fkey FOREIGN KEY (cidoc_class_code) REFERENCES model.cidoc_class(code) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_standard_type_id_fkey FOREIGN KEY (standard_type_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY model.openatlas_class ADD CONSTRAINT openatlas_class_write_access_group_name_fkey FOREIGN KEY (write_access_group_name) REFERENCES web."group"(name) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TRIGGER update_modified BEFORE UPDATE ON model.openatlas_class FOR EACH ROW EXECUTE PROCEDURE model.update_modified();

END;

-- Upgrade 5.6.0 to 5.7.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- #1292: Reference systems
CREATE TABLE web.reference_system (
    name text NOT NULL,
    entity_id integer NOT NULL,
    resolver_url text,
    website_url text,
    created timestamp without time zone,
    modified timestamp without time zone DEFAULT now() NOT NULL,
    locked boolean DEFAULT false NOT NULL
);
ALTER TABLE web.reference_system OWNER TO openatlas;
COMMENT ON COLUMN web.reference_system.locked IS 'If true because integrated in system only URLs are editable';
ALTER TABLE ONLY web.reference_system ADD CONSTRAINT reference_system_name_key UNIQUE (name);
ALTER TABLE ONLY web.reference_system ADD CONSTRAINT reference_system_pkey PRIMARY KEY (entity_id);
CREATE TRIGGER update_modified BEFORE UPDATE ON web.reference_system FOR EACH ROW EXECUTE PROCEDURE model.update_modified();
ALTER TABLE ONLY web.reference_system ADD CONSTRAINT reference_system_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE web.reference_system_form (
    id integer NOT NULL,
    reference_system_id integer NOT NULL,
    form_id integer NOT NULL
);
ALTER TABLE web.reference_system_form OWNER TO openatlas;
CREATE SEQUENCE web.reference_system_form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE web.reference_system_form_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.reference_system_form_id_seq OWNED BY web.reference_system_form.id;
ALTER TABLE ONLY web.reference_system_form ALTER COLUMN id SET DEFAULT nextval('web.reference_system_form_id_seq'::regclass);
ALTER TABLE ONLY web.reference_system_form ADD CONSTRAINT reference_system_form_pkey PRIMARY KEY (id);
ALTER TABLE ONLY web.reference_system_form ADD CONSTRAINT reference_system_form_reference_system_id_form_id_key UNIQUE (reference_system_id, form_id);
ALTER TABLE ONLY web.reference_system_form ADD CONSTRAINT reference_system_form_form_id_fkey FOREIGN KEY (form_id) REFERENCES web.form(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.reference_system_form ADD CONSTRAINT reference_system_form_reference_system_id_fkey
    FOREIGN KEY (reference_system_id) REFERENCES web.reference_system(entity_id) ON UPDATE CASCADE ON DELETE CASCADE;

COMMIT;

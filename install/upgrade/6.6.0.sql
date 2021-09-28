-- Upgrade 6.5.0 to 6.6.0
-- Be sure to backup the database and read the upgrade notes before executing!

BEGIN;

-- #1563: OpenAtlas model to database

-- Renaming
ALTER TABLE model.class RENAME TO cidoc_class;
ALTER TABLE model.class_i18n RENAME TO cidoc_class_i18n;
ALTER TABLE model.class_inheritance RENAME TO  cidoc_class_inheritance;
ALTER SEQUENCE model.class_id_seq RENAME TO cidoc_class_id_seq;
ALTER SEQUENCE model.class_i18n_id_seq RENAME to cidoc_class_i18n_id_seq;
ALTER SEQUENCE model.class_inheritance_id_seq RENAME TO cidoc_class_inheritance_id_seq;
ALTER TABLE model.entity RENAME COLUMN class_code TO cidoc_class_code;
ALTER TABLE model.entity RENAME COLUMN system_class to openatlas_class_name;

-- Adding missing constraint for wewb.group table
ALTER TABLE ONLY web."group" ADD CONSTRAINT group_name_key UNIQUE (name);


-- New table model.openatlas_class
CREATE TABLE model.openatlas_class (
    id integer NOT NULL,
    name text NOT NULL,
    cidoc_class_code text NOT NULL,
    standard_type_id integer,
    alias_possible boolean DEFAULT false,
    write_access_group_name text,
    layout_color text,
    layout_icon text,
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

INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_possible, write_access_group_name, layout_color, standard_type_id) VALUES
    ('acquisition',         'E8',  false, 'contributor', '#0000FF', (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('activity',            'E7',  false, 'contributor', '#0000FF', (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('actor_appellation',   'E82', false, 'contributor', NULL,      NULL),
    ('administrative_unit', 'E53', false, 'contributor', NULL,      NULL),
    ('appellation',         'E41', false, 'contributor', NULL,      NULL),
    ('artifact',            'E22', false, 'contributor', '#EE82EE', (SELECT id FROM model.entity WHERE name = 'Artifact' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('bibliography',        'E31', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Artifact' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('edition',             'E31', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Edition' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('external_reference',  'E31', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'External reference' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('feature',             'E18', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Feature' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('file',                'E31', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'License' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('find',                'E22', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Artifact' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('group',               'E74', true,  'contributor', '#34623C', NULL),
    ('human_remains',       'E20', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Human remains' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('move',                'E9',  false, 'contributor', '#0000FF', (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('object_location',     'E53', false, 'contributor', '#00FF00', NULL),
    ('person',              'E21', true,  'contributor', '#34B522', NULL),
    ('place',               'E18', true,  'contributor', '#FF0000', (SELECT id FROM model.entity WHERE name = 'Place' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('reference_system',    'E32', false, 'manager',     NULL,      NULL),
    ('source',              'E33', false, 'contributor', '#FFA500', (SELECT id FROM model.entity WHERE name = 'Source' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('stratigraphic_unit',  'E18', false, 'contributor', NULL,      (SELECT id FROM model.entity WHERE name = 'Stratigraphic unit' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('source_translation',  'E33', false, 'contributor', NULL,      NULL),
    ('type',                'E55', false, 'editor',      NULL,      NULL);

ALTER TABLE ONLY model.entity ADD CONSTRAINT entity_openatlas_class_name_fkey FOREIGN KEY (openatlas_class_name) REFERENCES model.openatlas_class(name) ON UPDATE CASCADE ON DELETE CASCADE;

END;

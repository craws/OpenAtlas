-- Upgrade 3.17.x to 3.19.0
-- Be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Add new user group contributer
INSERT INTO web.group (name) VALUES ('contributor');

-- Remove settings for obsolete color themes
DELETE FROM web.user_settings WHERE name = 'theme';

-- Insert additional boolean field "locked" to web.hierarchy
ALTER TABLE web.hierarchy ADD COLUMN locked boolean;
COMMENT ON COLUMN web.hierarchy.locked IS 'True if these types are not editable';
ALTER TABLE web.hierarchy ALTER column locked SET DEFAULT false;
UPDATE web.hierarchy SET locked = false;
ALTER TABLE web.hierarchy ALTER column locked SET NOT NULL;

-- Types for external references e.g. GeoNames
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'External Reference Match', 'SKOS based definition of the confidence degree that concepts can be used interchangeable.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'exact match', 'High degree of confidence that the concepts can be used interchangeably.');
INSERT INTO model.entity (class_code, name, description) VALUES ('E55', 'close match', 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='External Reference Match'), (SELECT id FROM model.entity WHERE name='exact match')),
    ('P127', (SELECT id FROM model.entity WHERE name='External Reference Match'), (SELECT id FROM model.entity WHERE name='close match'));
INSERT INTO web.hierarchy (id, name, multiple, system, directional, value_type, locked) VALUES ((SELECT id FROM model.entity WHERE name='External Reference Match'), 'External Reference Match', False, True, False, False, True);

-- Add user private notes
CREATE TABLE web.user_notes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    entity_id integer NOT NULL,
    text text NOT NULL,
    created timestamp without time zone NOT NULL,
    modified timestamp without time zone
);
ALTER TABLE web.user_notes OWNER TO openatlas;

CREATE SEQUENCE web.user_notes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE web.user_notes_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.user_notes_id_seq OWNED BY web.user_notes.id;
ALTER TABLE ONLY web.user_notes ALTER COLUMN id SET DEFAULT nextval('web.user_notes_id_seq'::regclass);
ALTER TABLE ONLY web.user_notes ADD CONSTRAINT user_notes_pkey PRIMARY KEY (id);
ALTER TABLE ONLY web.user_notes ADD CONSTRAINT user_notes_user_id_entity_id_key UNIQUE (user_id, entity_id);
ALTER TABLE ONLY web.user_notes ADD CONSTRAINT user_notes_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.user_notes ADD CONSTRAINT user_notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;
CREATE TRIGGER update_modified BEFORE UPDATE ON web.user_notes FOR EACH ROW EXECUTE PROCEDURE model.update_modified();

COMMIT;

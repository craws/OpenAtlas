-- Upgrade to 3.0.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Settings
DELETE FROM web.settings WHERE name IN
    ('mail_transport_password', 'mail_transport_auth', 'mail_transport_ssl', 'mail_transport_type', 'notify_login');
UPDATE web.settings SET name = 'site_name' WHERE name = 'sitename';
UPDATE web.settings SET value = 'en' WHERE name = 'default_language';
UPDATE web.settings SET value = '' WHERE value = 'false';
INSERT INTO web.settings (name, value) VALUES ('minimum_password_length', '12');
INSERT INTO web.settings (name, value) VALUES ('debug_mode', '');

-- Web content
DROP TABLE IF EXISTS web.i18n;
DROP TABLE IF EXISTS web.language;
DROP TABLE IF EXISTS web.content;
SET search_path = web, pg_catalog;
CREATE TABLE i18n (
    id integer NOT NULL,
    name text NOT NULL,
    language text NOT NULL,
    text text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);
ALTER TABLE i18n OWNER TO openatlas;
CREATE SEQUENCE i18n_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE i18n_id_seq OWNER TO openatlas;
ALTER SEQUENCE i18n_id_seq OWNED BY i18n.id;
ALTER TABLE ONLY i18n ALTER COLUMN id SET DEFAULT nextval('i18n_id_seq'::regclass);
ALTER TABLE ONLY i18n ADD CONSTRAINT i18n_name_language_key UNIQUE (name, language);
ALTER TABLE ONLY i18n ADD CONSTRAINT i18n_pkey PRIMARY KEY (id);
CREATE TRIGGER update_modified BEFORE UPDATE ON i18n FOR EACH ROW EXECUTE PROCEDURE model.update_modified();

-- User
ALTER TABLE web."user" ALTER COLUMN "active" DROP DEFAULT;
ALTER TABLE web."user" ALTER COLUMN "active" TYPE bool USING active::bool;
ALTER TABLE web."user" ALTER COLUMN "active" SET DEFAULT FALSE;

ALTER TABLE IF EXISTS ONLY web.user_settings DROP CONSTRAINT IF EXISTS user_settings_user_id_name_value_key;
ALTER TABLE ONLY web.user_settings ADD CONSTRAINT user_settings_user_id_name_key UNIQUE (user_id, name);

-- Date delete trigger
DROP TRIGGER IF EXISTS on_delete_link_property ON model.link_property;
DROP TRIGGER IF EXISTS on_delete_link ON model.link;
DROP FUNCTION IF EXISTS model.delete_dates();
CREATE FUNCTION model.delete_dates() RETURNS trigger
LANGUAGE plpgsql
AS $$
    BEGIN
        DELETE FROM model.entity WHERE id = OLD.range_id AND class_id = (SELECT id FROM model.class WHERE code = 'E61');
        RETURN OLD;
    END;
$$;
ALTER FUNCTION model.delete_dates() OWNER TO openatlas;
CREATE TRIGGER on_delete_link AFTER DELETE ON model.link FOR EACH ROW EXECUTE PROCEDURE model.delete_dates();
CREATE TRIGGER on_delete_link_property AFTER DELETE ON model.link_property FOR EACH ROW EXECUTE PROCEDURE model.delete_dates();

-- Types
ALTER TABLE model.entity ADD COLUMN system_type text;

-- Place Types
UPDATE model.entity SET name = 'Place' WHERE id = (SELECT id FROM model.entity WHERE name = 'Site');
UPDATE web.hierarchy set name = 'Place' WHERE name = 'Site';

-- Source Type
UPDATE model.entity SET system_type = 'source content'
WHERE id IN (
    SELECT e.id FROM model.entity e
    JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'Source Content'));

UPDATE model.entity SET system_type = 'source translation'
WHERE id IN (
    SELECT e.id FROM model.entity e
    JOIN model.link l ON e.id = l.range_id AND l.property_id = (SELECT id FROM model.property WHERE code = 'P73'));

DELETE FROM model.entity WHERE id = (SELECT id FROM model.entity WHERE name = 'Source Content');
UPDATE model.entity SET name = 'Source translation' WHERE id = (SELECT id FROM model.entity WHERE name = 'Linguistic object classification');
UPDATE web.hierarchy SET name = 'Source translation' WHERE name = 'Linguistic object classification';
UPDATE model.entity SET name = 'Original text' WHERE id = (SELECT id FROM model.entity WHERE name = 'Source Original Text');
UPDATE model.entity SET name = 'Translation' WHERE id = (SELECT id FROM model.entity WHERE name = 'Source Translation');
UPDATE model.entity SET name = 'Transliteration' WHERE id = (SELECT id FROM model.entity WHERE name = 'Source Transliteration');

INSERT INTO web.form (name, extendable) VALUES ('Source translation', 0);
INSERT INTO web.hierarchy_form (hierarchy_id, form_id) VALUES
    ((SELECT id FROM web.hierarchy WHERE name LIKE 'Source translation'),(SELECT id FROM web.form WHERE name LIKE 'Source translation'));

-- Date Type
UPDATE model.entity SET system_type = 'exact date value'
WHERE id IN (
    SELECT e.id FROM model.entity e
    JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'Exact date value'));
UPDATE model.entity SET system_type = 'from date value'
WHERE id IN (
    SELECT e.id FROM model.entity e
    JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'From date value'));
UPDATE model.entity SET system_type = 'to date value'
WHERE id IN (
    SELECT e.id FROM model.entity e
    JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'To date value'));

DELETE FROM model.entity WHERE id = (SELECT id FROM model.entity WHERE name = 'To date value');
DELETE FROM model.entity WHERE id = (SELECT id FROM model.entity WHERE name = 'Exact date value');
DELETE FROM model.entity WHERE id = (SELECT id FROM model.entity WHERE name = 'From date value');
DELETE FROM model.entity WHERE id = (SELECT id FROM model.entity WHERE name = 'Date value type');

-- References
UPDATE model.entity SET system_type = 'information carrier'
WHERE id IN (SELECT e.id FROM model.entity e JOIN model.class c ON e.class_id = c.id AND c.code = 'E84');

UPDATE model.entity e SET system_type = 'edition'
WHERE id IN (
    SELECT e2.id FROM model.entity e2
    JOIN model.link l ON e2.id = l.domain_id
        AND l.property_id = (SELECT id FROM model.property WHERE code = 'P2')
        AND (l.range_id = (SELECT id FROM model.entity WHERE name = 'Edition')
            OR l.range_id IN (
            SELECT e.id FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'Edition'))));

UPDATE model.entity e SET system_type = 'bibliography'
WHERE id IN (
    SELECT e2.id FROM model.entity e2
    JOIN model.link l ON e2.id = l.domain_id
        AND l.property_id = (SELECT id FROM model.property WHERE code = 'P2')
        AND (l.range_id = (SELECT id FROM model.entity WHERE name = 'Bibliography')
            OR l.range_id IN (
            SELECT e.id FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id AND l.range_id = (SELECT id FROM model.entity WHERE name = 'Bibliography'))));

-- Location of places
UPDATE model.entity SET system_type = 'place location' WHERE name LIKE 'Location of%' AND class_id = (SELECT id FROM model.class WHERE code = 'E53');

-- Alter web.hierarchy and form with booleans and clean up
ALTER TABLE ONLY web.hierarchy ADD CONSTRAINT hierarchy_name_key UNIQUE (name);
ALTER TABLE web.hierarchy DROP COLUMN extendable;
ALTER TABLE web.hierarchy ALTER COLUMN multiple DROP DEFAULT;
ALTER TABLE web.hierarchy ALTER COLUMN multiple TYPE bool USING multiple::bool;
ALTER TABLE web.hierarchy ALTER COLUMN multiple SET DEFAULT FALSE;
ALTER TABLE web.hierarchy ALTER COLUMN system DROP DEFAULT;
ALTER TABLE web.hierarchy ALTER COLUMN system TYPE bool USING system::bool;
ALTER TABLE web.hierarchy ALTER COLUMN system SET DEFAULT FALSE;
ALTER TABLE web.hierarchy ALTER COLUMN directional DROP DEFAULT;
ALTER TABLE web.hierarchy ALTER COLUMN directional TYPE bool USING directional::bool;
ALTER TABLE web.hierarchy ALTER COLUMN directional SET DEFAULT FALSE;
ALTER TABLE web.form ALTER COLUMN extendable DROP DEFAULT;
ALTER TABLE web.form ALTER COLUMN extendable TYPE bool USING extendable::bool;
ALTER TABLE web.form ALTER COLUMN extendable SET DEFAULT FALSE;

-- Remove all links to node roots because not needed anymore
DELETE FROM model.link WHERE
    property_id = (SELECT id FROM model.property WHERE code = 'P2')
    AND range_id IN (SELECT id FROM web.hierarchy);

-- Change gender to sex and remove system flag
UPDATE model.entity SET name = 'Sex', description = 'Categories for sex like female, male.'
    WHERE id = (SELECT id from model.entity WHERE name = 'Gender');
UPDATE web.hierarchy SET name = 'Sex', system = False WHERE name = 'Gender';

-- Change foreign keys at entity/class and links/property from id to code
ALTER TABLE IF EXISTS ONLY model.entity DROP CONSTRAINT IF EXISTS entity_class_id_fkey;
ALTER TABLE model.entity ALTER COLUMN class_id TYPE text;
ALTER TABLE model.entity RENAME class_id TO class_code;
UPDATE model.entity SET class_code = (SELECT code FROM model.class WHERE id = class_code::integer);
ALTER TABLE ONLY model.entity ADD CONSTRAINT entity_class_code_fkey FOREIGN KEY (class_code) REFERENCES model.class(code) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY model.link DROP CONSTRAINT IF EXISTS link_property_id_fkey;
ALTER TABLE model.link ALTER COLUMN property_id TYPE text;
ALTER TABLE model.link RENAME property_id TO property_code;
UPDATE model.link SET property_code = (SELECT code FROM model.property WHERE id = property_code::integer);
ALTER TABLE ONLY model.link ADD CONSTRAINT link_property_code_fkey FOREIGN KEY (property_code) REFERENCES model.property(code) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY model.link_property DROP CONSTRAINT IF EXISTS link_property_property_id_fkey;
ALTER TABLE model.link_property ALTER COLUMN property_id TYPE text;
ALTER TABLE model.link_property RENAME property_id TO property_code;
UPDATE model.link_property SET property_code = (SELECT code FROM model.property WHERE id = property_code::integer);
ALTER TABLE ONLY model.link_property ADD CONSTRAINT link_property_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES model.link(id) ON UPDATE CASCADE ON DELETE CASCADE;

COMMIT;

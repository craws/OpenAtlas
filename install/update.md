## INFO

Before executing SQL statements make a backup of the database.

Replace database role "openatlas" if needed.

### 2.3.0 to 3.0.0 Upgrade (PHP to Python upgrade)

Be sure to have upgraded the database to the PHP Version 2.3.2

#### Passwords

The password hash function changed to Bcrypt so all user passwords from the PHP version will be
invalid.

The mail password is not being stored in the database anymore and has to be set in the
/instance/config.py (MAIL_TRANSPORT_PASSWORD). See /install/example_config.py

#### Content

Website text translations where completely rewritten.

Please backup your text translations at "Content" in the web interface and
enter them in "Settings" (intro and contact; faq was removed) again after executing the SQL below.

#### Database update

    BEGIN;
    DELETE FROM web.settings WHERE name = 'mail_transport_password';
    UPDATE web.settings SET name = 'site_name' WHERE name = 'sitename';
    UPDATE web.settings SET value = 'en' WHERE name = 'default_language';
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
    UPDATE model.entity SET name = 'Sex', description = 'Categories for sex like female, male.' WHERE name = 'Gender';
    UPDATE web.hierarchy SET name = 'Sex' WHERE name = 'Gender';
    ALTER TABLE web."user" ALTER COLUMN "active" DROP DEFAULT;
    ALTER TABLE web."user" ALTER COLUMN "active" TYPE bool USING active::bool;
    ALTER TABLE web."user" ALTER COLUMN "active" SET DEFAULT FALSE;
    ALTER TABLE IF EXISTS ONLY web.user_settings DROP CONSTRAINT IF EXISTS user_settings_user_id_name_value_key;
    ALTER TABLE ONLY web.user_settings ADD CONSTRAINT user_settings_user_id_name_key UNIQUE (user_id, name);
    INSERT INTO web.settings (name, value) VALUES ('minimum_password_length', '12');
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

    -- Source Type

    UPDATE web.hierarchy SET extendable = True WHERE name = 'Linguistic object classification';

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

    -- Rest


    ALTER TABLE web.hierarchy ALTER COLUMN multiple DROP DEFAULT;
    ALTER TABLE web.hierarchy ALTER COLUMN multiple TYPE bool USING multiple::bool;
    ALTER TABLE web.hierarchy ALTER COLUMN multiple SET DEFAULT FALSE;
    ALTER TABLE web.hierarchy ALTER COLUMN system DROP DEFAULT;
    ALTER TABLE web.hierarchy ALTER COLUMN system TYPE bool USING system::bool;
    ALTER TABLE web.hierarchy ALTER COLUMN system SET DEFAULT FALSE;
    ALTER TABLE web.hierarchy ALTER COLUMN extendable DROP DEFAULT;
    ALTER TABLE web.hierarchy ALTER COLUMN extendable TYPE bool USING extendable::bool;
    ALTER TABLE web.hierarchy ALTER COLUMN extendable SET DEFAULT FALSE;
    ALTER TABLE web.hierarchy ALTER COLUMN directional DROP DEFAULT;
    ALTER TABLE web.hierarchy ALTER COLUMN directional TYPE bool USING directional::bool;
    ALTER TABLE web.hierarchy ALTER COLUMN directional SET DEFAULT FALSE;
    ALTER TABLE ONLY web.hierarchy ADD CONSTRAINT hierarchy_name_key UNIQUE (name);

    COMMIT;

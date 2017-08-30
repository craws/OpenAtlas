## INFO

Before executing SQL statements make a backup of the database.

Replace database role "openatlas" if needed.

### 2.3.0 to 3.0.0 Upgrade (PHP to Python upgrade)

Be sure to have upgraded the database at least to the PHP Version 2.3.2

#### Passwords

Since the password hash function changed to Bcrypt, all passwords from the PHP version will be invalid.

#### Content

Website text translations where completely rewritten.

Please backup your text translations (Intro, Contact, FAQ) at "Content" in the web interface and
enter them in "Settings" again after executing the SQL below.

#### Database update

    BEGIN;
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
    COMMIT;

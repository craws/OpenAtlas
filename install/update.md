## INFO

   Before executing SQL statements make a backup of the database and replace database role "openatlas_master" if needed.

### 2.3.0 to 3.0.0 Upgrade (PHP to Python upgrade)

#### Content

    Website text translations where completely rewritten.
    So please backup your text translations (Intro, Contact, FAQ) at "Content" in the web interface and
    enter them in "Settings" again after executing the SQL below.

#### Database update

    BEGIN;
    UPDATE web.settings SET name = 'site_name' WHERE name = 'sitename';
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
    ALTER TABLE i18n OWNER TO openatlas_master;
    CREATE SEQUENCE i18n_id_seq
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1;
    ALTER TABLE i18n_id_seq OWNER TO openatlas_master;
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
    COMMIT;

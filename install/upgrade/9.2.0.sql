BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.2.0' WHERE name = 'database_version';

CREATE TABLE IF NOT EXISTS model.rights_holder
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    class text NOT NULL,
    description text,
    created timestamp without time zone NOT NULL DEFAULT now(),
    modified timestamp without time zone,
    CONSTRAINT rights_holder_pkey PRIMARY KEY (id)
);
CREATE TRIGGER update_modified BEFORE UPDATE ON model.rights_holder FOR EACH ROW EXECUTE PROCEDURE model.update_modified();

ALTER TABLE IF EXISTS model.rights_holder OWNER to openatlas;

CREATE TABLE IF NOT EXISTS model.rights_holder_file
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    entity_id integer NOT NULL,
    rights_holder_id integer NOT NULL,
    role text NOT NULL,
    description text,
    CONSTRAINT rights_holder_file_pkey PRIMARY KEY (id),
    CONSTRAINT fk_entity FOREIGN KEY (entity_id)
        REFERENCES model.entity (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT fk_rights_holder FOREIGN KEY (rights_holder_id)
        REFERENCES model.rights_holder (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    created timestamp without time zone NOT NULL DEFAULT now(),
    modified timestamp without time zone
);

CREATE TRIGGER update_modified BEFORE UPDATE ON model.rights_holder_file FOR EACH ROW EXECUTE PROCEDURE model.update_modified();

ALTER TABLE IF EXISTS model.rights_holder_file OWNER to openatlas;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_rights_holder_name') THEN
        ALTER TABLE model.rights_holder ADD CONSTRAINT uq_rights_holder_name UNIQUE (name);
    END IF;
END $$;


INSERT INTO model.rights_holder (name, class)
SELECT DISTINCT TRIM(name), 'person'
FROM (
    SELECT creator AS name FROM model.file_info WHERE creator IS NOT NULL
    UNION
    SELECT license_holder AS name FROM model.file_info WHERE license_holder IS NOT NULL
) AS all_names
WHERE TRIM(name) <> ''
ON CONFLICT (name) DO NOTHING;


INSERT INTO model.rights_holder_file (entity_id, rights_holder_id, role)
SELECT
    f.entity_id,
    r.id,
    'creator'
FROM model.file_info f
JOIN model.rights_holder r ON TRIM(f.creator) = r.name
WHERE f.creator IS NOT NULL AND TRIM(f.creator) <> '';


INSERT INTO model.rights_holder_file (entity_id, rights_holder_id, role)
SELECT
    f.entity_id,
    r.id,
    'license_holder'
FROM model.file_info f
JOIN model.rights_holder r ON TRIM(f.license_holder) = r.name
WHERE f.license_holder IS NOT NULL AND TRIM(f.license_holder) <> '';


ALTER TABLE model.file_info
    DROP COLUMN creator,
    DROP COLUMN license_holder CASCADE;

END;

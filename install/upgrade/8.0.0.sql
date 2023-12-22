-- Upgrade 7.17.x to 8.0.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.0.0' WHERE name = 'database_version';

-- #2054: Remove content for presentation sites
DELETE FROM web.i18n WHERE name IN (
    'contact_for_frontend',
    'intro_for_frontend',
    'legal_notice_for_frontend',
    'site_name_for_frontend');

-- #2096: Add presentation site link in backend
INSERT INTO web.settings (name, value) VALUES
    ('frontend_website_url', ''),
    ('frontend_resolver_url', '');

-- #1910 IIIF annotation system
CREATE TABLE IF NOT EXISTS web.annotation_image (
    id integer NOT NULL,
    image_id integer NOT NULL,
    entity_id integer,
    coordinates text COLLATE pg_catalog."default" NOT NULL,
    user_id integer,
    annotation text COLLATE pg_catalog."default" NOT NULL,
    created timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT annotation_image_pkey PRIMARY KEY (id),
    CONSTRAINT annotation_image_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT annotation_image_image_id_fkey FOREIGN KEY (image_id) REFERENCES model.entity (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE NOT VALID,
    CONSTRAINT annotation_image_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user" (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE SET NULL NOT VALID
);

ALTER TABLE IF EXISTS web.annotation_image OWNER to openatlas;
CREATE SEQUENCE web.annotation_image_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE web.annotation_image_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.annotation_image_id_seq OWNED BY web.annotation_image.id;
ALTER TABLE ONLY web.annotation_image ALTER COLUMN id SET DEFAULT nextval('web.annotation_image_id_seq'::regclass);

END;

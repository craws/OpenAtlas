-- Upgrade 8.1.x to 8.4.0
-- Be sure to backup the database and read the upgrade notes before executing.

-- Duplicate overlay will be removed with the SQL below. They should have the
-- the same coordinates, but you can check with following SQL before running
-- the database update script.

--  SELECT a.id, a.bounding_box FROM web.map_overlay a WHERE (
-- 	SELECT count(*) FROM web.map_overlay b WHERE a.image_id = b.image_id and a.bounding_box != b.bounding_box
--  ) > 1

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.4.0' WHERE name = 'database_version';

-- #2158 - Overlays for multiple places
ALTER TABLE web.map_overlay DROP COLUMN IF EXISTS link_id, DROP COLUMN IF EXISTS place_id;

DELETE FROM web.map_overlay a
    USING web.map_overlay  b
    WHERE a.id > b.id AND a.image_id = b.image_id;

ALTER TABLE web.map_overlay ADD CONSTRAINT map_overlay_image_id_key UNIQUE (image_id);

-- #2261 Option to prevent selection of a type
DROP TABLE IF EXISTS web.type_none_selectable;
DROP SEQUENCE IF EXISTS web.type_none_selectable_id_seq;
CREATE SEQUENCE web.type_none_selectable_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
ALTER TABLE web.type_none_selectable_id_seq OWNER TO openatlas;

CREATE TABLE web.type_none_selectable (
    "id" integer DEFAULT nextval('web.type_none_selectable_id_seq') NOT NULL,
    "entity_id" integer NOT NULL,
    "created" timestamp DEFAULT now() NOT NULL,
    CONSTRAINT "type_none_selectable_pkey" PRIMARY KEY ("id")
);
ALTER TABLE IF EXISTS web.type_none_selectable OWNER to openatlas;
COMMENT ON TABLE web.type_none_selectable IS 'IDs of types that are not meant to be selected, e.g. a category';

ALTER TABLE ONLY web.type_none_selectable ADD CONSTRAINT entity_id_key UNIQUE (entity_id);
ALTER TABLE ONLY web.type_none_selectable ADD CONSTRAINT "type_none_selectable_entity_id_fkey"
    FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

END;

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

END;

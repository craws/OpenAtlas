-- Upgrade 3.9.0 to 3.10.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Remove all property links to node roots because not needed anymore
DELETE FROM model.link_property WHERE property_code = 'P2' AND range_id IN (SELECT id FROM web.hierarchy);

-- Remove IP logging
ALTER TABLE web.system_log DROP COLUMN ip;

COMMIT;

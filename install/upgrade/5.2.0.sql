-- Upgrade 5.1.0 to 5.2.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- #1167: Settings and profile
DELETE FROM settings WHERE name = 'minimum_tablesorter_search';
ALTER TABLE ONLY web.settings ADD CONSTRAINT settings_name_key UNIQUE (name);

COMMIT;

-- Upgrade 5.0.0 to 5.1.0
-- Be sure to backup the database and read the update notes before executing this!

BEGIN;

-- #1167: Settings and profile
DELETE FROM settings WHERE name = 'minimum_tablesorter_search';

COMMIT;

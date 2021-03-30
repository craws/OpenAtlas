-- Upgrade 6.0.0 to 6.1.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- Remove obsolete debug_mode
DELETE FROM web.settings WHERE name = 'debug_mode';

COMMIT;

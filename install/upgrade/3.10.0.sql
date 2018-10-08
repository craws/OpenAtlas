-- Upgrade 3.9.0 to 3.10.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Remove IP logging
ALTER TABLE web.system_log DROP COLUMN ip;

COMMIT;

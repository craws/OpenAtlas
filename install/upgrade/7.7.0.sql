-- Upgrade 7.5.0 to 7.7.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.7.0' WHERE name = 'database_version';

END;

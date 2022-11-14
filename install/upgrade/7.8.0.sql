-- Upgrade 7.7.0 to 7.8.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.8.0' WHERE name = 'database_version';

-- Option to make types required (#1400)
ALTER TABLE web.hierarchy ADD COLUMN "required" boolean DEFAULT false NOT NULL;

END;

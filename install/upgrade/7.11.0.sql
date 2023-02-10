-- Upgrade 7.10.0 to 7.11.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- For now there are only some cleanup statements so need to raise version

-- Raise database version
-- UPDATE web.settings SET value = '7.11.0' WHERE name = 'database_version';

-- Remove setting for show API buttons (#)
DELETE FROM web.user_settings WHERE name = 'entity_show_api';

-- Remove old logs
DELETE FROM web.system_log WHERE created < '2022-01-01';

END;

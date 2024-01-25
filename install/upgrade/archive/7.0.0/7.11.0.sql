-- Upgrade 7.10.0 to 7.11.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.11.0' WHERE name = 'database_version';

-- Remove setting for show API buttons (#1963)
DELETE FROM web.user_settings WHERE name = 'entity_show_api';

-- Remove system logs before 2022, delete this if you want to keep them (#1964)
DELETE FROM web.system_log WHERE created < '2022-01-01';

END;

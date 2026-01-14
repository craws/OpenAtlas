BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.1.0' WHERE name = 'database_version';

-- Remove overlay option (#2703)
DELETE FROM web.settings WHERE name = 'module_map_overlay';
DELETE FROM web.user_settings WHERE name = 'module_map_overlay';

END;

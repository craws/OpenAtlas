-- Upgrade 7.5.0 to 7.7.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.7.0' WHERE name = 'database_version';

-- Remove subunit module
DELETE FROM web.settings WHERE name = 'module_sub_units';
DELETE FROM web.user_settings WHERE name = 'module_sub_units';

-- Fix that 'Features for sexing' type wasn't set to multiple
UPDATE web.hierarchy SET multiple = true WHERE name = 'Features for sexing';

-- Rename "actor actor relation" to just "actor relation"
UPDATE web.hierarchy SET name = 'Actor relation' WHERE name = 'Actor actor relation';
UPDATE model.entity SET name = 'Actor relation' WHERE id = (SELECT id FROM web.hierarchy WHERE name = 'Actor relation');
UPDATE model.openatlas_class SET name = 'actor_relation' WHERE name = 'actor_actor_relation';

END;

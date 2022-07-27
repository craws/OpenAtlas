-- Upgrade 7.4.0 to 7.5.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.5.0' WHERE name = 'database_version';

-- Remove reference system flag from type_anthropology
UPDATE model.openatlas_class SET reference_system_allowed = false WHERE name = 'type_anthropology';

END;

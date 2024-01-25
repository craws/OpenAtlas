-- Upgrade 7.15.0 to 7.16.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.16.0' WHERE name = 'database_version';

-- #2051 Wrong direction for P9
UPDATE model.link SET domain_id=range_id, range_id=domain_id
WHERE property_code = 'P9';

END;

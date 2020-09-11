-- Upgrade 5.4.0 to 5.5.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- Remove leading and trailing white spaces from names
UPDATE model.entity SET name = TRIM(name);

-- #929: Module options
INSERT INTO web.settings (name, value) VALUES
    ('module_geonames', ''),
    ('module_map_overlay', ''),
    ('module_notes', ''),
    ('module_sub_units', '');

COMMIT;

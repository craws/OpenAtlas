-- Upgrade 5.3.0 to 5.4.0
-- Be sure to backup the database and read the upgrade notes before executing this!

BEGIN;

-- #929: Module options
INSERT INTO settings (name, value) VALUES
    ('module_geonames', ''),
    ('module_map_overlay', ''),
    ('module_notes', ''),
    ('module_sub_units', '');

COMMIT;

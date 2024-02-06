-- Upgrade 7.3.0 to 7.4.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.4.0' WHERE name = 'database_version';

-- #1574 Dates with hours and minutes
INSERT INTO web.settings (name, value) VALUES ('module_time', '');

-- #1620: Natural events
INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
    ('event',    'E5', false, true,  true, 'contributor',      '#0000FF',      'mdi-calendar',             (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1));

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
    ((SELECT id FROM web.hierarchy WHERE name='Event'), 'event');

END;

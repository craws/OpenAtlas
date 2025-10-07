BEGIN;

-- Raise database version
-- UPDATE web.settings SET value = '9.0.0' WHERE name = 'database_version';

-- New classes (#2464)

-- Remove creation and event classes, after mapping to new ones (#2634)
UPDATE model.entity SET (cidoc_class_code, openatlas_class_name) = ('E7', 'activity') WHERE openatlas_class_name = 'event';
UPDATE model.entity SET (cidoc_class_code, openatlas_class_name) = ('E12', 'production') WHERE openatlas_class_name = 'creation';
DELETE FROM model.link WHERE property_code = 'P94';

-- Remove obsolete class definitions
DELETE FROM model.openatlas_class WHERE name IN ('actor_function', 'actor_relation', 'creation', 'event', 'involvement');

END;

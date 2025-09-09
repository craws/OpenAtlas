BEGIN;

-- Raise database version
-- UPDATE web.settings SET value = '9.0.0' WHERE name = 'database_version';

-- New classes (#2464)

-- Remove obsolete class definitions
DELETE FROM model.openatlas_class WHERE name IN ('actor_function', 'actor_relation', 'involvement');

END;

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.6.0' WHERE name = 'database_version';

-- Add fuzzystrmatch extension and phonetic GIN index on model.entity.name
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;
CREATE INDEX IF NOT EXISTS entity_name_dm_idx ON model.entity USING gin (public.daitch_mokotoff(name));

END;

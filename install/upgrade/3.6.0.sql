-- Upgrade to 3.6.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Add value types

ALTER TABLE web.hierarchy ADD COLUMN value_type boolean;
COMMENT ON COLUMN web.hierarchy.value_type IS 'True if links to this type can have numeric values';
ALTER TABLE web.hierarchy ALTER column value_type SET DEFAULT false;
UPDATE web.hierarchy SET value_type = false;
ALTER TABLE web.hierarchy ALTER column value_type SET NOT NULL;

COMMIT;

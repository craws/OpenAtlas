-- Upgrade to 3.12.0 to 3.13.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Drop obsolete value_integer field
ALTER TABLE model.entity DROP COLUMN value_integer;

COMMIT;

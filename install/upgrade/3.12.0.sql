-- Upgrade to 3.11.0 to 3.12.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Fix possible naming errors at gis point
UPDATE gis.point SET type = 'centerpoint';

COMMIT;

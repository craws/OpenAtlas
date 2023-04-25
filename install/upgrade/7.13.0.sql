-- Upgrade 7.12.0 to 7.13.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Fix direction of preceding events (#2007)
UPDATE model.link SET domain_id = range_id, range_id = domain_id WHERE property_code = 'P134';

-- Fix spelling errors in model (#2009)
UPDATE model.property SET name = 'begins in' WHERE code = 'OA8';
UPDATE model.property SET name = 'ends in' WHERE code = 'OA9';

END;

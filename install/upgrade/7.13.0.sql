-- Upgrade 7.12.0 to 7.13.0
-- Be sure to backup the database and read the upgrade notes before executing.

-- So far the database version wasn't raised for 7.12.0 so the database upgrade
-- script won't execute this file. Reason for this is that there is more to
-- to come but feel free to execute it manually. So far SQL Code below won't
-- be problematic if run again with the database upgrade script later.

BEGIN;

-- Fix spelling errors in model (#2009)
UPDATE model.property SET name = 'begins in' WHERE code = 'OA8';
UPDATE model.property SET name = 'ends in' WHERE code = 'OA9';

END;

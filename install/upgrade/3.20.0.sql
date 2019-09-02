-- Upgrade 3.19.x to 3.20.0
-- Be sure to backup the database and read the update notes before executing this!

BEGIN;

--  #1043 DataTables - Adaptions for DataTables
UPDATE web.settings SET value = '25' WHERE name= 'default_table_rows' AND value = '20';
UPDATE web.user_settings SET value = '25' WHERE name= 'table_rows' AND value = '20';

COMMIT;

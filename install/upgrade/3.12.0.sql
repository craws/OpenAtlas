-- Upgrade to 3.11.0 to 3.12.0, be sure to backup the database and read the update notes before executing this!

BEGIN;

-- Adding settings for minimum character search limits
INSERT INTO web.settings (name, value) VALUES ('minimum_jstree_search', '1');
INSERT INTO web.settings (name, value) VALUES ('minimum_tablesorter_search', '1');

-- Fix possible naming errors at gis point
UPDATE gis.point SET type = 'centerpoint';

COMMIT;

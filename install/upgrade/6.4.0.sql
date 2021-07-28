-- Upgrade 6.3.0 to 6.4.0
-- Be sure to backup the database and read the upgrade notes before executing!

-- Activate image processing (#1492)
INSERT INTO web.settings (name, value) VALUES ('image_processing', 'True');

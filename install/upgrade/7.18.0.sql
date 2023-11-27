-- Upgrade 7.17.x to 7.18.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.18.0' WHERE name = 'database_version';

-- #2096: Add presentation site link in backend
INSERT INTO web.settings (name, value) VALUES
    ('frontend_website_url', ''),
    ('frontend_resolver_url', '');

END;

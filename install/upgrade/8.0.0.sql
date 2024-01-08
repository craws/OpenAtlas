-- Upgrade 7.17.x to 8.0.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.0.0' WHERE name = 'database_version';

-- #2054: Remove content for presentation sites
DELETE FROM web.i18n WHERE name IN (
    'contact_for_frontend',
    'intro_for_frontend',
    'legal_notice_for_frontend',
    'site_name_for_frontend');

-- #2096: Add presentation site link in backend
INSERT INTO web.settings (name, value) VALUES
    ('frontend_website_url', ''),
    ('frontend_resolver_url', '');

END;

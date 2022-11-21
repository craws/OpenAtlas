-- Upgrade 7.8.0 to 7.9.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.9.0' WHERE name = 'database_version';

-- Add inverse translations for OA properties (#1885)
UPDATE model.property SET name_inverse = 'is first appearance of' WHERE code = 'OA8';
UPDATE model.property SET name_inverse = 'is last appearance of' WHERE code = 'OA9';

UPDATE model.property_i18n set text_inverse = 'ist erster Ort von' WHERE property_code = 'OA8' AND language_code = 'de';
UPDATE model.property_i18n set text_inverse = 'is first appearance of' WHERE property_code = 'OA8' AND language_code = 'en';
UPDATE model.property_i18n set text_inverse = 'ist letzter Ort von' WHERE property_code = 'OA9' AND language_code = 'de';
UPDATE model.property_i18n set text_inverse = 'is last appearance of' WHERE property_code = 'OA9' AND language_code = 'en';

END;

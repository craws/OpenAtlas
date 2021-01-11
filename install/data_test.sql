
-- Create test user
INSERT INTO web.user (group_id, username, password, active, email) VALUES
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Alice',    '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True,  'alice@example.com'),
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Inactive', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', False, 'inactive@example.com'),
    ((SELECT id FROM web.group WHERE name = 'editor'), 'Editor',  '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True,  'editor@example.com');

INSERT INTO web.user_settings (user_id, name, value) VALUES
    ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_dates', 'True'),
    ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_import', 'True'),
    ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_class', 'True'),
    ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_api', 'True');

-- Activate debug mode
UPDATE web.settings SET value = 'True' WHERE name = 'debug_mode';

-- Citation example
INSERT INTO web.i18n (name, language, text) VALUES ('citation_example', 'en', 'citation example');

-- Insert invalid link
INSERT INTO model.entity (class_code, name) VALUES ('E13', 'Invalid linked entity');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P86', (SELECT id FROM model.entity WHERE name = 'Invalid linked entity'), (SELECT id FROM model.entity WHERE name = 'Invalid linked entity'));

-- Remove external reference systems forms because they throw errors 'Not a valid choice' errors if not all of the precision field is set everytime
TRUNCATE web.reference_system_form;

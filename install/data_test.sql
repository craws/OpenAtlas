SET search_path = web;

-- Create test user
INSERT INTO web.user (group_id, username, password, active, email) VALUES
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Alice', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'alice@example.com'),
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Inactive', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', False, 'max@example.com');

INSERT INTO web.user_settings (user_id, name, value) VALUES ((SELECT id FROM web.user WHERE username = 'Alice'), 'layout', 'advanced');

-- Activate debug mode
UPDATE web.settings SET value = 'True' WHERE name = 'debug_mode';

-- Insert invalid link
INSERT INTO model.entity (class_code, name) VALUES ('E13', 'Invalid linked entity');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES ('P86', (SELECT id FROM model.entity WHERE name = 'Invalid linked entity'), (SELECT id FROM model.entity WHERE name = 'Invalid linked entity'));

SET search_path = web;

INSERT INTO web.user (group_id, username, password, active, email) VALUES
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Alice', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'alice@umbrella.net'),
    ((SELECT id FROM web.group WHERE name = 'admin'), 'Inactive', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', False, 'mad@max.net');

INSERT INTO web.user_settings (user_id, name, value) VALUES ((SELECT id FROM web.user WHERE username = 'Alice'), 'layout', 'advanced');

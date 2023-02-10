-- Create test user
INSERT INTO web.user (group_id, username, password, active, email, password_reset_code, password_reset_date, unsubscribe_code)
VALUES
  ((SELECT id FROM web.group WHERE name = 'admin'), 'Alice', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'alice@example.com', '1234', current_timestamp, NULL),
  ((SELECT id FROM web.group WHERE name = 'admin'), 'Inactive', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', False, 'inactive@example.com', NULL, NULL, NULL),
  ((SELECT id FROM web.group WHERE name = 'manager'), 'Manager', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'manager@example.com', '5678', '2020-02-02', '1234'),
  ((SELECT id FROM web.group WHERE name = 'contributor'), 'Contributor', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'contirbutor@example.com', NULL, NULL, NULL),
  ((SELECT id FROM web.group WHERE name = 'editor'), 'Editor', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'editor@example.com', NULL, NULL, NULL),
  ((SELECT id FROM web.group WHERE name = 'readonly'), 'Readonly', '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True, 'readonly@example.com', NULL, NULL, NULL);

INSERT INTO web.user_settings (user_id, name, value)
VALUES
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_class', 'True'),
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_dates', 'True'),
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_import', 'True'),
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'newsletter', 'True'),
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'module_time', 'True'),
  ((SELECT id FROM web.user WHERE username = 'Alice'), 'table_show_icons', 'True');

-- Citation example
INSERT INTO web.i18n (name, language, text) VALUES ('citation_example', 'en', 'citation example');

-- Log entry for none existing entity
INSERT INTO web.user_log (user_id, entity_id, action) VALUES (2, 6666, 'insert');

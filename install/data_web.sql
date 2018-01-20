SET search_path = web;

INSERT INTO "group" (name) VALUES
('admin'),
('editor'),
('manager'),
('readonly');

INSERT INTO web.user (username, password, active, email, group_id) VALUES (
    'OpenAtlas',
    '$2b$12$O.apSfFsSbpmYLDW/0QgyeHHenbiT0D72NLgOOQ4Rkju/oS15rJTu',
    true,
    'test@example.com',
    (SELECT id FROM web.group WHERE name = 'admin'));

INSERT INTO settings (name, value) VALUES
('debug_mode', ''),
('default_language', 'en'),
('default_table_rows', '20'),
('failed_login_forget_minutes', '1'),
('failed_login_tries', '3'),
('log_level', '6'),
('mail', ''),
('mail_transport_username', ''),
('mail_transport_port', ''),
('mail_transport_host', ''),
('mail_from_email', ''),
('mail_from_name', ''),
('mail_recipients_login', ''),
('mail_recipients_feedback', ''),
('minimum_password_length', '12'),
('random_password_length', '16'),
('reset_confirm_hours', '24'),
('site_name', 'OpenAtlas');

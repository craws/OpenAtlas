SET search_path = web;

INSERT INTO "group" (name) VALUES
('admin'),
('editor'),
('manager'),
('readonly');

INSERT INTO settings (name, value) VALUES
('default_language', 'en'),
('default_table_rows', '20'),
('failed_login_forget_minutes', '1'),
('failed_login_tries', '3'),
('log_level', '6'),
('maintenance', '0'),
('mail', '0'),
('mail_transport_username', ''),
('mail_transport_port', ''),
('mail_transport_host', ''),
('mail_from_email', ''),
('mail_from_name', ''),
('mail_recipients_login', ''),
('mail_recipients_feedback', ''),
('minimum_password_length', '12'),
('notify_login', '1'),
('offline', '1'),
('random_password_length', '16'),
('reset_confirm_hours', '24'),
('site_name', 'OpenAtlas');

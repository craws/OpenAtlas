SET search_path = web;

INSERT INTO "group" (name) VALUES
('admin'),
('editor'),
('manager'),
('readonly');

INSERT INTO settings (name, value) VALUES
('failed_login_forget_minutes', '1'),
('failed_login_tries', '3'),
('random_password_length', '16'),
('reset_confirm_hours', '24'),
('default_language', 'en'),
('log_level', '6'),
('maintenance', '0'),
('offline', '1'),
('site_name', 'OpenAtlas'),
('default_table_rows', '20'),
('notify_login', '1'),
('mail', '0'),
('mail_transport_username', ''),
('mail_transport_password', ''),
('mail_transport_ssl', ''),
('mail_transport_type', ''),
('mail_transport_auth', ''),
('mail_transport_port', ''),
('mail_transport_host', ''),
('mail_from_email', ''),
('mail_from_name', ''),
('mail_recipients_login', ''),
('mail_recipients_feedback', '')
;

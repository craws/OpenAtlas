SET search_path = web;

INSERT INTO "group" (name) VALUES
    ('admin'),
    ('contributor'),
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
    ('api_public', ''),
    ('debug_mode', ''),
    ('default_language', 'en'),
    ('default_table_rows', '25'),
    ('failed_login_forget_minutes', '1'),
    ('failed_login_tries', '3'),
    ('file_upload_max_size', '10'),
    ('file_upload_allowed_extension', 'gif jpeg jpg pdf png txt zip'),
    ('log_level', '6'),
    ('logo_file_id', ''),
    ('mail', ''),
    ('mail_transport_username', ''),
    ('mail_transport_port', ''),
    ('mail_transport_host', ''),
    ('mail_from_email', ''),
    ('mail_from_name', ''),
    ('mail_recipients_feedback', ''),
    ('map_cluster_max_radius', '50'),
    ('map_cluster_disable_at_zoom', '12'),
    ('minimum_jstree_search', '1'),
    ('minimum_password_length', '12'),
    ('profile_image_width', '200'),
    ('random_password_length', '16'),
    ('reset_confirm_hours', '24'),
    ('site_name', 'OpenAtlas');

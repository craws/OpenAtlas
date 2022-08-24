-- Create test user
INSERT INTO web.user (group_id, username, password, active, email)
VALUES ((SELECT id FROM web.group WHERE name = 'admin'), 'Alice',
        '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True,
        'alice@example.com'),
       ((SELECT id FROM web.group WHERE name = 'admin'), 'Inactive',
        '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', False,
        'inactive@example.com'),
       ((SELECT id FROM web.group WHERE name = 'editor'), 'Editor',
        '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK', True,
        'editor@example.com');

INSERT INTO web.user_settings (user_id, name, value)
VALUES ((SELECT id FROM web.user WHERE username = 'Alice'),
        'entity_show_dates', 'True'),
       ((SELECT id FROM web.user WHERE username = 'Alice'), 'table_show_icons',
        'True'),
       ((SELECT id FROM web.user WHERE username = 'Alice'),
        'entity_show_import', 'True'),
       ((SELECT id FROM web.user WHERE username = 'Alice'),
        'entity_show_class', 'True'),
       ((SELECT id FROM web.user WHERE username = 'Alice'), 'entity_show_api',
        'True'),
       ((SELECT id FROM web.user WHERE username = 'Alice'), 'module_time',
        'True');

-- Citation example
INSERT INTO web.i18n (name, language, text)
VALUES ('citation_example', 'en', 'citation example');
-- Content example for API
INSERT INTO web.i18n (name, language, text)
VALUES ('intro_for_frontend', 'en', 'This is English');
INSERT INTO web.i18n (name, language, text)
VALUES ('intro_for_frontend', 'de', 'Das ist Deutsch');

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name,
                name, description, begin_from, begin_to, begin_comment,
                end_from, end_to, end_comment)
VALUES ('E18', 'place', 'Shire','The Shire was the homeland of the hobbits.',
        '2018-01-31', '2018-03-01', 'Begin of the shire',  '2019-01-31',
        '2019-03-01','Descent of Shire'),
VALUES ('E53', 'location', 'Location of Shire', NONE, NONE, NONE, NONE, NONE,
    NONE, NONE,);


INSERT INTO model.gis (
                entity_id,
                name,
                description,
                type,
                geom_{shape})
            VALUES (
                (SELECT id from model.entity WHERE name='Location of Shire'),
                'Shire',
                'Nice place',
                'centerpoint',
                public.ST_SetSRID(public.ST_GeomFromGeoJSON('{"type":"Point","coordinates":[9, 17]}'),4326)
            );

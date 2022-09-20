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
VALUES ('E53', 'location', 'Location of Shire', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E53', 'feature', 'Home of Baggins', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E53', 'stratigraphic_unit', 'Bar', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E31', 'file', 'Picture with a License', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E31', 'file', 'File without license', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E21', 'person', 'Frodo', 'That is Frodo', NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E21', 'person', 'Sam', 'That is Sam', NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E32', 'external_reference', 'https://lotr.fandom.com/', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E41', 'appellation', 'Sûza', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E41', 'appellation', 'The ring bearer', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E22', 'artifact', 'The One Ring', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
VALUES ('E7', 'activity', 'Travel to Mordor', NONE, NONE, NONE, NONE, NONE, NONE, NONE),
    ;


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


INSERT INTO model.link (property_code, range_id, domain_id, description) VALUES
    ('P2', (SELECT id FROM model.entity WHERE name='Boundary Mark'), (SELECT id FROM model.entity WHERE name='Shire'), NULL),
    ('P1', (SELECT id FROM model.entity WHERE name='Sûza'), (SELECT id FROM model.entity WHERE name='Shire'), NULL),
    ('P1', (SELECT id FROM model.entity WHERE name='The ring bearer'), (SELECT id FROM model.entity WHERE name='Frodo'), NULL),
    ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), 'Fandom Wiki of lord of the rings'),
   ('P46', (SELECT id FROM model.entity WHERE name='Home of Baggins'), (SELECT id FROM model.entity WHERE name='Shire'), NULL),
   ('P46', (SELECT id FROM model.entity WHERE name='Bar'), (SELECT id FROM model.entity WHERE name='Home of Baggins'), NULL),
   ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Location of Shire'), NULL ),
   ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Location of Shire'), NULL ),
   ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Picture with a License'), NULL ),
   ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='File without license'), NULL ),
   ('P52', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='The One Ring'), NULL ),
   ('P2', (SELECT id FROM model.entity WHERE name='Open license'), (SELECT id FROM model.entity WHERE name='Picture with a License'), NULL ),
   ('P2', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Shire'), '23.0' ),
   ('P74', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam'), NULL ),
   ('P11', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Travel to Mordor'), NULL ),
   ('P14', (SELECT id FROM model.entity WHERE name='Sam'), (SELECT id FROM model.entity WHERE name='Travel to Mordor'), NULL ),
   ('P7', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Travel to Mordor'), NULL ),
   ;

INSERT INTO model.link (property_code, range_id, domain_id, description, type_id) VALUES
   ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='GeoNames'), '2761369', (SELECT id FROM model.entity WHERE name='closeMatch') ),
    ('OA7', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Sam'), NULL, (SELECT id FROM model.entity WHERE name='Friend of') ),

   ;

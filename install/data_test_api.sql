
-- Content example for API
INSERT INTO web.i18n (name, language, text) VALUES ('intro_for_frontend', 'en', 'This is English');
INSERT INTO web.i18n (name, language, text) VALUES ('intro_for_frontend', 'de', 'Das ist Deutsch');

INSERT INTO model.entity (
  cidoc_class_code, openatlas_class_name, name, description, begin_from, begin_to, begin_comment,
  end_from, end_to, end_comment, created, modified
) VALUES (
  'E18', 'place', 'Shire','The Shire was the homeland of the hobbits.',
  '2018-01-31', '2018-03-01', 'Begin of the shire', '2019-01-31',
  '2019-03-01','Descent of Shire', '2022-09-21 16:38:01.923431',
  '2022-09-21 16:38:05.923431'
);

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
  ('E53', 'object_location', 'Location of Shire', NULL),
  ('E18', 'place', 'Mordor', 'The heart of evil.'),
  ('E53', 'object_location', 'Location of Mordor', NULL),
  ('E22', 'artifact', 'The One Ring', NULL),
  ('E53', 'object_location', 'Location of The One Ring', NULL),
  ('E18', 'feature', 'Home of Baggins', NULL),
  ('E53', 'object_location', 'Location of Home of Baggins', NULL),
  ('E18', 'stratigraphic_unit', 'Bar', NULL),
  ('E53', 'object_location', 'Location of Bar', NULL),
  ('E31', 'file', 'Picture with a License', NULL),
  ('E31', 'file', 'File without license', NULL),
  ('E33', 'source', 'Silmarillion', NULL),
  ('E21', 'person', 'Frodo', 'That is Frodo'),
  ('E21', 'person', 'Sam', 'That is Sam'),
  ('E32', 'external_reference', 'https://lotr.fandom.com/', NULL),
  ('E41', 'appellation', 'Sûza', NULL),
  ('E41', 'appellation', 'The ring bearer', NULL),
  ('E7', 'activity', 'Travel to Mordor', NULL),
  ('E7', 'activity', 'Exchange of the one ring', NULL);


INSERT INTO model.gis (entity_id, name, description, type, geom_point, geom_polygon, geom_linestring)
VALUES
  ((SELECT id from model.entity WHERE name='Location of Mordor'),
  'Mordor',
  'Nicer place',
  'polyline',
  NULL,
  NULL,
  '0102000020E610000002000000890CC36E40FA3C4086C57C1702814440E3CB71BFA4F83C40A0D4D2DD13814440'),
  ((SELECT id from model.entity WHERE name='Location of Mordor'),
  'Mordor',
  'best place',
  'area',
  NULL,
  '0103000020E61000000100000005000000A13E6C6B5FF03C40527185FEB7834440E6FAEBBEE0F03C40270C23F97E8344404AE254EC24F13C406043D2B1A5834440A253097DA1F03C40A5422755CF834440A13E6C6B5FF03C40527185FEB7834440',
  NULL),
  ((SELECT id from model.entity WHERE name='Location of Shire'),
  'Shire',
  'best place',
  'area',
  NULL,
  '0103000020E61000000100000005000000A13E6C6B5FF03C40527185FEB7834440E6FAEBBEE0F03C40270C23F97E8344404AE254EC24F13C406043D2B1A5834440A253097DA1F03C40A5422755CF834440A13E6C6B5FF03C40527185FEB7834440',
  NULL),
  ((SELECT id from model.entity WHERE name='Location of Shire'),
  'Shire',
  'Nice place',
  'centerpoint',
  public.ST_SetSRID(public.ST_GeomFromGeoJSON('{"coordinates": [16.370696110389183, 48.20857123273274], "type": "Point"}'),4326),
  NULL,
  NULL),
  ((SELECT id from model.entity WHERE name='Location of Bar'),
  'Bar',
  'Nice bar',
  'polyline',
  NULL,
  NULL,
  public.ST_SetSRID(public.ST_GeomFromGeoJSON('{"coordinates": [[16.058535573227413,48.3288554316763],[16.058314371638566,48.32892676274859],[16.058390786732897,48.3289856108081]], "type": "LineString"}'),4326)),
  ((SELECT id from model.entity WHERE name='Location of Home of Baggins'),
  'Baggins Polygon',
  'Nice Baggins',
  'shape',
  NULL,
  public.ST_SetSRID(public.ST_GeomFromGeoJSON('{"coordinates": [[[9.208250656,58.950008233],[17.472247157,57.279042765],[20.197607706,62.955223045],[5.252082118,63.821287653],[9.208250656,58.950008233]]], "type": "Polygon"}'),4326),
  NULL);


INSERT INTO model.link (property_code, range_id, domain_id)
VALUES
  ('P2', (SELECT id FROM model.entity WHERE name='Boundary Mark'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P2', (SELECT id FROM model.entity WHERE name='Boundary Mark'), (SELECT id FROM model.entity WHERE name='Mordor')),
  ('P2', (SELECT id FROM model.entity WHERE name='Exchange'), (SELECT id FROM model.entity WHERE name='Exchange of the one ring')),
  ('P1', (SELECT id FROM model.entity WHERE name='Sûza'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P1', (SELECT id FROM model.entity WHERE name='The ring bearer'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('P46', (SELECT id FROM model.entity WHERE name='Home of Baggins'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P46', (SELECT id FROM model.entity WHERE name='Bar'), (SELECT id FROM model.entity WHERE name='Home of Baggins')),
  ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Location of Shire') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Shire') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Mordor'), (SELECT id FROM model.entity WHERE name='Mordor') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of The One Ring'), (SELECT id FROM model.entity WHERE name='The One Ring') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Home of Baggins'), (SELECT id FROM model.entity WHERE name='Home of Baggins') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Bar'), (SELECT id FROM model.entity WHERE name='Bar') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='File without license') ),
  ('P52', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='The One Ring') ),
  ('P2', (SELECT id FROM model.entity WHERE name='Open license'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P74', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam') ),
  ('P11', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Travel to Mordor') ),
  ('P14', (SELECT id FROM model.entity WHERE name='Sam'), (SELECT id FROM model.entity WHERE name='Travel to Mordor') ),
  ('P7', (SELECT id FROM model.entity WHERE name='Location of Mordor'), (SELECT id FROM model.entity WHERE name='Travel to Mordor') );


INSERT INTO model.link (property_code, range_id, domain_id, description, type_id)
VALUES
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='GeoNames'), '2761369', (SELECT id FROM model.entity WHERE name='close match') ),
  ('OA7', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Sam'), NULL, (SELECT id FROM model.entity WHERE name='Economical') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), 'Fandom Wiki of lord of the rings', NULL),
  ('P2', (SELECT id FROM model.entity WHERE name='Height'), (SELECT id FROM model.entity WHERE name='Shire'), '23.0', NULL );

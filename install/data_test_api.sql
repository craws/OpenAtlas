INSERT INTO model.entity (
  cidoc_class_code, openatlas_class_name, name, description, begin_from, begin_to, begin_comment, end_from, end_to, end_comment, created, modified)
VALUES
    ('E18', 'place', 'Shire','The Shire was the homeland of the hobbits.','2018-01-31', '2018-03-01', 'Begin of the shire', '2019-01-31',  '2019-03-01','Descent of Shire', '2022-09-21 16:38:01.923431','2022-09-21 16:38:05.923431'),
    ('E21', 'person', 'Sam', 'That is Sam','200-01-31', '200-03-01', 'Begin of the shire', '700-01-31', '800-03-01','Descent of Shire', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('E74', 'group', 'The Fellowship', '','215-01-31', '216-05-23', '', '700-01-31', '800-03-01','', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description, modified)
VALUES
  ('E53', 'object_location', 'Location of Shire', NULL, CURRENT_TIMESTAMP),
  ('E18', 'place', 'Mordor', 'The heart of evil.', CURRENT_TIMESTAMP),
  ('E53', 'object_location', 'Location of Mordor', NULL, CURRENT_TIMESTAMP),
  ('E22', 'artifact', 'The One Ring', 'The one ring', CURRENT_TIMESTAMP),
  ('E53', 'object_location', 'Location of The One Ring', NULL, CURRENT_TIMESTAMP),
  ('E18', 'feature', 'Home of Baggins', 'Home of Baggins', CURRENT_TIMESTAMP),
  ('E53', 'object_location', 'Location of Home of Baggins', NULL, CURRENT_TIMESTAMP),
  ('E18', 'stratigraphic_unit', 'Bar', NULL, CURRENT_TIMESTAMP),
  ('E53', 'object_location', 'Location of Bar', NULL, CURRENT_TIMESTAMP),
  ('E31', 'file', 'Picture with a License', 'With a license', CURRENT_TIMESTAMP),
  ('E31', 'file', 'File without license', 'No license', CURRENT_TIMESTAMP),
  ('E31', 'file', 'File without file', 'No file', CURRENT_TIMESTAMP),
  ('E31', 'file', 'File not public', 'Not public', CURRENT_TIMESTAMP),
  ('E33', 'source', 'Silmarillion', 'The Silmarillion', CURRENT_TIMESTAMP),
  ('E21', 'person', 'Frodo', 'That is Frodo', CURRENT_TIMESTAMP),
  ('E21', 'person', 'https://viaf.org/viaf/95218067', 'John Ronald Reuel Tolkien', CURRENT_TIMESTAMP),
  ('E31', 'external_reference', 'https://lotr.fandom.com/', NULL, CURRENT_TIMESTAMP),
  ('E31', 'bibliography', 'Frodo et. al.', 'Book of Frodo and his friends', CURRENT_TIMESTAMP),
  ('E41', 'appellation', 'Sûza', NULL, CURRENT_TIMESTAMP),
  ('E41', 'appellation', 'The ring bearer', NULL, CURRENT_TIMESTAMP),
  ('E7', 'activity', 'Travel to Mordor', NULL, CURRENT_TIMESTAMP),
  ('E7', 'activity', 'Exchange of the one ring', NULL, CURRENT_TIMESTAMP),
  ('E55', 'type', 'Lord of the rings', NULL, CURRENT_TIMESTAMP),
  ('E55', 'type', 'Case Study', NULL, CURRENT_TIMESTAMP),
  ('E55', 'type', 'Tavern', NULL, CURRENT_TIMESTAMP),
  ('E55', 'type', 'Hills', NULL, CURRENT_TIMESTAMP),
  ('E55', 'type', 'Ring', NULL, CURRENT_TIMESTAMP),
  ('E31', 'external_reference', 'https://en.wikipedia.org/wiki/Public_domain', NULL, CURRENT_TIMESTAMP),
  ('E31', 'external_reference', 'https://doi.org/10.2307/j.ctv1vtz8mq.3', NULL, CURRENT_TIMESTAMP);


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
  ('P127', (SELECT id FROM model.entity WHERE name='Case Study'), (SELECT id FROM model.entity WHERE name='Lord of the rings')),
  ('P127', (SELECT id FROM model.entity WHERE name='Stratigraphic unit'), (SELECT id FROM model.entity WHERE name='Tavern')),
  ('P127', (SELECT id FROM model.entity WHERE name='Feature'), (SELECT id FROM model.entity WHERE name='Hills')),
  ('P127', (SELECT id FROM model.entity WHERE name='Artifact'), (SELECT id FROM model.entity WHERE name='Ring')),
  ('P127', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='CC BY 4.0')),
  ('P127', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='CC BY-SA 4.0')),
  ('P2', (SELECT id FROM model.entity WHERE name='Boundary Mark'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P2', (SELECT id FROM model.entity WHERE name='Boundary Mark'), (SELECT id FROM model.entity WHERE name='Mordor')),
  ('P2', (SELECT id FROM model.entity WHERE name='Exchange'), (SELECT id FROM model.entity WHERE name='Exchange of the one ring')),
  ('P2', (SELECT id FROM model.entity WHERE name='Testament'), (SELECT id FROM model.entity WHERE name='Silmarillion')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Travel to Mordor')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Home of Baggins')),
  ('P2', (SELECT id FROM model.entity WHERE name='Hills'), (SELECT id FROM model.entity WHERE name='Home of Baggins')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Silmarillion')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='https://viaf.org/viaf/95218067')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Picture with a License')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='File without file')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='File not public')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/')),
  ('P2', (SELECT id FROM model.entity WHERE name='Ring'), (SELECT id FROM model.entity WHERE name='The One Ring')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='The One Ring')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Bar')),
  ('P2', (SELECT id FROM model.entity WHERE name='Tavern'), (SELECT id FROM model.entity WHERE name='Bar')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Mordor')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Sam')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='File without license')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('P74', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('OA8', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('OA9', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('P74', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam')),
  ('OA8', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam')),
  ('OA9', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam')),
  ('P2', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Exchange of the one ring')),
  ('P2', (SELECT id FROM model.entity WHERE name='Male'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('P2', (SELECT id FROM model.entity WHERE name='Link'), (SELECT id FROM model.entity WHERE name='https://en.wikipedia.org/wiki/Public_domain')),
  ('P1', (SELECT id FROM model.entity WHERE name='Sûza'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P1', (SELECT id FROM model.entity WHERE name='The ring bearer'), (SELECT id FROM model.entity WHERE name='Frodo')),
  ('P46', (SELECT id FROM model.entity WHERE name='Home of Baggins'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P2', (SELECT id FROM model.entity WHERE name='Hills'), (SELECT id FROM model.entity WHERE name='Home of Baggins')),
  ('P46', (SELECT id FROM model.entity WHERE name='Bar'), (SELECT id FROM model.entity WHERE name='Home of Baggins')),
  ('P46', (SELECT id FROM model.entity WHERE name='The One Ring'), (SELECT id FROM model.entity WHERE name='Shire')),
  ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Location of Shire') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Shire') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Mordor'), (SELECT id FROM model.entity WHERE name='Mordor') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of The One Ring'), (SELECT id FROM model.entity WHERE name='The One Ring') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Home of Baggins'), (SELECT id FROM model.entity WHERE name='Home of Baggins') ),
  ('P53', (SELECT id FROM model.entity WHERE name='Location of Bar'), (SELECT id FROM model.entity WHERE name='Bar') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P67', (SELECT id FROM model.entity WHERE name='https://viaf.org/viaf/95218067'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='File without license') ),
  ('P52', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='The One Ring') ),
  ('P2', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='Picture with a License') ),
  ('P2', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='File without file') ),
  ('P2', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='File not public') ),
  ('P74', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam') ),
  ('OA8', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam') ),
  ('OA9', (SELECT id FROM model.entity WHERE name='Location of Shire'), (SELECT id FROM model.entity WHERE name='Sam') ),
  ('P11', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Travel to Mordor') ),
  ('P11', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='The Fellowship') ),
  ('P11', (SELECT id FROM model.entity WHERE name='Sam'), (SELECT id FROM model.entity WHERE name='The Fellowship') ),
  ('P134', (SELECT id FROM model.entity WHERE name='Travel to Mordor'), (SELECT id FROM model.entity WHERE name='Exchange of the one ring') ),
  ('P7', (SELECT id FROM model.entity WHERE name='Location of Mordor'), (SELECT id FROM model.entity WHERE name='Travel to Mordor') );

INSERT INTO model.link (property_code, range_id, domain_id, begin_from, end_from)
VALUES
  ('P14', (SELECT id FROM model.entity WHERE name='Sam'), (SELECT id FROM model.entity WHERE name='Travel to Mordor'), '2018-03-01', '2018-04-01' );

INSERT INTO model.link (property_code, range_id, domain_id, description, type_id)
VALUES
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Frodo et. al.'), '987', NULL ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Frodo et. al.'), '234', NULL ),
  ('P67', (SELECT id FROM model.entity WHERE name='Picture with a License'), (SELECT id FROM model.entity WHERE name='Frodo et. al.'), '112', NULL ),
  ('P67', (SELECT id FROM model.entity WHERE name='Picture with a License'), (SELECT id FROM model.entity WHERE name='https://doi.org/10.2307/j.ctv1vtz8mq.3'), NULL, NULL ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='GeoNames'), '2761369', (SELECT id FROM model.entity WHERE name='close match') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Wikidata'), 'Q218728', (SELECT id FROM model.entity WHERE name='exact match') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Mordor'), (SELECT id FROM model.entity WHERE name='Wikidata'), 'Q202886', (SELECT id FROM model.entity WHERE name='exact match') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Wikidata'), 'Q177329', (SELECT id FROM model.entity WHERE name='exact match') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Sam'), (SELECT id FROM model.entity WHERE name='Wikidata'), 'Q219473', (SELECT id FROM model.entity WHERE name='exact match') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Lord of the rings'), (SELECT id FROM model.entity WHERE name='Wikidata'), 'Q15228', (SELECT id FROM model.entity WHERE name='exact match') ),
  ('OA7', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='Sam'), NULL, (SELECT id FROM model.entity WHERE name='Economical') ),
  ('P67', (SELECT id FROM model.entity WHERE name='Frodo'), (SELECT id FROM model.entity WHERE name='https://doi.org/10.2307/j.ctv1vtz8mq.3'), 'Studying The Lord of the Rings', NULL ),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), 'Fandom Wiki of lord of the rings', NULL),
  ('P67', (SELECT id FROM model.entity WHERE name='https://viaf.org/viaf/95218067'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), 'Fandom Wiki of lord of the rings', NULL),
  ('P67', (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='https://doi.org/10.2307/j.ctv1vtz8mq.3'), 'Studying The Lord of the Rings', NULL),
  ('P67', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), 'Public domain', NULL),
  ('P2', (SELECT id FROM model.entity WHERE name='Height'), (SELECT id FROM model.entity WHERE name='Shire'), '23.0', NULL ),
  ('P2', (SELECT id FROM model.entity WHERE name='Weight'), (SELECT id FROM model.entity WHERE name='Shire'), '999.0', NULL ),
  ('P2', (SELECT id FROM model.entity WHERE name='Link'), (SELECT id FROM model.entity WHERE name='https://lotr.fandom.com/'), NULL, NULL ),
  ('P2', (SELECT id FROM model.entity WHERE name='Public domain'), (SELECT id FROM model.entity WHERE name='https://en.wikipedia.org/wiki/Public_domain'), 'https://en.wikipedia.org/wiki/Public_domain', NULL ),
  ('P2', (SELECT id FROM model.entity WHERE name='CC BY 4.0'), (SELECT id FROM model.entity WHERE name='https://en.wikipedia.org/wiki/Public_domain'), 'https://creativecommons.org/licenses/by/4.0/deed.de', NULL ),
  ('P2', (SELECT id FROM model.entity WHERE name='CC BY-SA 4.0'), (SELECT id FROM model.entity WHERE name='https://en.wikipedia.org/wiki/Public_domain'), 'https://creativecommons.org/licenses/by-sa/4.0/deed.de', NULL );

INSERT INTO web.entity_profile_image (entity_id, image_id)
VALUES ( (SELECT id FROM model.entity WHERE name='Shire'), (SELECT id FROM model.entity WHERE name='Picture with a License') )
ON CONFLICT (entity_id) DO UPDATE SET image_id=(SELECT id FROM model.entity WHERE name='Picture with a License');

INSERT INTO web.map_overlay (image_id, bounding_box)
        VALUES ((SELECT id FROM model.entity WHERE name='Picture with a License'), '[[48.58653,15.64356],[48.58709,15.64294]]');

INSERT INTO model.file_info (entity_id, public, creator, license_holder)
VALUES
    ((SELECT id FROM model.entity WHERE name='File without license'), TRUE, 'https://viaf.org/viaf/95218067', NULL ),
    ((SELECT id FROM model.entity WHERE name='File without file'), TRUE, NULL, 'Sam' ),
    ((SELECT id FROM model.entity WHERE name='Picture with a License'), TRUE, 'https://viaf.org/viaf/95218067', 'Sauron' ),
    ((SELECT id FROM model.entity WHERE name='File not public'), FALSE, 'Sauron', NULL );

UPDATE model.entity
SET begin_from = CURRENT_DATE
WHERE name = 'Economical';


INSERT INTO web.hierarchy (id, name, multiple, category)
VALUES ((SELECT id FROM model.entity WHERE name='Case Study'), 'Case Study', true, 'custom');

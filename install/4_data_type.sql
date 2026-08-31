-- Default types and OpenAtlas classes

INSERT INTO model.openatlas_class (name, cidoc_class_code, new_types_allowed, write_access_group_name, standard_type_id) VALUES
  ('administrative_unit', 'E53', false, 'editor', NULL),
  ('type'               , 'E55', false, 'editor', NULL),
  ('type_tools'         , 'E55', false, 'admin',  NULL);

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Bibliography', 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.'),
  ('type', 'Inbook', Null),
  ('type', 'Article', Null),
  ('type', 'Book', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Inbook')),
  ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Article'))   ,
  ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Book'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Edition', 'Categories for the classification of written sources'' editions like charter editions, chronicle edition etc.'),
  ('type', 'Charter Edition', Null),
  ('type', 'Letter Edition', Null),
  ('type', 'Chronicle Edition', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Charter Edition')),
  ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Letter Edition')),
  ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Chronicle Edition'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'External reference', 'Categories for the classification of external references like a link to Wikipedia'),
  ('type', 'Link', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='External reference'), (SELECT id FROM model.entity WHERE name='Link'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'External reference match', 'SKOS based definition of the confidence degree that concepts can be used interchangeable.'),
  ('type', 'exact match', 'High degree of confidence that the concepts can be used interchangeably.'),
  ('type', 'close match', 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='exact match')),
  ('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='close match'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Actor function', 'Definitions of an actor''s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".'),
  ('type', 'Bishop', Null),
  ('type', 'Abbot', Null),
  ('type', 'Pope', Null),
  ('type', 'Emperor', Null),
  ('type', 'Count', Null),
  ('type', 'King', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Bishop')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Abbot')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Pope')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Emperor')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Count')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='King'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type', 'Artifact'),
  ('type', 'Coin'),
  ('type', 'Statue');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Artifact'), (SELECT id FROM model.entity WHERE name='Coin')),
  ('P127', (SELECT id FROM model.entity WHERE name='Artifact'), (SELECT id FROM model.entity WHERE name='Statue'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Involvement', 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".'),
  ('type', 'Creator', Null),
  ('type', 'Sponsor', Null),
  ('type', 'Victim', Null),
  ('type', 'Offender', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Creator')),
  ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Sponsor')),
  ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Victim')),
  ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Offender'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Sex', 'Categories for sex like female, male.'),
  ('type', 'Female', Null),
  ('type', 'Male', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Sex'), (SELECT id FROM model.entity WHERE name='Female')),
  ('P127', (SELECT id FROM model.entity WHERE name='Sex'), (SELECT id FROM model.entity WHERE name='Male'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Event', 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.'),
  ('type', 'Change of Property', Null),
  ('type', 'Donation', Null),
  ('type', 'Sale', Null),
  ('type', 'Exchange', Null),
  ('type', 'Conflict', Null),
  ('type', 'Battle', Null),
  ('type', 'Raid', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Event'), (SELECT id FROM model.entity WHERE name='Change of Property')),
  ('P127', (SELECT id FROM model.entity WHERE name='Event'), (SELECT id FROM model.entity WHERE name='Conflict')),
  ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Donation')),
  ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Sale')),
  ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Exchange')),
  ('P127', (SELECT id FROM model.entity WHERE name='Conflict'), (SELECT id FROM model.entity WHERE name='Battle')),
  ('P127', (SELECT id FROM model.entity WHERE name='Conflict'), (SELECT id FROM model.entity WHERE name='Raid'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Source', 'Types for historical sources like charter, chronicle, letter etc.'),
  ('type', 'Charter', Null),
  ('type', 'Testament', Null),
  ('type', 'Letter', Null),
  ('type', 'Contract', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Charter')),
  ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Testament')),
  ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Letter')),
  ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Contract'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'License', 'Type for the licensing of a file'),
  ('type', 'Public domain', Null),
  ('type', 'CC BY 4.0', Null),
  ('type', 'CC BY-SA 4.0', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='License'), (SELECT id FROM model.entity WHERE name='Public domain')),
  ('P127', (SELECT id FROM model.entity WHERE name='License'), (SELECT id FROM model.entity WHERE name='CC BY 4.0')),
  ('P127', (SELECT id FROM model.entity WHERE name='License'), (SELECT id FROM model.entity WHERE name='CC BY-SA 4.0'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Actor relation', 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).'),
  ('type', 'Kindredship', Null),
  ('type', 'Parent of (Child of)', Null),
  ('type', 'Social', Null),
  ('type', 'Friend of', Null),
  ('type', 'Enemy of', Null),
  ('type', 'Mentor of (Student of)', Null),
  ('type', 'Political', Null),
  ('type', 'Ally of', Null),
  ('type', 'Leader of (Retinue of)', Null),
  ('type', 'Economical', Null),
  ('type', 'Provider of (Customer of)', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Actor relation'), (SELECT id FROM model.entity WHERE name='Kindredship')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor relation'), (SELECT id FROM model.entity WHERE name='Social')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor relation'), (SELECT id FROM model.entity WHERE name='Political')),
  ('P127', (SELECT id FROM model.entity WHERE name='Actor relation'), (SELECT id FROM model.entity WHERE name='Economical')),
  ('P127', (SELECT id FROM model.entity WHERE name='Kindredship'), (SELECT id FROM model.entity WHERE name='Parent of (Child of)')),
  ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Friend of')),
  ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Enemy of')),
  ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Mentor of (Student of)')),
  ('P127', (SELECT id FROM model.entity WHERE name='Political'), (SELECT id FROM model.entity WHERE name='Ally of')),
  ('P127', (SELECT id FROM model.entity WHERE name='Political'), (SELECT id FROM model.entity WHERE name='Leader of (Retinue of)')),
  ('P127', (SELECT id FROM model.entity WHERE name='Economical'), (SELECT id FROM model.entity WHERE name='Provider of (Customer of)'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Place', 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.'),
  ('type', 'Settlement', Null),
  ('type', 'Military Facility', Null),
  ('type', 'Ritual Site', Null),
  ('type', 'Burial Site', Null),
  ('type', 'Infrastructure', Null),
  ('type', 'Economic Site', Null),
  ('type', 'Boundary Mark', Null),
  ('type', 'Topographical entity', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Settlement')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Military Facility')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Ritual Site')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Burial Site')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Infrastructure')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Economic Site')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Boundary Mark')),
  ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Topographical entity'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Feature', 'Classification of the archaeological feature e.g. grave, pit, ...'),
  ('type', 'Grave', Null),
  ('type', 'Pit', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Feature'), (SELECT id FROM model.entity WHERE name='Grave')),
  ('P127', (SELECT id FROM model.entity WHERE name='Feature'), (SELECT id FROM model.entity WHERE name='Pit'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Stratigraphic unit', 'Classification of the archaeological SU e.g. burial, deposit, ...'),
  ('type', 'Burial', Null),
  ('type', 'Deposit', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Stratigraphic unit'), (SELECT id FROM model.entity WHERE name='Burial')),
  ('P127', (SELECT id FROM model.entity WHERE name='Stratigraphic unit'), (SELECT id FROM model.entity WHERE name='Deposit'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Human remains', 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the model.entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).'),
  ('type', 'Upper Body', Null),
  ('type', 'Lower Body', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND openatlas_class_name = 'type'), (SELECT id FROM model.entity WHERE name='Upper Body')),
  ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND openatlas_class_name = 'type'), (SELECT id FROM model.entity WHERE name='Lower Body'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type', 'Text'),
  ('type', 'Original Text'),
  ('type', 'Translation'),
  ('type', 'Transliteration');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Text'), (SELECT id FROM model.entity WHERE name='Original Text')),
  ('P127', (SELECT id FROM model.entity WHERE name='Text'), (SELECT id FROM model.entity WHERE name='Translation')),
  ('P127', (SELECT id FROM model.entity WHERE name='Text'), (SELECT id FROM model.entity WHERE name='Transliteration'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Dimensions', 'Physical dimensions like weight and height.'),
  ('type', 'Height', 'centimeter'),
  ('type', 'Weight', 'gram');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Height')),
  ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Weight'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type', 'Case study', 'Mark entities for different case studies, used e.g. for presentation sites.');

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('type_tools', 'Features for sexing', 'Bone features used for biological sex estimation of human remains.'),
  ('type_tools', 'Radiocarbon', 'Used for radiocarbon dating'),
  ('type_tools', 'Skull', NULL),
  ('type_tools', 'Mandible', NULL),
  ('type_tools', 'Pelvis', NULL),
  ('type_tools', 'Robusticity', NULL);

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Skull'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
  ('P127', (SELECT id FROM model.entity WHERE name='Mandible'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
  ('P127', (SELECT id FROM model.entity WHERE name='Pelvis'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
  ('P127', (SELECT id FROM model.entity WHERE name='Robusticity'), (SELECT id FROM model.entity WHERE name='Features for sexing'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type_tools', 'Glabella'),
  ('type_tools', 'Arcus superciliaris'),
  ('type_tools', 'Tuber frontalis and parietalis'),
  ('type_tools', 'Inclinatio frontalis'),
  ('type_tools', 'Processus mastoideus'),
  ('type_tools', 'Relief of planum nuchale'),
  ('type_tools', 'Protuberantia occipitalis externa'),
  ('type_tools', 'Processus zygomaticus'),
  ('type_tools', 'Os zygomaticum'),
  ('type_tools', 'Crista supramastoideum'),
  ('type_tools', 'Margo supraorbitalis'),
  ('type_tools', 'Shape of orbita');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Glabella'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Arcus superciliaris'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Tuber frontalis and parietalis'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Inclinatio frontalis'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Processus mastoideus'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Relief of planum nuchale'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Protuberantia occipitalis externa'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Processus zygomaticus'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Os zygomaticum'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Crista supramastoideum'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Margo supraorbitalis'), (SELECT id FROM model.entity WHERE name='Skull')),
  ('P127', (SELECT id FROM model.entity WHERE name='Shape of orbita'), (SELECT id FROM model.entity WHERE name='Skull'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type_tools', 'Overall apperence'),
  ('type_tools', 'Mentum'),
  ('type_tools', 'Angulus'),
  ('type_tools', 'Margo inferior (M2)'),
  ('type_tools', 'Angle');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Overall apperence'), (SELECT id FROM model.entity WHERE name='Mandible')),
  ('P127', (SELECT id FROM model.entity WHERE name='Mentum'), (SELECT id FROM model.entity WHERE name='Mandible')),
  ('P127', (SELECT id FROM model.entity WHERE name='Angulus'), (SELECT id FROM model.entity WHERE name='Mandible')),
  ('P127', (SELECT id FROM model.entity WHERE name='Margo inferior (M2)'), (SELECT id FROM model.entity WHERE name='Mandible')),
  ('P127', (SELECT id FROM model.entity WHERE name='Angle'), (SELECT id FROM model.entity WHERE name='Mandible'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type_tools', 'Sulcus praeauricularis'),
  ('type_tools', 'Incisura ischiadica major'),
  ('type_tools', 'Angulus pubis'),
  ('type_tools', 'Arc composé'),
  ('type_tools', 'Os coxae'),
  ('type_tools', 'Foramen obturatum'),
  ('type_tools', 'Corpus ossis ischii'),
  ('type_tools', 'Crista iliaca'),
  ('type_tools', 'Fossa iliaca'),
  ('type_tools', 'Pelvis major'),
  ('type_tools', 'Auricular area'),
  ('type_tools', 'Sacrum'),
  ('type_tools', 'Fossa acetabuli');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Sulcus praeauricularis'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Incisura ischiadica major'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Angulus pubis'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Arc composé'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Os coxae'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Foramen obturatum'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Corpus ossis ischii'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Crista iliaca'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Fossa iliaca'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Pelvis major'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Auricular area'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Sacrum'), (SELECT id FROM model.entity WHERE name='Pelvis')),
  ('P127', (SELECT id FROM model.entity WHERE name='Fossa acetabuli'), (SELECT id FROM model.entity WHERE name='Pelvis'));

INSERT INTO model.entity (openatlas_class_name, name) VALUES
  ('type_tools', 'Humerus'),
  ('type_tools', 'Femur');
INSERT INTO model.link (property_code, domain_id, range_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Humerus'), (SELECT id FROM model.entity WHERE name='Robusticity')),
  ('P127', (SELECT id FROM model.entity WHERE name='Femur'), (SELECT id FROM model.entity WHERE name='Robusticity'));

INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
    ('type', 'Public sharing allowed', 'Mark files for public sharing, e.g. on presentation sites'),
    ('type', 'Yes', ''),
    ('type', 'No', '');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P127', (SELECT id FROM model.entity WHERE name='Public sharing allowed'), (SELECT id FROM model.entity WHERE name='Yes')),
  ('P127', (SELECT id FROM model.entity WHERE name='Public sharing allowed'), (SELECT id FROM model.entity WHERE name='No'));

INSERT INTO web.hierarchy (id, name, category, multiple, directional, required) VALUES
  ((SELECT id FROM model.entity WHERE name='Actor function'), 'Actor function', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Actor relation'), 'Actor relation', 'standard', False, True, False),
  ((SELECT id FROM model.entity WHERE name='Artifact'), 'Artifact', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Bibliography'), 'Bibliography', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Case study'), 'Case study', 'custom', True, False, False),
  ((SELECT id FROM model.entity WHERE name='Dimensions'), 'Dimensions', 'value', True, False, False),
  ((SELECT id FROM model.entity WHERE name='Edition'), 'Edition', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Event'), 'Event', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='External reference'), 'External reference', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='External reference match'), 'External reference match', 'system', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Feature'), 'Feature', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Features for sexing'), 'Features for sexing', 'tools', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Human remains' AND openatlas_class_name = 'type'), 'Human remains', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Involvement'), 'Involvement', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='License'), 'License', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Place'), 'Place', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Public sharing allowed'), 'Public sharing allowed', 'system', False, False, True),
  ((SELECT id FROM model.entity WHERE name='Radiocarbon'), 'Radiocarbon', 'tools', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Sex'), 'Sex', 'custom', True, False, False),
  ((SELECT id FROM model.entity WHERE name='Source'), 'Source', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Stratigraphic unit'), 'Stratigraphic unit', 'standard', False, False, False),
  ((SELECT id FROM model.entity WHERE name='Text'), 'Text', 'standard', False, False, False);

INSERT INTO model.openatlas_class (name, cidoc_class_code, new_types_allowed, write_access_group_name, standard_type_id) VALUES
  ('acquisition',          'E8',  true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('activity',             'E7',  true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('alias',                'E41', false, 'contributor', NULL),
  ('artifact',             'E22', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Artifact' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('bibliography',         'E31', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Bibliography' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('edition',              'E31', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Edition' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('external_reference',   'E31', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'External reference' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('feature',              'E18', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Feature' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('file',                 'E31', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'License' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('group',                'E74', true,  'contributor', NULL),
  ('human_remains',        'E20', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Human remains' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('modification',         'E11', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('move',                  'E9', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('object_location',      'E53', false, 'contributor', NULL),
  ('person',               'E21', true,  'contributor', NULL),
  ('place',                'E18', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Place' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('production',           'E12', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Event' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('reference_system',     'E32', false, 'manager',     NULL),
  ('source',               'E33', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Source' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('stratigraphic_unit',   'E18', true,  'contributor', (SELECT id FROM model.entity WHERE name = 'Stratigraphic unit' AND openatlas_class_name = 'type' ORDER BY id ASC LIMIT 1)),
  ('text',                 'E33', false, 'contributor', NULL);

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
  ((SELECT id FROM web.hierarchy WHERE name='Artifact'), 'artifact'),
  ((SELECT id FROM web.hierarchy WHERE name='Bibliography'), 'bibliography'),
  ((SELECT id FROM web.hierarchy WHERE name='Dimensions'), 'artifact'),
  ((SELECT id FROM web.hierarchy WHERE name='Edition'), 'edition'),
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'acquisition'),
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'activity'),
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'modification'),
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'move'),
  ((SELECT id FROM web.hierarchy WHERE name='Event'), 'production'),
  ((SELECT id FROM web.hierarchy WHERE name='External reference'), 'external_reference'),
  ((SELECT id FROM web.hierarchy WHERE name='Feature'), 'feature'),
  ((SELECT id FROM web.hierarchy WHERE name='Human remains'), 'human_remains'),
  ((SELECT id FROM web.hierarchy WHERE name='License'), 'file'),
  ((SELECT id FROM web.hierarchy WHERE name='Place'), 'place'),
  ((SELECT id FROM web.hierarchy WHERE name='Public sharing allowed'), 'file'),
  ((SELECT id FROM web.hierarchy WHERE name='External reference match'), 'reference_system'),
  ((SELECT id FROM web.hierarchy WHERE name='Sex'), 'person'),
  ((SELECT id FROM web.hierarchy WHERE name='Source'), 'source'),
  ((SELECT id FROM web.hierarchy WHERE name='Stratigraphic unit'), 'stratigraphic_unit'),
  ((SELECT id FROM web.hierarchy WHERE name='Text'), 'text');

-- External Reference Systems
INSERT INTO model.entity (openatlas_class_name, name, description) VALUES
  ('reference_system', 'GeoNames', 'Geographical database covering all countries and many places.'),
  ('reference_system', 'Wikidata', 'A free and open knowledge base and common source of open data providing persistent identifier and links to other sources.'),
  ('reference_system', 'GND', 'GND stands for Gemeinsame Normdatei (Integrated Authority File) and offers a broad range of elements to describe authorities.'),
  ('reference_system', 'DOI', 'A DOI (Digital Object Identifier) is a persistent identifier for digital resources. OpenAtlas uses Crossref for autocomplete, but any DOI can be stored and resolved, even if it is not found there. Please enter only the DOI identifier itself, not the full URL or domain.'),
  ('reference_system', 'Cadaster', 'Austrian cadastre from the Federal Office of Metrology and Surveying Austria.'),
  ('reference_system', 'ChronOntology', 'iDAI.chronontology is a Linked Open Data gazetteer developed by the German Archaeological Institute (DAI) that connects and organizes historical and prehistoric period definitions across space, time, and scholarly disciplines. It provides a standardized framework for mapping chronological terms and their spatial overlaps, making regional period names machine-readable and interoperable across different databases.'),
  ('reference_system', 'VIAF', 'VIAF (Virtual International Authority File) is a major international service that clusters authority data from national libraries and cultural institutions worldwide into single, unified clusters.'),
  ('reference_system', 'Kulturpool', 'Kulturpool is Austria''s central digital portal for art, culture, and science, aggregating millions of digital objects and metadata from nationwide museums, libraries, and archives. Administered by the Natural History Museum Vienna (NHM), it serves as the official national aggregator for the European digital platform Europeana.'),
  ('reference_system', 'Getty AAT', 'Getty AAT (Art and Architecture Thesaurus) is a controlled vocabulary for art and architecture terms. AAT is a thesaurus containing generic terms, dates, relationships, sources, and notes for work types, roles, materials, styles, cultures, techniques, and other concepts related to art, architecture, and other cultural heritage (e.g., amphora, oil paint, olieverf, acetolysis, sintering, orthographic drawings, Olmeca, Rinascimento, Buddhism, watercolors, asa-no-ha-toji, sralais). Please enter only the Getty AAT identifier itself, not the full URL or domain.');

INSERT INTO web.reference_system (system, name, api, entity_id, resolver_url, website_url, identifier_example)
VALUES
  (true, 'GeoNames',      'GeoNames',      (SELECT id FROM model.entity WHERE name = 'GeoNames'      AND openatlas_class_name = 'reference_system'), 'https://www.geonames.org/', 'https://www.geonames.org/', '1234567'),
  (true, 'Wikidata',      'Wikidata',      (SELECT id FROM model.entity WHERE name = 'Wikidata'      AND openatlas_class_name = 'reference_system'), 'https://www.wikidata.org/entity/', 'https://www.wikidata.org', 'Q123'),
  (true, 'GND',           'GND',           (SELECT id FROM model.entity WHERE name = 'GND'           AND openatlas_class_name = 'reference_system'), 'https://lobid.org/gnd/', 'https://d-nb.info/standards/elementset/gnd', '119338467'),
  (true, 'DOI',           'DOI',           (SELECT id FROM model.entity WHERE name = 'DOI'           AND openatlas_class_name = 'reference_system'), 'https://doi.org/', 'https://www.crossref.org/', '10.5281/zenodo.20451000'),
  (true, 'Cadaster',      'Cadaster',      (SELECT id FROM model.entity WHERE name = 'Cadaster'      AND openatlas_class_name = 'reference_system'), 'https://kataster.bev.gv.at/api/gst/', 'https://kataster.bev.gv.at/', '01004/784/1'),
  (true, 'VIAF',          'VIAF',          (SELECT id FROM model.entity WHERE name = 'VIAF'          AND openatlas_class_name = 'reference_system'), 'https://viaf.org/viaf/', 'https://viaf.org', '6215151353538552720009'),
  (true, 'ChronOntology', 'ChronOntology', (SELECT id FROM model.entity WHERE name = 'ChronOntology' AND openatlas_class_name = 'reference_system'), 'https://chronontology.dainst.org/period/', 'https://chronontology.dainst.org/', 'UCBAClZzVqwh'),
  (true, 'Kulturpool',    'Kulturpool',    (SELECT id FROM model.entity WHERE name = 'Kulturpool'    AND openatlas_class_name = 'reference_system'), 'https://kulturpool.at/objekte/', 'https://kulturpool.at/', 'dfc50104-275f-44b7-aa9f-00975528a671'),
  (true, 'Getty AAT',     'GettyAAT',      (SELECT id FROM model.entity WHERE name = 'Getty AAT'     AND openatlas_class_name = 'reference_system'), 'https://vocab.getty.edu/page/aat/', 'https://www.getty.edu/research/tools/vocabularies/aat/', '300387513');

INSERT INTO model.link (property_code, range_id, domain_id) VALUES
  ('P2', (SELECT id FROM model.entity WHERE name='exact match'), (SELECT id FROM model.entity WHERE name='Cadaster')),
  ('P2', (SELECT id FROM model.entity WHERE name='exact match'), (SELECT id FROM model.entity WHERE name='Getty AAT')),
  ('P2', (SELECT id FROM model.entity WHERE name='exact match'), (SELECT id FROM model.entity WHERE name='DOI'));

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name) VALUES
  ((SELECT entity_id FROM web.reference_system WHERE name='GeoNames'), 'place'),
  ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'place'),
  ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'person'),
  ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'group'),
  ((SELECT entity_id FROM web.reference_system WHERE name='Getty AAT'), 'type'),
  ((SELECT entity_id FROM web.reference_system WHERE name='GND'), 'person'),
  ((SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'edition'),
  ((SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'external_reference'),
  ((SELECT entity_id FROM web.reference_system WHERE name='DOI'), 'bibliography');

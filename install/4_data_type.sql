-- Default types and OpenAtlas classes

INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
    ('administrative_unit',  'E53', false, false, false, 'contributor', NULL,      'mdi-map-marker', NULL),
    ('type',                 'E55', false, true,  false, 'editor',      NULL,      NULL,             NULL),
    ('type_anthropology',    'E55', false, true,  false, 'admin',      NULL,      NULL,             NULL);

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Bibliography', 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.'),
    ('E55', 'type', 'Inbook', Null),
    ('E55', 'type', 'Article', Null),
    ('E55', 'type', 'Book', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Inbook')),
    ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Article'))   ,
    ('P127', (SELECT id FROM model.entity WHERE name='Bibliography'), (SELECT id FROM model.entity WHERE name='Book'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Edition', 'Categories for the classification of written sources'' editions like charter editions, chronicle edition etc.'),
    ('E55', 'type', 'Charter Edition', Null),
    ('E55', 'type', 'Letter Edition', Null),
    ('E55', 'type', 'Chronicle Edition', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Charter Edition')),
    ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Letter Edition')),
    ('P127', (SELECT id FROM model.entity WHERE name='Edition'), (SELECT id FROM model.entity WHERE name='Chronicle Edition'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'External reference', 'Categories for the classification of external references like a link to Wikipedia'),
    ('E55', 'type', 'Link', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='External reference'), (SELECT id FROM model.entity WHERE name='Link'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'External reference match', 'SKOS based definition of the confidence degree that concepts can be used interchangeable.'),
    ('E55', 'type', 'exact match', 'High degree of confidence that the concepts can be used interchangeably.'),
    ('E55', 'type', 'close match', 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='exact match')),
    ('P127', (SELECT id FROM model.entity WHERE name='External reference match'), (SELECT id FROM model.entity WHERE name='close match'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Actor function', 'Definitions of an actor''s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".'),
    ('E55', 'type', 'Bishop', Null),
    ('E55', 'type', 'Abbot', Null),
    ('E55', 'type', 'Pope', Null),
    ('E55', 'type', 'Emperor', Null),
    ('E55', 'type', 'Count', Null),
    ('E55', 'type', 'King', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Bishop')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Abbot')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Pope')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Emperor')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='Count')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor function'), (SELECT id FROM model.entity WHERE name='King'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type', 'Artifact'),
    ('E55', 'type', 'Coin'),
    ('E55', 'type', 'Statue');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Artifact'), (SELECT id FROM model.entity WHERE name='Coin')),
    ('P127', (SELECT id FROM model.entity WHERE name='Artifact'), (SELECT id FROM model.entity WHERE name='Statue'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Involvement', 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".'),
    ('E55', 'type', 'Creator', Null),
    ('E55', 'type', 'Sponsor', Null),
    ('E55', 'type', 'Victim', Null),
    ('E55', 'type', 'Offender', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Creator')),
    ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Sponsor')),
    ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Victim')),
    ('P127', (SELECT id FROM model.entity WHERE name='Involvement'), (SELECT id FROM model.entity WHERE name='Offender'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Sex', 'Categories for sex like female, male.'),
    ('E55', 'type', 'Female', Null),
    ('E55', 'type', 'Male', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Sex'), (SELECT id FROM model.entity WHERE name='Female')),
    ('P127', (SELECT id FROM model.entity WHERE name='Sex'), (SELECT id FROM model.entity WHERE name='Male'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Event', 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.'),
    ('E55', 'type', 'Change of Property', Null),
    ('E55', 'type', 'Donation', Null),
    ('E55', 'type', 'Sale', Null),
    ('E55', 'type', 'Exchange', Null),
    ('E55', 'type', 'Conflict', Null),
    ('E55', 'type', 'Battle', Null),
    ('E55', 'type', 'Raid', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Event'), (SELECT id FROM model.entity WHERE name='Change of Property')),
    ('P127', (SELECT id FROM model.entity WHERE name='Event'), (SELECT id FROM model.entity WHERE name='Conflict')),
    ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Donation')),
    ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Sale')),
    ('P127', (SELECT id FROM model.entity WHERE name='Change of Property'), (SELECT id FROM model.entity WHERE name='Exchange')),
    ('P127', (SELECT id FROM model.entity WHERE name='Conflict'), (SELECT id FROM model.entity WHERE name='Battle')),
    ('P127', (SELECT id FROM model.entity WHERE name='Conflict'), (SELECT id FROM model.entity WHERE name='Raid'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Source', 'Types for historical sources like charter, chronicle, letter etc.'),
    ('E55', 'type', 'Charter', Null),
    ('E55', 'type', 'Testament', Null),
    ('E55', 'type', 'Letter', Null),
    ('E55', 'type', 'Contract', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Charter')),
    ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Testament')),
    ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Letter')),
    ('P127', (SELECT id FROM model.entity WHERE name='Source'), (SELECT id FROM model.entity WHERE name='Contract'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'License', 'Types for the licensing of a file'),
    ('E55', 'type', 'Proprietary license', Null),
    ('E55', 'type', 'Open license', Null),
    ('E55', 'type', 'Public domain', Null),
    ('E55', 'type', 'CC BY 4.0', Null),
    ('E55', 'type', 'CC BY-SA 4.0', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='License'), (SELECT id FROM model.entity WHERE name='Proprietary license')),
    ('P127', (SELECT id FROM model.entity WHERE name='License'), (SELECT id FROM model.entity WHERE name='Open license')),
    ('P127', (SELECT id FROM model.entity WHERE name='Open license'), (SELECT id FROM model.entity WHERE name='Public domain')),
    ('P127', (SELECT id FROM model.entity WHERE name='Open license'), (SELECT id FROM model.entity WHERE name='CC BY 4.0')),
    ('P127', (SELECT id FROM model.entity WHERE name='Open license'), (SELECT id FROM model.entity WHERE name='CC BY-SA 4.0'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Actor actor relation', 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).'),
    ('E55', 'type', 'Kindredship', Null),
    ('E55', 'type', 'Parent of (Child of)', Null),
    ('E55', 'type', 'Social', Null),
    ('E55', 'type', 'Friend of', Null),
    ('E55', 'type', 'Enemy of', Null),
    ('E55', 'type', 'Mentor of (Student of)', Null),
    ('E55', 'type', 'Political', Null),
    ('E55', 'type', 'Ally of', Null),
    ('E55', 'type', 'Leader of (Retinue of)', Null),
    ('E55', 'type', 'Economical', Null),
    ('E55', 'type', 'Provider of (Customer of)', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Actor actor relation'), (SELECT id FROM model.entity WHERE name='Kindredship')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor actor relation'), (SELECT id FROM model.entity WHERE name='Social')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor actor relation'), (SELECT id FROM model.entity WHERE name='Political')),
    ('P127', (SELECT id FROM model.entity WHERE name='Actor actor relation'), (SELECT id FROM model.entity WHERE name='Economical')),
    ('P127', (SELECT id FROM model.entity WHERE name='Kindredship'), (SELECT id FROM model.entity WHERE name='Parent of (Child of)')),
    ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Friend of')),
    ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Enemy of')),
    ('P127', (SELECT id FROM model.entity WHERE name='Social'), (SELECT id FROM model.entity WHERE name='Mentor of (Student of)')),
    ('P127', (SELECT id FROM model.entity WHERE name='Political'), (SELECT id FROM model.entity WHERE name='Ally of')),
    ('P127', (SELECT id FROM model.entity WHERE name='Political'), (SELECT id FROM model.entity WHERE name='Leader of (Retinue of)')),
    ('P127', (SELECT id FROM model.entity WHERE name='Economical'), (SELECT id FROM model.entity WHERE name='Provider of (Customer of)'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Place', 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.'),
    ('E55', 'type', 'Settlement', Null),
    ('E55', 'type', 'Military Facility', Null),
    ('E55', 'type', 'Ritual Site', Null),
    ('E55', 'type', 'Burial Site', Null),
    ('E55', 'type', 'Infrastructure', Null),
    ('E55', 'type', 'Economic Site', Null),
    ('E55', 'type', 'Boundary Mark', Null),
    ('E55', 'type', 'Topographical entity', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Settlement')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Military Facility')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Ritual Site')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Burial Site')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Infrastructure')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Economic Site')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Boundary Mark')),
    ('P127', (SELECT id FROM model.entity WHERE name='Place'), (SELECT id FROM model.entity WHERE name='Topographical entity'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Feature', 'Classification of the archaeological feature e.g. grave, pit, ...'),
    ('E55', 'type', 'Grave', Null),
    ('E55', 'type', 'Pit', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Feature'), (SELECT id FROM model.entity WHERE name='Grave')),
    ('P127', (SELECT id FROM model.entity WHERE name='Feature'), (SELECT id FROM model.entity WHERE name='Pit'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Stratigraphic unit', 'Classification of the archaeological SU e.g. burial, deposit, ...'),
    ('E55', 'type', 'Burial', Null),
    ('E55', 'type', 'Deposit', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Stratigraphic unit'), (SELECT id FROM model.entity WHERE name='Burial')),
    ('P127', (SELECT id FROM model.entity WHERE name='Stratigraphic unit'), (SELECT id FROM model.entity WHERE name='Deposit'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Human remains', 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the model.entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).'),
    ('E55', 'type', 'Upper Body', Null),
    ('E55', 'type', 'Lower Body', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND cidoc_class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Upper Body')),
    ('P127', (SELECT id FROM model.entity WHERE name='Human remains' AND cidoc_class_code = 'E55'), (SELECT id FROM model.entity WHERE name='Lower Body'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E53', 'administrative_unit', 'Administrative unit', 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.'),
    ('E53', 'administrative_unit', 'Austria', Null),
    ('E53', 'administrative_unit', 'Wien', Null),
    ('E53', 'administrative_unit', 'Niederösterreich', Null),
    ('E53', 'administrative_unit', 'Germany', Null),
    ('E53', 'administrative_unit', 'Italy', Null),
    ('E53', 'administrative_unit', 'Czech Republic', Null),
    ('E53', 'administrative_unit', 'Slovakia', Null),
    ('E53', 'administrative_unit', 'Slovenia', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Austria')),
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Italy')),
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Germany')),
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Czech Republic')),
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Slovakia')),
    ('P89', (SELECT id FROM model.entity WHERE name='Administrative unit'), (SELECT id FROM model.entity WHERE name='Slovenia')),
    ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Wien')),
    ('P89', (SELECT id FROM model.entity WHERE name='Austria'), (SELECT id FROM model.entity WHERE name='Niederösterreich'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E53', 'administrative_unit', 'Historical place', 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.'),
    ('E53', 'administrative_unit', 'Carantania', Null),
    ('E53', 'administrative_unit', 'Marcha Orientalis', Null),
    ('E53', 'administrative_unit', 'Comitatus Iauntal', Null),
    ('E53', 'administrative_unit', 'Kingdom of Serbia', Null);
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P89', (SELECT id FROM model.entity WHERE name='Historical place'), (SELECT id FROM model.entity WHERE name='Carantania')),
    ('P89', (SELECT id FROM model.entity WHERE name='Historical place'), (SELECT id FROM model.entity WHERE name='Marcha Orientalis')),
    ('P89', (SELECT id FROM model.entity WHERE name='Historical place'), (SELECT id FROM model.entity WHERE name='Comitatus Iauntal')),
    ('P89', (SELECT id FROM model.entity WHERE name='Historical place'), (SELECT id FROM model.entity WHERE name='Kingdom of Serbia'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type', 'Source translation'),
    ('E55', 'type', 'Original Text'),
    ('E55', 'type', 'Translation'),
    ('E55', 'type', 'Transliteration');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Source translation'), (SELECT id FROM model.entity WHERE name='Original Text')),
    ('P127', (SELECT id FROM model.entity WHERE name='Source translation'), (SELECT id FROM model.entity WHERE name='Translation')),
    ('P127', (SELECT id FROM model.entity WHERE name='Source translation'), (SELECT id FROM model.entity WHERE name='Transliteration'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type', 'Dimensions', 'Physical dimensions like weight and height.'),
    ('E55', 'type', 'Height', 'centimeter'),
    ('E55', 'type', 'Weight', 'gram');
INSERT INTO model.link (property_code, range_id, domain_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Height')),
    ('P127', (SELECT id FROM model.entity WHERE name='Dimensions'), (SELECT id FROM model.entity WHERE name='Weight'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type_anthropology', 'Features for sexing', 'Bone features used for biological sex estimation of human remains.'),
    ('E55', 'type_anthropology', 'Skull', NULL),
    ('E55', 'type_anthropology', 'Mandible', NULL),
    ('E55', 'type_anthropology', 'Pelvis', NULL),
    ('E55', 'type_anthropology', 'Robusticity', NULL);

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Skull'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='Mandible'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='Pelvis'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='Robusticity'), (SELECT id FROM model.entity WHERE name='Features for sexing'));


INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', 'Glabella'),
    ('E55', 'type_anthropology', 'Arcus superciliaris'),
    ('E55', 'type_anthropology', 'Tuber frontalis and parietalis'),
    ('E55', 'type_anthropology', 'Inclinatio frontalis'),
    ('E55', 'type_anthropology', 'Processus mastoideus'),
    ('E55', 'type_anthropology', 'Relief of planum nuchale'),
    ('E55', 'type_anthropology', 'Protuberantia occipitalis externa'),
    ('E55', 'type_anthropology', 'Processus zygomaticus'),
    ('E55', 'type_anthropology', 'Os zygomaticum'),
    ('E55', 'type_anthropology', 'Crista supramastoideum'),
    ('E55', 'type_anthropology', 'Margo supraorbitalis'),
    ('E55', 'type_anthropology', 'Shape of orbita');

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

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', 'Overall apperence'),
    ('E55', 'type_anthropology', 'Mentum'),
    ('E55', 'type_anthropology', 'Angulus'),
    ('E55', 'type_anthropology', 'Margo inferior (M2)'),
    ('E55', 'type_anthropology', 'Angle');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Overall apperence'), (SELECT id FROM model.entity WHERE name='Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='Mentum'), (SELECT id FROM model.entity WHERE name='Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='Angulus'), (SELECT id FROM model.entity WHERE name='Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='Margo inferior (M2)'), (SELECT id FROM model.entity WHERE name='Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='Angle'), (SELECT id FROM model.entity WHERE name='Mandible'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', 'Sulcus praeauricularis'),
    ('E55', 'type_anthropology', 'Incisura ischiadica major'),
    ('E55', 'type_anthropology', 'Angulus pubis'),
    ('E55', 'type_anthropology', 'Arc composé'),
    ('E55', 'type_anthropology', 'Os coxae'),
    ('E55', 'type_anthropology', 'Foramen obturatum'),
    ('E55', 'type_anthropology', 'Corpus ossis ischii'),
    ('E55', 'type_anthropology', 'Crista iliaca'),
    ('E55', 'type_anthropology', 'Fossa iliaca'),
    ('E55', 'type_anthropology', 'Pelvis major'),
    ('E55', 'type_anthropology', 'Auricular area'),
    ('E55', 'type_anthropology', 'Sacrum'),
    ('E55', 'type_anthropology', 'Fossa acetabuli');

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

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', 'Humerus'),
    ('E55', 'type_anthropology', 'Femur');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Humerus'), (SELECT id FROM model.entity WHERE name='Robusticity')),
    ('P127', (SELECT id FROM model.entity WHERE name='Femur'), (SELECT id FROM model.entity WHERE name='Robusticity'));

INSERT INTO web.hierarchy (id, name, category, multiple, directional) VALUES
    ((SELECT id FROM model.entity WHERE name='Actor function'), 'Actor function', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Actor actor relation'), 'Actor actor relation', 'standard', False, True),
    ((SELECT id FROM model.entity WHERE name='Administrative unit'), 'Administrative unit', 'place', True, False),
    ((SELECT id FROM model.entity WHERE name='Artifact'), 'Artifact', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Bibliography'), 'Bibliography', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Edition'), 'Edition', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Event'), 'Event', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='External reference'), 'External reference', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='External reference match'), 'External reference match', 'system', False, False),
    ((SELECT id FROM model.entity WHERE name='Feature'), 'Feature', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Features for sexing'), 'Features for sexing', 'anthropology',False , False),
    ((SELECT id FROM model.entity WHERE name='Historical place'), 'Historical place', 'place', True, False),
    ((SELECT id FROM model.entity WHERE name='Human remains' AND cidoc_class_code = 'E55'), 'Human remains', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Involvement'), 'Involvement', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='License'), 'License', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Source'), 'Source', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Place'), 'Place', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Stratigraphic unit'), 'Stratigraphic unit', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Source translation'), 'Source translation', 'standard', False, False),
    ((SELECT id FROM model.entity WHERE name='Dimensions'), 'Dimensions', 'value', True, False),
    ((SELECT id FROM model.entity WHERE name='Sex'), 'Sex', 'custom', False, False);

INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
    ('acquisition',          'E8',  false, true,  true,  'contributor', '#0000FF', 'mdi-calendar',   (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('activity',             'E7',  false, true,  true,  'contributor', '#0000FF', 'mdi-calendar',   (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('actor_actor_relation', NULL,  false, false, false, 'contributor', NULL,      NULL,             (SELECT id FROM model.entity WHERE name = 'Actor actor relation' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('actor_function',       NULL,  false, false, false, 'contributor', NULL,      NULL,             (SELECT id FROM model.entity WHERE name = 'Actor function' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('appellation',          'E41', false, false, false, 'contributor', NULL,      NULL,             NULL),
    ('artifact',             'E22', false, true,  true,  'contributor', '#EE82EE', 'mdi-shapes',     (SELECT id FROM model.entity WHERE name = 'Artifact' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('bibliography',         'E31', false, false, true,  'contributor', NULL,      'mdi-text-box',   (SELECT id FROM model.entity WHERE name = 'Bibliography' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('edition',              'E31', false, false, true,  'contributor', NULL,      'mdi-text-box',   (SELECT id FROM model.entity WHERE name = 'Edition' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('external_reference',   'E31', false, false, true,  'contributor', NULL,      'mdi-text-box',   (SELECT id FROM model.entity WHERE name = 'External reference' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('feature',              'E18', false, true,  true,  'contributor', NULL,      'mdi-map-marker', (SELECT id FROM model.entity WHERE name = 'Feature' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('file',                 'E31', false, false, true,  'contributor', NULL,      'mdi-text-box',   (SELECT id FROM model.entity WHERE name = 'License' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('group',                'E74', true,  true,  true,  'contributor', '#34623C', 'mdi-account',    NULL),
    ('human_remains',        'E20', false, true,  true,  'contributor', NULL,      'mdi-map-marker', (SELECT id FROM model.entity WHERE name = 'Human remains' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('involvement',          NULL,  false, false, false, 'contributor', NULL,      NULL,             (SELECT id FROM model.entity WHERE name = 'Involvement' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('move',                 'E9',  false, true,  true,  'contributor', '#0000FF', 'mdi-calendar',   (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('object_location',      'E53', false, false, false, 'contributor', '#00FF00', NULL,             NULL),
    ('person',               'E21', true,  true,  true,  'contributor', '#34B522', 'mdi-account',    NULL),
    ('place',                'E18', true,  true,  true,  'contributor', '#FF0000', 'mdi-map-marker', (SELECT id FROM model.entity WHERE name = 'Place' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('production',           'E12', false, true,  true,  'contributor', '#0000FF', 'mdi-calendar',   (SELECT id FROM model.entity WHERE name = 'Event' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('reference_system',     'E32', false, false, false, 'manager',     NULL,      NULL,             NULL),
    ('source',               'E33', false, true,  true,  'contributor', '#FFA500', 'mdi-text-box',   (SELECT id FROM model.entity WHERE name = 'Source' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1)),
    ('source_translation',   'E33', false, false, false, 'contributor', NULL,      'mdi-text-box',   NULL),
    ('stratigraphic_unit',   'E18', false, true,  true,  'contributor', NULL,      'mdi-map-marker', (SELECT id FROM model.entity WHERE name = 'Stratigraphic unit' AND cidoc_class_code = 'E55' ORDER BY id ASC LIMIT 1));

INSERT INTO web.hierarchy_openatlas_class (hierarchy_id, openatlas_class_name) VALUES
    ((SELECT id FROM web.hierarchy WHERE name='Actor function'), 'actor_function'),
    ((SELECT id FROM web.hierarchy WHERE name='Actor actor relation'), 'actor_actor_relation'),
    ((SELECT id FROM web.hierarchy WHERE name='Administrative unit'), 'place'),
    ((SELECT id FROM web.hierarchy WHERE name='Artifact'), 'artifact'),
    ((SELECT id FROM web.hierarchy WHERE name='Bibliography'), 'bibliography'),
    ((SELECT id FROM web.hierarchy WHERE name='Edition'), 'edition'),
    ((SELECT id FROM web.hierarchy WHERE name='Event'), 'acquisition'),
    ((SELECT id FROM web.hierarchy WHERE name='Event'), 'activity'),
    ((SELECT id FROM web.hierarchy WHERE name='Event'), 'move'),
    ((SELECT id FROM web.hierarchy WHERE name='Event'), 'production'),
    ((SELECT id FROM web.hierarchy WHERE name='External reference'), 'external_reference'),
    ((SELECT id FROM web.hierarchy WHERE name='Feature'), 'feature'),
    ((SELECT id FROM web.hierarchy WHERE name='Historical place'), 'place'),
    ((SELECT id FROM web.hierarchy WHERE name='Human remains'), 'human_remains'),
    ((SELECT id FROM web.hierarchy WHERE name='Involvement'), 'involvement'),
    ((SELECT id FROM web.hierarchy WHERE name='License'), 'file'),
    ((SELECT id FROM web.hierarchy WHERE name='Place'), 'place'),
    ((SELECT id FROM web.hierarchy WHERE name='Source'), 'source'),
    ((SELECT id FROM web.hierarchy WHERE name='Source translation'), 'source_translation'),
    ((SELECT id FROM web.hierarchy WHERE name='Stratigraphic unit'), 'stratigraphic_unit'),

    ((SELECT id FROM web.hierarchy WHERE name='Dimensions'), 'artifact'),
    ((SELECT id FROM web.hierarchy WHERE name='Sex'), 'person');

-- External Reference Systems
INSERT INTO model.entity (name, cidoc_class_code, description, openatlas_class_name) VALUES
    ('GeoNames', 'E32', 'Geographical database covering all countries and many places.', 'reference_system'),
    ('Wikidata', 'E32', 'A free and open knowledge base and common source of open data providing persistent identifier and links to other sources.', 'reference_system');

INSERT INTO web.reference_system (system, name, entity_id, resolver_url, website_url, identifier_example)
VALUES (
          true,
          'GeoNames',
          (SELECT id FROM model.entity WHERE name = 'GeoNames' AND cidoc_class_code = 'E32'),
          'https://www.geonames.org/',
          'https://www.geonames.org/',
          '1234567'),
       (
          true,
          'Wikidata',
          (SELECT id FROM model.entity WHERE name = 'Wikidata' AND cidoc_class_code = 'E32'),
          'https://www.wikidata.org/entity/',
          'https://www.wikidata.org',
          'Q123');

INSERT INTO web.reference_system_openatlas_class (reference_system_id, openatlas_class_name) VALUES
    ((SELECT entity_id FROM web.reference_system WHERE name='GeoNames'), 'place'),
    ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'place'),
    ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'person'),
    ((SELECT entity_id FROM web.reference_system WHERE name='Wikidata'), 'group');

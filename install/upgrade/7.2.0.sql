-- Upgrade 7.1.x to 7.2.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.2.0' WHERE name = 'database_version';

-- #1445: Tool - Anthropological sex estimation

INSERT INTO model.openatlas_class (name, cidoc_class_code, alias_allowed, reference_system_allowed, new_types_allowed, write_access_group_name, layout_color, layout_icon, standard_type_id) VALUES
    ('type_anthropology',    'E55', false, true,  false, 'admin',      NULL,      NULL,             NULL);

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type_anthropology', 'Features for sexing', 'Bone features used for biological sex estimation of human remains.'),
    ('E55', 'type_anthropology', '#-remove-#Skull', NULL),
    ('E55', 'type_anthropology', '#-remove-#Mandible', NULL),
    ('E55', 'type_anthropology', '#-remove-#Pelvis', NULL),
    ('E55', 'type_anthropology', '#-remove-#Robusticity', NULL);

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Skull'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Mandible'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis'), (SELECT id FROM model.entity WHERE name='Features for sexing')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Robusticity'), (SELECT id FROM model.entity WHERE name='Features for sexing'));


INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', '#-remove-#Glabella'),
    ('E55', 'type_anthropology', '#-remove-#Arcus superciliaris'),
    ('E55', 'type_anthropology', '#-remove-#Tuber frontalis and parietalis'),
    ('E55', 'type_anthropology', '#-remove-#Inclinatio frontalis'),
    ('E55', 'type_anthropology', '#-remove-#Processus mastoideus'),
    ('E55', 'type_anthropology', '#-remove-#Relief of planum nuchale'),
    ('E55', 'type_anthropology', '#-remove-#Protuberantia occipitalis externa'),
    ('E55', 'type_anthropology', '#-remove-#Processus zygomaticus'),
    ('E55', 'type_anthropology', '#-remove-#Os zygomaticum'),
    ('E55', 'type_anthropology', '#-remove-#Crista supramastoideum'),
    ('E55', 'type_anthropology', '#-remove-#Margo supraorbitalis'),
    ('E55', 'type_anthropology', '#-remove-#Shape of orbita');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Glabella'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Arcus superciliaris'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Tuber frontalis and parietalis'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Inclinatio frontalis'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Processus mastoideus'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Relief of planum nuchale'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Protuberantia occipitalis externa'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Processus zygomaticus'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Os zygomaticum'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Crista supramastoideum'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Margo supraorbitalis'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Shape of orbita'), (SELECT id FROM model.entity WHERE name='#-remove-#Skull'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', '#-remove-#Overall apperence'),
    ('E55', 'type_anthropology', '#-remove-#Mentum'),
    ('E55', 'type_anthropology', '#-remove-#Angulus'),
    ('E55', 'type_anthropology', '#-remove-#Margo inferior (M2)'),
    ('E55', 'type_anthropology', '#-remove-#Angle');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Overall apperence'), (SELECT id FROM model.entity WHERE name='#-remove-#Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Mentum'), (SELECT id FROM model.entity WHERE name='#-remove-#Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Angulus'), (SELECT id FROM model.entity WHERE name='#-remove-#Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Margo inferior (M2)'), (SELECT id FROM model.entity WHERE name='#-remove-#Mandible')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Angle'), (SELECT id FROM model.entity WHERE name='#-remove-#Mandible'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', '#-remove-#Sulcus praeauricularis'),
    ('E55', 'type_anthropology', '#-remove-#Incisura ischiadica major'),
    ('E55', 'type_anthropology', '#-remove-#Angulus pubis'),
    ('E55', 'type_anthropology', '#-remove-#Arc composé'),
    ('E55', 'type_anthropology', '#-remove-#Os coxae'),
    ('E55', 'type_anthropology', '#-remove-#Foramen obturatum'),
    ('E55', 'type_anthropology', '#-remove-#Corpus ossis ischii'),
    ('E55', 'type_anthropology', '#-remove-#Crista iliaca'),
    ('E55', 'type_anthropology', '#-remove-#Fossa iliaca'),
    ('E55', 'type_anthropology', '#-remove-#Pelvis major'),
    ('E55', 'type_anthropology', '#-remove-#Auricular area'),
    ('E55', 'type_anthropology', '#-remove-#Sacrum'),
    ('E55', 'type_anthropology', '#-remove-#Fossa acetabuli');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Sulcus praeauricularis'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Incisura ischiadica major'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Angulus pubis'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Arc composé'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Os coxae'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Foramen obturatum'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Corpus ossis ischii'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Crista iliaca'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Fossa iliaca'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis major'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Auricular area'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Sacrum'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Fossa acetabuli'), (SELECT id FROM model.entity WHERE name='#-remove-#Pelvis'));

INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_anthropology', '#-remove-#Humerus'),
    ('E55', 'type_anthropology', '#-remove-#Femur');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Humerus'), (SELECT id FROM model.entity WHERE name='#-remove-#Robusticity')),
    ('P127', (SELECT id FROM model.entity WHERE name='#-remove-#Femur'), (SELECT id FROM model.entity WHERE name='#-remove-#Robusticity'));

INSERT INTO web.hierarchy (id, name, multiple, category, directional) VALUES
((SELECT id FROM model.entity WHERE name='Features for sexing'), 'Features for sexing', False, 'anthropology', False);

UPDATE model.entity SET name = substr(name, 11, length(name)) WHERE name LIKE '#-remove-#%';

END;

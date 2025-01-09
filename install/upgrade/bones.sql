BEGIN;

-- Feature bone inventory (#1473)
INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name) VALUES
    ('E55', 'type_tools', 'Bone inventory'),
    ('E55', 'type_tools', 'Inventory: Skull'),
    ('E55', 'type_tools', 'Inventory: Teeth'),
    ('E55', 'type_tools', 'Inventory: Shoulder girdle'),
    ('E55', 'type_tools', 'Inventory: Arms and hands'),
    ('E55', 'type_tools', 'Inventory: Axial skeleton'),
    ('E55', 'type_tools', 'Inventory: Pelvis'),
    ('E55', 'type_tools', 'Inventory: Legs and feet');

INSERT INTO web.type_none_selectable (entity_id) VALES
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Bone inventory'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Skull'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Teeth'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Shoulder girdle'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Arms and hands'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Axial skeleton'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Pelvis'),
    (SELECT id FROM model.entiy WHERE openatlas_class_name = 'type_tools' AND name = 'Inventory: Legs and feet');

INSERT INTO model.link (property_code, domain_id, range_id) VALUES
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Skull'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Teeth'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Shoulder girdle'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Arms and hands'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Axial skeleton'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Pelvis'), (SELECT id FROM model.entity WHERE name='Bone inventory')),
    ('P127', (SELECT id FROM model.entity WHERE name='Inventory: Legs and feet'), (SELECT id FROM model.entity WHERE name='Bone inventory')),

-- Skull
INSERT INTO model.entity (cidoc_class_code, openatlas_class_name, name, description) VALUES
    ('E55', 'type_tools', ''),

-- Work in progress
    Frontal
        Orbit R
        Orbit L
    Parietal R
    Parietal L
    Temporal R
        Squama R
        Petrous R
        Mastoid R
    Temporal R
        Squama L
        Petrous L
        Mastoid L
    Occipital
        Pars squama
        Pars lateralis R
        Pars lateralis L
        Pars basilaris R
        Pars basilaris L
    Sphenoid
        Ala major R
        Ala minor R
        Ala major L
        Ala minor L
        Sphenoid body
    Maxilla R
    Maxilla L
    Nasal R
    Nasal L
    Lacrimale R
    Lacrimale L
    Ethmoid
    Zygomatic R
    Zygomatic L
    Vomer
    Palate R
    Palate L
    Inferior conchae R
    Inferior conchae L
    Mandible R
        Ramus R
        Condyle R
    Mandible L
        Ramus L
        Condyle L
    Auditory ossicles
        Stapes R
        Incus R
        Malleus R
        Stapes L
        Incus L
        Malleus L
    Cricoid cartilage
    Thyroid
    Hyoid
    TMJ R
    TMJ L

END;

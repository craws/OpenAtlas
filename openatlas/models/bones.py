from __future__ import annotations

from typing import Any

from openatlas.database.tools import remove_bone_preservation_type
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def create_bones(super_: Entity, name: str, category: dict[str, Any]):
    add_bone(super_, name, category)


def get_bones(entity: Entity) -> dict[str, Any]:
    inventory = bone_inventory
    for sub in entity.get_linked_entities('P46'):
        if sub.name in bone_inventory.keys():
            if type_ := sub.get_linked_entity('P2'):
                inventory[sub.name]['data'] = type_.name
    return inventory


def add_bone(
        super_: Entity,
        name: str,
        category: dict[str, Any]):
    bone = False
    for sub in super_.get_linked_entities('P46'):
        if sub.name == name:
            bone = sub
            break
    if not bone:
        bone = Entity.insert('bone', name)
        bone.link('P46', super_, inverse=True)
    else:
        remove_bone_preservation_type(
            bone.id,
            Type.get_hierarchy('Bone preservation').subs)
    if 'data' in category and category['data']:
        bone.link('P2', Entity.get_by_id(int(category['data'])))
    if 'subs' in category:
        for name, sub in category['subs'].items():
            add_bone(bone, name, sub)


bone_inventory = {
    'Skull': {
        'preservation': 'percent',
        'subs': {
            'Frontal': {
                'preservation': 'percent',
                'subs': {
                    'Orbit R': {'preservation': 'percent'},
                    'Orbit L': {'preservation': 'percent'}}},
            'Parietal R': {'preservation': 'percent'},
            'Parietal L': {'preservation': 'percent'},
            'Temporal R': {
                'preservation': 'percent',
                'subs': {
                    'Squama R': {'preservation': 'percent'},
                    'Petrous R': {'preservation': 'percent'},
                    'Mastoid R': {'preservation': 'percent'}}},
            'Temporal L': {
                'preservation': 'percent',
                'subs': {
                    'Squama L': {'preservation': 'percent'},
                    'Petrous L': {'preservation': 'percent'},
                    'Mastoid L': {'preservation': 'percent'}}},
            'Occipital': {
                'preservation': 'percent',
                'subs': {
                    'Pars squama': {'preservation': 'percent'},
                    'Pars lateralis R': {'preservation': 'percent'},
                    'Pars lateralis L': {'preservation': 'percent'},
                    'Pars basilaris R': {'preservation': 'percent'},
                    'Pars basilaris L': {'preservation': 'percent'}}},
            'Sphenoid': {
                'preservation': 'percent',
                'subs': {
                    'Ala major R': {'preservation': 'percent'},
                    'Ala minor R': {'preservation': 'percent'},
                    'Ala major L': {'preservation': 'percent'},
                    'Ala minor L': {'preservation': 'percent'},
                    'Sphenoid body': {'preservation': 'percent'}}},
            'Maxilla R': {'preservation': 'percent'},
            'Maxilla L': {'preservation': 'percent'},
            'Nasal R': {'preservation': 'percent'},
            'Nasal L': {'preservation': 'percent'},
            'Lacrimale R': {'preservation': 'percent'},
            'Lacrimale L': {'preservation': 'percent'},
            'Ethmoid': {'preservation': 'percent'},
            'Zygomatic R': {'preservation': 'percent'},
            'Zygomatic L': {'preservation': 'percent'},
            'Vomer': {'preservation': 'percent'},
            'Palate R': {'preservation': 'percent'},
            'Palate L': {'preservation': 'percent'},
            'Inferior conchae R': {'preservation': 'percent'},
            'Inferior conchae L': {'preservation': 'percent'},
            'Mandible R': {
                'preservation': 'percent',
                'subs': {
                    'Ramus R': {'preservation': 'percent'},
                    'Condyle R': {'preservation': 'percent'}}},
            'Mandible L': {
                'preservation': 'percent',
                'subs': {
                    'Ramus L': {'preservation': 'percent'},
                    'Condyle L': {'preservation': 'percent'}}},
            'Auditory ossicles': {
                'preservation': None,
                'subs': {
                    'Stapes R': {'preservation': 'percent'},
                    'Incus R': {'preservation': 'percent'},
                    'Malleus R': {'preservation': 'percent'},
                    'Stapes L': {'preservation': 'percent'},
                    'Incus L': {'preservation': 'percent'},
                    'Malleus L': {'preservation': 'percent'}}},
            'Cricoid cartilage': {'preservation': 'percent'},
            'Thyroid': {'preservation': 'percent'},
            'Hyoid': {'preservation': 'percent'},
            'TMJ R': {'preservation': 'percent'},
            'TMJ L': {'preservation': 'percent'}}},
    'Dentition': {
        'preservation': 'percent',
        'subs': {
            'Permanent teeth': {
                'preservation': None,
                'subs': {
                    'Maxilla': {
                        'preservation': None,
                        'subs': {
                            'Right side': {
                                'preservation': None,
                                'subs': {
                                    'I1 R (11)': {'preservation': 'percent'},
                                    'I2 R (12)': {'preservation': 'percent'},
                                    'C R (13)': {'preservation': 'percent'},
                                    'PM1 R (14)': {'preservation': 'percent'},
                                    'PM2 R (15)': {'preservation': 'percent'},
                                    'M1 R (16)': {'preservation': 'percent'},
                                    'M2 R (17)': {'preservation': 'percent'},
                                    'M3 R (18)': {'preservation': 'percent'}}},
                            'Left side': {
                                'preservation': None,
                                'subs': {
                                    'I1 L (21)': {'preservation': 'percent'},
                                    'I2 L (22)': {'preservation': 'percent'},
                                    'C L (23)': {'preservation': 'percent'},
                                    'PM1 L (24)': {'preservation': 'percent'},
                                    'PM2 L (25)': {'preservation': 'percent'},
                                    'M1 L (26)': {'preservation': 'percent'},
                                    'M2 L (27)': {'preservation': 'percent'},
                                    'M3 L (28)': {'preservation': 'percent'}}}
                        }},
                    'Mandible': {
                        'preservation': None,
                        'subs': {
                            'Left side': {
                                'preservation': None,
                                'subs': {
                                    'I1 L (31)': {'preservation': 'percent'},
                                    'I2 L (32)': {'preservation': 'percent'},
                                    'C L (33)': {'preservation': 'percent'},
                                    'PM1 L (34)': {'preservation': 'percent'},
                                    'PM2 L (35)': {'preservation': 'percent'},
                                    'M1 L (36)': {'preservation': 'percent'},
                                    'M2 L (37)': {'preservation': 'percent'},
                                    'M3 L (38)': {'preservation': 'percent'}}},
                            'Right side': {
                                'preservation': None,
                                'subs': {
                                    'I1 R (41)': {'preservation': 'percent'},
                                    'I2 R (42)': {'preservation': 'percent'},
                                    'C R (43)': {'preservation': 'percent'},
                                    'PM1 R (44)': {'preservation': 'percent'},
                                    'PM2 R (45)': {'preservation': 'percent'},
                                    'M1 R (46)': {'preservation': 'percent'},
                                    'M2 R (47)': {'preservation': 'percent'},
                                    'M3 R (48)': {'preservation': 'percent'}}}
                        }}}},
            'Deciduous': {
                'preservation': None,
                'subs': {
                    'Maxilla': {
                        'preservation': None,
                        'subs': {
                            'Right side': {
                                'preservation': None,
                                'subs': {
                                    'I1 R (51)': {'preservation': 'percent'},
                                    'I2 R (52)': {'preservation': 'percent'},
                                    'C R (53)': {'preservation': 'percent'},
                                    'M1 R (54)': {'preservation': 'percent'},
                                    'M2 R (55)': {'preservation': 'percent'}}},
                            'Left side': {
                                'preservation': None,
                                'subs': {
                                    'I1 L (61)': {'preservation': 'percent'},
                                    'I2 L (62)': {'preservation': 'percent'},
                                    'C L (63)': {'preservation': 'percent'},
                                    'M1 L (64)': {'preservation': 'percent'},
                                    'M2 L (65)': {'preservation': 'percent'}}}
                        }},
                    'Mandible': {
                        'preservation': None,
                        'subs': {
                            'Left side': {
                                'preservation': None,
                                'subs': {
                                    'I1 L (71)': {'preservation': 'percent'},
                                    'I2 L (72)': {'preservation': 'percent'},
                                    'C L (73)': {'preservation': 'percent'},
                                    'M1 L (74)': {'preservation': 'percent'},
                                    'M2 L (75)': {'preservation': 'percent'}}},
                            'Right side': {
                                'preservation': None,
                                'subs': {
                                    'I1 R (81)': {'preservation': 'percent'},
                                    'I2 R (82)': {'preservation': 'percent'},
                                    'C R (83)': {'preservation': 'percent'},
                                    'M1 R (84)': {'preservation': 'percent'},
                                    'M2 R (85)': {'preservation': 'percent'}}}
                        }}}}}},
    'Shoulder girdle': {
        'preservation': None,
        'subs': {
            'Clavicle R': {
                'preservation': 'percent',
                'subs': {
                    'Clavicula med. Epiphysis R': {'preservation': 'percent'},
                    'Clavicula med. third R': {'preservation': 'percent'},
                    'Clavicula mid. third R': {'preservation': 'percent'},
                    'Clavicula lat. third R': {'preservation': 'percent'},
                    'Clavicula lat. Epiphysis R': {'preservation': 'percent'}}
            },
            'Clavicle L': {
                'preservation': 'percent',
                'subs': {
                    'Clavicula med. Epiphysis L': {'preservation': 'percent'},
                    'Clavicula med. third L': {'preservation': 'percent'},
                    'Clavicula mid. third L': {'preservation': 'percent'},
                    'Clavicula lat. third L': {'preservation': 'percent'},
                    'Clavicula lat. Epiphysis L': {'preservation': 'percent'}}
            },
            'Scapula R': {
                'preservation': 'percent',
                'subs': {
                    'Body R': {'preservation': 'percent'},
                    'Glenoid cavity R': {'preservation': 'percent'},
                    'Acromion process R': {'preservation': 'percent'},
                    'Coracoid process R': {'preservation': 'percent'}}},
            'Scapula L': {
                'preservation': 'percent',
                'subs': {
                    'Body L': {'preservation': 'percent'},
                    'Glenoid cavity L': {'preservation': 'percent'},
                    'Acromion process L': {'preservation': 'percent'},
                    'Coracoid process L': {'preservation': 'percent'}}}}},
    'Arms and hands': {
        'preservation': None,
        'subs': {
            'Arm R': {
                'preservation': 'percent',
                'subs': {
                    'Humerus R': {
                        'preservation': 'percent',
                        'subs': {
                            'Humerus - proximal epiphysis R':
                                {'preservation': 'percent'},
                            'Humerus - proximal third R':
                                {'preservation': 'percent'},
                            'Humerus - middle third R':
                                {'preservation': 'percent'},
                            'Humerus - distal third R':
                                {'preservation': 'percent'},
                            'Humerus - distal epiphysis R':
                                {'preservation': 'percent'},
                            'Glenohumeral R': {'preservation': 'percent'},
                            'Capitulum R': {'preservation': 'percent'},
                            'Trochlea R': {'preservation': 'percent'}}},
                    'Ulna R': {
                        'preservation': 'percent',
                        'subs': {
                            'Ulna - proximal epiphysis R':
                                {'preservation': 'percent'},
                            'Ulna - proximal third R':
                                {'preservation': 'percent'},
                            'Ulna - middle third R':
                                {'preservation': 'percent'},
                            'Ulna - distal third R':
                                {'preservation': 'percent'},
                            'Ulna - distal epiphysis R':
                                {'preservation': 'percent'},
                            'Trochlear notch R':
                                {'preservation': 'percent'},
                            'Radial notch R':
                                {'preservation': 'percent'},
                            'Ulna distal radioulnar R':
                                {'preservation': 'percent'}}},
                    'Radius R': {
                        'preservation': 'percent',
                        'subs': {
                            'Radius - proximal epiphysis R':
                                {'preservation': 'percent'},
                            'Radius - proximal third R':
                                {'preservation': 'percent'},
                            'Radius - middle third R':
                                {'preservation': 'percent'},
                            'Radius - distal third R':
                                {'preservation': 'percent'},
                            'Radius - distal epiphysis R':
                                {'preservation': 'percent'},
                            'Articular fovea R':
                                {'preservation': 'percent'},
                            'Circumferentia art. R':
                                {'preservation': 'percent'},
                            'Radius distal Radioulnar R':
                                {'preservation': 'percent'},
                            'Scaphoid lat. R': {'preservation': 'percent'},
                            'Lunate mes. R': {'preservation': 'percent'}}}}},
            'Arm L': {
                'preservation': 'percent',
                'subs': {
                    'Humerus L': {
                        'preservation': 'percent',
                        'subs': {
                            'Humerus - proximal epiphysis L':
                                {'preservation': 'percent'},
                            'Humerus - proximal third L':
                                {'preservation': 'percent'},
                            'Humerus - middle third L':
                                {'preservation': 'percent'},
                            'Humerus - distal third L':
                                {'preservation': 'percent'},
                            'Humerus - distal epiphysis L':
                                {'preservation': 'percent'},
                            'Glenohumeral L': {'preservation': 'percent'},
                            'Capitulum L': {'preservation': 'percent'},
                            'Trochlea L': {'preservation': 'percent'}}},
                    'Ulna L': {
                        'preservation': 'percent',
                        'subs': {
                            'Ulna - proximal epiphysis L':
                                {'preservation': 'percent'},
                            'Ulna - proximal third L':
                                {'preservation': 'percent'},
                            'Ulna - middle third L':
                                {'preservation': 'percent'},
                            'Ulna - distal third L':
                                {'preservation': 'percent'},
                            'Ulna - distal epiphysis L':
                                {'preservation': 'percent'},
                            'Trochlear notch L':
                                {'preservation': 'percent'},
                            'Radial notch L':
                                {'preservation': 'percent'},
                            'Ulna distal radioulnar L':
                                {'preservation': 'percent'}}},
                    'Radius L': {
                        'preservation': 'percent',
                        'subs': {
                            'Radius - proximal epiphysis L':
                                {'preservation': 'percent'},
                            'Radius - proximal third L':
                                {'preservation': 'percent'},
                            'Radius - middle third L':
                                {'preservation': 'percent'},
                            'Radius - distal third L':
                                {'preservation': 'percent'},
                            'Radius - distal epiphysis L':
                                {'preservation': 'percent'},
                            'Articular fovea L':
                                {'preservation': 'percent'},
                            'Circumferentia art. L':
                                {'preservation': 'percent'},
                            'Radius distal Radioulnar L':
                                {'preservation': 'percent'},
                            'Scaphoid lat. L': {'preservation': 'percent'},
                            'Lunate mes. L': {'preservation': 'percent'}}}}},
            'Hand R': {
                'preservation': 'percent',
                'subs': {
                    'Carpals R': {
                        'preservation': None,
                        'subs': {
                            'Scaphoid R': {'preservation': 'percent'},
                            'Lunate R': {'preservation': 'percent'},
                            'Triquetrum R': {'preservation': 'percent'},
                            'Capitulum R': {'preservation': 'percent'},
                            'Hamatum R': {'preservation': 'percent'},
                            'Trapezoideum R': {'preservation': 'percent'},
                            'Trapezium R': {'preservation': 'percent'},
                            'Pisiforme R': {'preservation': 'percent'}}},
                    'Metacarpals R': {
                        'preservation': None,
                        'subs': {
                            'Metacarpal 1 R': {'preservation': 'percent'},
                            'Metacarpal 2 R': {'preservation': 'percent'},
                            'Metacarpal 3 R': {'preservation': 'percent'},
                            'Metacarpal 4 R': {'preservation': 'percent'},
                            'Metacarpal 5 R': {'preservation': 'percent'}}},
                    'Phalanges R': {
                        'preservation': 'percent',
                        'subs': {
                            'Proximal phalanges R': {'preservation': 'number'},
                            'Medial phalanges R': {'preservation': 'number'},
                            'Distal phalanges R': {'preservation': 'number'},
                            'Sesamoid R': {'preservation': 'number'}}}}},
            'Hand L': {
                'preservation': 'percent',
                'subs': {
                    'Carpals L': {
                        'preservation': None,
                        'subs': {
                            'Scaphoid L': {'preservation': 'percent'},
                            'Lunate L': {'preservation': 'percent'},
                            'Triquetrum L': {'preservation': 'percent'},
                            'Capitulum L': {'preservation': 'percent'},
                            'Hamatum L': {'preservation': 'percent'},
                            'Trapezoideum L': {'preservation': 'percent'},
                            'Trapezium L': {'preservation': 'percent'},
                            'Pisiforme L': {'preservation': 'percent'}}},
                    'Metacarpals R': {
                        'preservation': None,
                        'subs': {
                            'Metacarpal 1 L': {'preservation': 'percent'},
                            'Metacarpal 2 L': {'preservation': 'percent'},
                            'Metacarpal 3 L': {'preservation': 'percent'},
                            'Metacarpal 4 L': {'preservation': 'percent'},
                            'Metacarpal 5 L': {'preservation': 'percent'}}},
                    'Phalanges R': {
                        'preservation': 'percent',
                        'subs': {
                            'Proximal phalanges L': {'preservation': 'number'},
                            'Medial phalanges L': {'preservation': 'number'},
                            'Distal phalanges L': {'preservation': 'number'},
                            'Sesamoid L': {'preservation': 'number'}}}}}}},
    'Axial skeleton': {
        'preservation': None,
        'subs': {
            'Sternum': {
                'preservation': 'percent',
                'subs': {
                    'Manubrium': {'preservation': 'percent'},
                    'Xiphoid process': {'preservation': 'percent'},
                    'Body': {'preservation': 'percent'}}},
            'Ribs': {
                'preservation': 'percent',
                'subs': {
                    'Right side': {
                        'preservation': None,
                        'subs': {
                            'First rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'First rib R head': {
                                        'preservation': 'percent'},
                                    'First rib R mid.': {
                                        'preservation': 'percent'},
                                    'First rib R stern.': {
                                        'preservation': 'percent'}}},
                            'Second rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'Second rib R head': {
                                        'preservation': 'percent'},
                                    'Second rib R mid.': {
                                        'preservation': 'percent'},
                                    'Second rib R stern.': {
                                        'preservation': 'percent'}}},
                            'Third to tenth rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'Third to tenth rib R head': {
                                        'preservation': 'number'},
                                    'Third to tenth rib R mid.': {
                                        'preservation': 'number'},
                                    'Third to tenth rib R stern.': {
                                        'preservation': 'number'}}},
                            'Eleventh rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'Eleventh rib R head': {
                                        'preservation': 'percent'},
                                    'Eleventh rib R mid.': {
                                        'preservation': 'percent'},
                                    'Eleventh rib R stern.': {
                                        'preservation': 'percent'}}},
                            'Twelfth rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'Twelfth rib R head': {
                                        'preservation': 'percent'},
                                    'Twelfth rib R mid.': {
                                        'preservation': 'percent'},
                                    'Twelfth rib R stern.': {
                                        'preservation': 'percent'}}}}},
                    'Left side': {
                        'preservation': None,
                        'subs': {
                            'First rib L': {
                                'preservation': 'percent',
                                'subs': {
                                    'First rib L head': {
                                        'preservation': 'percent'},
                                    'First rib L mid.': {
                                        'preservation': 'percent'},
                                    'First rib L stern.': {
                                        'preservation': 'percent'}}},
                            'Second rib L': {
                                'preservation': 'percent',
                                'subs': {
                                    'Second rib L head': {
                                        'preservation': 'percent'},
                                    'Second rib L mid.': {
                                        'preservation': 'percent'},
                                    'Second rib L stern.': {
                                        'preservation': 'percent'}}},
                            'Third to tenth rib L': {
                                'preservation': 'percent',
                                'subs': {
                                    'Third to tenth rib L head': {
                                        'preservation': 'number'},
                                    'Third to tenth rib L mid.': {
                                        'preservation': 'number'},
                                    'Third to tenth rib L stern.': {
                                        'preservation': 'number'}}},
                            'Eleventh rib L': {
                                'preservation': 'percent',
                                'subs': {
                                    'Eleventh rib L head': {
                                        'preservation': 'percent'},
                                    'Eleventh rib L mid.': {
                                        'preservation': 'percent'},
                                    'Eleventh rib L stern.': {
                                        'preservation': 'percent'}}},
                            'Twelfth rib R': {
                                'preservation': 'percent',
                                'subs': {
                                    'Twelfth rib L head': {
                                        'preservation': 'percent'},
                                    'Twelfth rib L mid.': {
                                        'preservation': 'percent'},
                                    'Twelfth rib L stern.': {
                                        'preservation': 'percent'}}}}}}},
            'Vertebral column': {
                    'preservation': 'percent',
                    'subs': {
                        'Cervical vertebrae': {
                            'preservation': None,
                            'subs': {
                                'C01 (Atlas)': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C01 Body': {
                                            'preservation': 'percent'},
                                        'C01 Arch R': {
                                            'preservation': 'percent'},
                                        'C01 Arch L': {
                                            'preservation': 'percent'}}},
                                'C02 (Atlas)': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C02 Body': {
                                            'preservation': 'percent'},
                                        'C02 Arch R': {
                                            'preservation': 'percent'},
                                        'C02 Arch L': {
                                            'preservation': 'percent'}}},
                                'C03': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C03 Body': {
                                            'preservation': 'percent'},
                                        'C03 Arch R': {
                                            'preservation': 'percent'},
                                        'C03 Arch L': {
                                            'preservation': 'percent'}}},
                                'C04': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C04 Body': {
                                            'preservation': 'percent'},
                                        'C04 Arch R': {
                                            'preservation': 'percent'},
                                        'C04 Arch L': {
                                            'preservation': 'percent'}}},
                                'C05': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C05 Body': {
                                            'preservation': 'percent'},
                                        'C05 Arch R': {
                                            'preservation': 'percent'},
                                        'C05 Arch L': {
                                            'preservation': 'percent'}}},
                                'C06': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C06 Body': {
                                            'preservation': 'percent'},
                                        'C06 Arch R': {
                                            'preservation': 'percent'},
                                        'C06 Arch L': {
                                            'preservation': 'percent'}}},
                                'C07': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'C07 Body': {
                                            'preservation': 'percent'},
                                        'C07 Arch R': {
                                            'preservation': 'percent'},
                                        'C07 Arch L': {
                                            'preservation': 'percent'}}}}},
                        'Thoracic vertebrae': {
                            'preservation': None,
                                'subs': {
                                    'Th01': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th01 Body': {
                                                'preservation': 'percent'},
                                            'Th01 Arch R': {
                                                'preservation': 'percent'},
                                            'Th01 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th02': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th02 Body': {
                                                'preservation': 'percent'},
                                            'Th02 Arch R': {
                                                'preservation': 'percent'},
                                            'Th02 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th03': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th03 Body': {
                                                'preservation': 'percent'},
                                            'Th03 Arch R': {
                                                'preservation': 'percent'},
                                            'Th03 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th04': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th04 Body': {
                                                'preservation': 'percent'},
                                            'Th04 Arch R': {
                                                'preservation': 'percent'},
                                            'Th04 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th05': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th05 Body': {
                                                'preservation': 'percent'},
                                            'Th05 Arch R': {
                                                'preservation': 'percent'},
                                            'Th05 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th06': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th06 Body': {
                                                'preservation': 'percent'},
                                            'Th06 Arch R': {
                                                'preservation': 'percent'},
                                            'Th06 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th07': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th07 Body': {
                                                'preservation': 'percent'},
                                            'Th07 Arch R': {
                                                'preservation': 'percent'},
                                            'Th07 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th08': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th08 Body': {
                                                'preservation': 'percent'},
                                            'Th08 Arch R': {
                                                'preservation': 'percent'},
                                            'Th08 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th09': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th09 Body': {
                                                'preservation': 'percent'},
                                            'Th09 Arch R': {
                                                'preservation': 'percent'},
                                            'Th09 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th10': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th10 Body': {
                                                'preservation': 'percent'},
                                            'Th10 Arch R': {
                                                'preservation': 'percent'},
                                            'Th10 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th11': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th11 Body': {
                                                'preservation': 'percent'},
                                            'Th11 Arch R': {
                                                'preservation': 'percent'},
                                            'Th11 Arch L': {
                                                'preservation': 'percent'}}},
                                    'Th12': {
                                        'preservation': 'percent',
                                        'subs': {
                                            'Th12 Body': {
                                                'preservation': 'percent'},
                                            'Th12 Arch R': {
                                                'preservation': 'percent'},
                                            'Th12 Arch L': {
                                                'preservation': 'percent'}}}}},
                        'Lumbar vertebrae': {
                            'preservation': None,
                            'subs': {
                                'L01': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'L01 Body': {
                                            'preservation': 'percent'},
                                        'L01 Arch R': {
                                            'preservation': 'percent'},
                                        'L01 Arch L': {
                                            'preservation': 'percent'}}},
                                'L02': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'L02 Body': {
                                            'preservation': 'percent'},
                                        'L02 Arch R': {
                                            'preservation': 'percent'},
                                        'L02 Arch L': {
                                            'preservation': 'percent'}}},
                                'L03': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'L03 Body': {
                                            'preservation': 'percent'},
                                        'L03 Arch R': {
                                            'preservation': 'percent'},
                                        'L03 Arch L': {
                                            'preservation': 'percent'}}},
                                'L04': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'L04 Body': {
                                            'preservation': 'percent'},
                                        'L04 Arch R': {
                                            'preservation': 'percent'},
                                        'L04 Arch L': {
                                            'preservation': 'percent'}}},
                                'L05': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'L05 Body': {
                                            'preservation': 'percent'},
                                        'L05 Arch R': {
                                            'preservation': 'percent'},
                                        'L05 Arch L': {
                                            'preservation': 'percent'}}}}},
                        'Sacrum': {
                            'preservation': None,
                            'subs': {
                                'S01': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'S01 Body': {
                                            'preservation': 'percent'},
                                        'S01 Arch R': {
                                            'preservation': 'percent'},
                                        'S01 Arch L': {
                                            'preservation': 'percent'}}},
                                'S02': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'S02 Body': {
                                            'preservation': 'percent'},
                                        'S02 Arch R': {
                                            'preservation': 'percent'},
                                        'S02 Arch L': {
                                            'preservation': 'percent'}}},
                                'S03': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'S03 Body': {
                                            'preservation': 'percent'},
                                        'S03 Arch R': {
                                            'preservation': 'percent'},
                                        'S03 Arch L': {
                                            'preservation': 'percent'}}},
                                'S04': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'S04 Body': {
                                            'preservation': 'percent'},
                                        'S04 Arch R': {
                                            'preservation': 'percent'},
                                        'S04 Arch L': {
                                            'preservation': 'percent'}}},
                                'S05': {
                                    'preservation': 'percent',
                                    'subs': {
                                        'S05 Body': {
                                            'preservation': 'percent'},
                                        'S05 Arch R': {
                                            'preservation': 'percent'},
                                        'S05 Arch L': {
                                            'preservation': 'percent'}}}}},
                            'Coccyx': {'preservation': 'percent'}}}}},
    'Pelvis': {
        'preservation': None,
        'subs': {
            'Pelvis R': {
                'preservation': 'percent',
                'subs': {
                    'Ilium R': {'preservation': 'percent'},
                    'Ischium R': {'preservation': 'percent'},
                    'Pubis R': {'preservation': 'percent'},
                    'Auricular surface R': {'preservation': 'percent'},
                    'Acetabulum R': {'preservation': 'percent'}}},
            'Pelvis L': {
                'preservation': 'percent',
                'subs': {
                    'Ilium L': {'preservation': 'percent'},
                    'Ischium L': {'preservation': 'percent'},
                    'Pubis L': {'preservation': 'percent'},
                    'Auricular surface L': {'preservation': 'percent'},
                    'Acetabulum L': {'preservation': 'percent'}}}}},

    'Legs and Feet': {
        'preservation': None,
        'subs': {
            'Leg R': {
                'preservation': 'percent',
                'subs': {
                    'Femur R': {
                        'preservation': 'percent',
                        'subs': {
                            'Femur - proximal epiphysis R': {
                                'preservation': 'percent'},
                            'Femur - proximal third R': {
                                'preservation': 'percent'},
                            'Femur - middle third R': {
                                'preservation': 'percent'},
                            'Femur - distal third R': {
                                'preservation': 'percent'},
                            'Femur - distal epiphysis R': {
                                'preservation': 'percent'},
                            'Femur head R': {
                                'preservation': 'percent'},
                            'Femur Femoropatella R': {
                                'preservation': 'percent'},
                            'Femur medial femorotibial R': {
                                'preservation': 'percent'},
                            'Femur lateral femorotibial R': {
                                'preservation': 'percent'}}},
                    'Patella R': {
                        'preservation': 'percent',
                        'subs': {
                            'Patella Femoropatellar R': {
                                'preservation': 'percent'}}},
                    'Tibia R': {
                        'preservation': 'percent',
                        'subs': {
                            'Tibia - proximal epiphysis R': {
                                'preservation': 'percent'},
                            'Tibia - proximal third R': {
                                'preservation': 'percent'},
                            'Tibia - middle third R': {
                                'preservation': 'percent'},
                            'Tibia - distal third R': {
                                'preservation': 'percent'},
                            'Tibia - distal epiphysis R': {
                                'preservation': 'percent'},
                            'Tibia medial femorotibial R': {
                                'preservation': 'percent'},
                            'Tibia lateral femorotibial R': {
                                'preservation': 'percent'},
                            'Tibia proximal tibiofibular R': {
                                'preservation': 'percent'},
                            'Tibia talocrural R': {
                                'preservation': 'percent'}}},
                    'Fibula R': {
                        'preservation': 'percent',
                        'subs': {
                            'Fibula - proximal epiphysis R': {
                                'preservation': 'percent'},
                            'Fibula - proximal third R': {
                                'preservation': 'percent'},
                            'Fibula - middle third R': {
                                'preservation': 'percent'},
                            'Fibula - distal third R': {
                                'preservation': 'percent'},
                            'Fibula - distal epiphysis R': {
                                'preservation': 'percent'},
                            'Fibula prox. Tibiofibular R': {
                                'preservation': 'percent'},
                            'Fibula talofibular R': {
                                'preservation': 'percent'}}}}},
            'Leg L': {
                'preservation': 'percent',
                'subs': {
                    'Femur L': {
                        'preservation': 'percent',
                        'subs': {
                            'Femur - proximal epiphysis L': {
                                'preservation': 'percent'},
                            'Femur - proximal third L': {
                                'preservation': 'percent'},
                            'Femur - middle third L': {
                                'preservation': 'percent'},
                            'Femur - distal third L': {
                                'preservation': 'percent'},
                            'Femur - distal epiphysis L': {
                                'preservation': 'percent'},
                            'Femur head L': {
                                'preservation': 'percent'},
                            'Femur Femoropatella L': {
                                'preservation': 'percent'},
                            'Femur medial femorotibial L': {
                                'preservation': 'percent'},
                            'Femur lateral femorotibial L': {
                                'preservation': 'percent'}}},
                    'Patella L': {
                        'preservation': 'percent',
                        'subs': {
                            'Patella Femoropatellar L': {
                                'preservation': 'percent'}}},
                    'Tibia L': {
                        'preservation': 'percent',
                        'subs': {
                            'Tibia - proximal epiphysis L': {
                                'preservation': 'percent'},
                            'Tibia - proximal third L': {
                                'preservation': 'percent'},
                            'Tibia - middle third L': {
                                'preservation': 'percent'},
                            'Tibia - distal third L': {
                                'preservation': 'percent'},
                            'Tibia - distal epiphysis L': {
                                'preservation': 'percent'},
                            'Tibia medial femorotibial L': {
                                'preservation': 'percent'},
                            'Tibia lateral femorotibial L': {
                                'preservation': 'percent'},
                            'Tibia proximal tibiofibular L': {
                                'preservation': 'percent'},
                            'Tibia talocrural L': {
                                'preservation': 'percent'}}},
                    'Fibula L': {
                        'preservation': 'percent',
                        'subs': {
                            'Fibula - proximal epiphysis L': {
                                'preservation': 'percent'},
                            'Fibula - proximal third L': {
                                'preservation': 'percent'},
                            'Fibula - middle third L': {
                                'preservation': 'percent'},
                            'Fibula - distal third L': {
                                'preservation': 'percent'},
                            'Fibula - distal epiphysis L': {
                                'preservation': 'percent'},
                            'Fibula prox. Tibiofibular L': {
                                'preservation': 'percent'},
                            'Fibula talofibular L': {
                                'preservation': 'percent'}}}}},
            'Foot R': {
                'preservation': 'percent',
                'subs': {
                    'Tarsals R': {
                        'preservation': None,
                        'subs': {
                            'Calcaneus R': {'preservation': 'percent'},
                            'Talus R': {'preservation': 'percent'},
                            'Navicular R': {'preservation': 'percent'},
                            'Cuboid R': {'preservation': 'percent'},
                            'Medial cuneiform R': {'preservation': 'percent'},
                            'Intermediate cuneiform R': {
                                'preservation': 'percent'},
                            'Lateral cuneiform R': {'preservation': 'percent'}
                        }},
                    'Metatarsals R': {
                        'preservation': None,
                        'subs': {
                            'Metatarsal 1 R': {'preservation': 'percent'},
                            'Metatarsal 2 R': {'preservation': 'percent'},
                            'Metatarsal 3 R': {'preservation': 'percent'},
                            'Metatarsal 4 R': {'preservation': 'percent'},
                            'Metatarsal 5 R': {'preservation': 'percent'}}},
                    'Phalanges R': {
                        'preservation': 'percent',
                        'subs': {
                            'Prox. Phalang.': {'preservation': 'number'},
                            'Mid. Phalang. R': {'preservation': 'number'},
                            'Distal Phalang. R': {'preservation': 'number'},
                            'Sesamoid R': {'preservation': 'number'}}}}},
            'Foot L': {
                'preservation': 'percent',
                'subs': {
                    'Tarsals L': {
                        'preservation': None,
                        'subs': {
                            'Calcaneus L': {'preservation': 'percent'},
                            'Talus L': {'preservation': 'percent'},
                            'Navicular L': {'preservation': 'percent'},
                            'Cuboid L': {'preservation': 'percent'},
                            'Medial cuneiform L': {'preservation': 'percent'},
                            'Intermediate cuneiform L': {
                                'preservation': 'percent'},
                            'Lateral cuneiform L': {'preservation': 'percent'}
                        }},
                    'Metatarsals L': {
                        'preservation': None,
                        'subs': {
                            'Metatarsal 1 L': {'preservation': 'percent'},
                            'Metatarsal 2 L': {'preservation': 'percent'},
                            'Metatarsal 3 L': {'preservation': 'percent'},
                            'Metatarsal 4 L': {'preservation': 'percent'},
                            'Metatarsal 5 L': {'preservation': 'percent'}}},
                    'Phalanges L': {
                        'preservation': 'percent',
                        'subs': {
                            'Prox. Phalang.': {'preservation': 'number'},
                            'Mid. Phalang. L': {'preservation': 'number'},
                            'Distal Phalang. L': {'preservation': 'number'},
                            'Sesamoid L': {'preservation': 'number'}}}}}}}}

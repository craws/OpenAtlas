from __future__ import annotations

structure = {
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
                            'Sesamoid L': {'preservation': 'number'}}}}},

}}}
"""

Axial skeleton

    Sternum
        Manubrium
        Body
        Xiphoid process
    Ribs
        Right side
            First rib R
                First rib R head
                First rib R mid.
                First rib R stern.
            Second rib R
                Second rib R head
                Second rib R Mid.
                Second rib R Stern.
            Third to tenth rib R
                Third to tenth rib R head (no)
                Third to tenth rib R mid. (no)
                Third to tenth rib R stern. (no)
            Eleventh rib R
                Eleventh rib R head
                Eleventh rib R mid.
                Eleventh rib R stern.
            Twelfth rib R
                Twelfth rib R head
                Twelfth rib R mid.
                Twelfth rib R stern.
        Left side
            First rib L
                First rib L head
                First rib L mid.
                First rib L stern.
            Second rib L
                Second rib L head
                Second rib L Mid.
                Second rib L Stern.
            Third to tenth rib L
                Third to tenth rib L head (no)
                Third to tenth rib L mid. (no)
                Third to tenth rib L stern. (no)
            Eleventh rib L
                Eleventh rib L head
                Eleventh rib L mid.
                Eleventh rib L stern.
            Twelfth rib L
                Twelfth rib L head
                Twelfth rib L mid.
                Twelfth rib L stern.
    Vertebral column
        Cervical vertebrae
            C01 (Atlas)
                C01 Body
                C01 Arch R
                C01 Arch L
            C02 (Axis)
                C02 Body
                C02 Arch R
                C02 Arch L
            C03
                C03 Body
                C03 Arch R
                C03 Arch L
            C04
                C04 Body
                C04 Arch R
                C04 Arch L
            C05
                C05 Body
                C05 Arch R
                C05 Arch L
            C06
                C06 Body
                C06 Arch R
                C06 Arch L
            C07
                C07 Body
                C07 Arch R
                C07 Arch L
        Thoracic vertebrae
            Th01
                Th01 Body
                Th01 Arch R
                Th01 Arch L
            Th02
                Th02 Body
                Th02 Arch R
                Th02 Arch L
            Th03
                Th03 Body
                Th03 Arch R
                Th03 Arch L
            Th04
                Th04 Body
                Th04 Arch R
                Th04 Arch L
            Th05
                Th05 Body
                Th05 Arch R
                Th05 Arch L
            Th06
                Th06 Body
                Th06 Arch R
                Th06 Arch L
            Th07
                Th07 Body
                Th07 Arch R
                Th07 Arch L
            Th08
                Th08 Body
                Th08 Arch R
                Th08 Arch L
            Th09
                Th09 Body
                Th09 Arch R
                Th09 Arch L
            Th10
                Th10 Body
                Th10 Arch R
                Th10 Arch L
            Th11
                Th11 Body
                Th11 Arch R
                Th11 Arch
            Th12
                Th12 Body
                Th12 Arch R
                Th12 Arch L
        Lumbar vertebrae
            L01
                L01 body
                L01 Arch R
                L01 Arch L
            L02
                L02 body
                L02 Arch R
                L02 Arch L
            L03
                L03 body
                L03 Arch R
                L03 Arch L
            L04
                L04 body
                L04 Arch R
                L04 Arch L
            L05
                L05 body
                L05 Arch R
                L05 Arch L
        Sacrum
            S01
                S01 body
                S01 Arch R
                S01 Arch L
            S02
                S02 body
                S02 Arch R
                S02 Arch L
            S03
                S03 body
                S03 Arch R
                S03 Arch L
            S04
                S04 body
                S04 Arch R
                S04 Arch L
            S05
                S05 body
                S05 Arch R
                S05 Arch L
        Coccyx

Pelvis

    Pelvis R
        Ilium R
        Ischium R
        Pubis R
        Auricular surface R
        Acetabulum R
    Pelvis L
        Ilium L
        Ischium L
        Pubis L
        Auricular surface L
        Acetabulum L

Legs and Feet

    Leg R
        Femur R
            Femur - proximal epiphysis R
            Femur - proximal third R
            Femur - middle third R
            Femur - distal third R
            Femur - distal epiphysis R
            Femur head R
            Femur Femoropatella R
            Femur medial femorotibial R
            Femur lateral femorotibial R
        Patella R
            Patella Femoropatellar R
        Tibia R
            Tibia - proximal epiphysis R
            Tibia - proximal third R
            Tibia - middle third R
            Tibia - distal third R
            Tibia - distal epiphysis R
            Tibia medial femorotibial R
            Tibia lateral femorotibial R
            Tibia proximal tibiofibular R
            Tibia talocrural R
        Fibula R
            Fibula - proximal epiphysis R
            Fibula - proximal third R
            Fibula - middle third R
            Fibula - distal third R
            Fibula - distal epiphysis R
            Fibula prox. Tibiofibular R
            Fibula talofibular R
    Leg L
        Femur L
            Femur - proximal epiphysis L
            Femur - proximal third L
            Femur - middle third L
            Femur - distal third L
            Femur - distal epiphysis L
            Femur head L
            Femur Femoropatella L
            Femur medial femorotibial L
            Femur lateral femorotibial L
        Patella L
            Patella Femoropatellar L
        Tibia L
            Tibia - proximal epiphysis L
            Tibia - proximal third L
            Tibia - middle third L
            Tibia - distal third L
            Tibia - distal epiphysis L
            Tibia medial femorotibial L
            Tibia lateral femorotibial L
            Tibia proximal tibiofibular L
            Tibia talocrural L
        Fibula left
            Fibula - proximal epiphysis L
            Fibula - proximal third L
            Fibula - middle third L
            Fibula - distal third L
            Fibula - distal epiphysis L
            Fibula prox. Tibiofibular L
            Fibula talofibular L
    Foot R
        Tarsals R
            Calcaneus R
            Talus R
            Navicular R
            Cuboid R
            Medial cuneiform R
            Intermediate cuneiform R
            Lateral cuneiform R
        Metatarsals R
            Metatarsal 1 R
            Metatarsal 2 R
            Metatarsal 3 R
            Metatarsal 4 R
            Metatarsal 5 R
        Phalanges R
            Prox. Phalang. R (no)
            Mid. Phalang. R (no)
            Distal Phalang. R (no)
            Sesamoid R (no.)
    Foot L
        Tarsals L
            Calcaneus L
            Talus L
            Navicular L
            Cuboid L
            Medial cuneiform L
            Intermediate cuneiform L
            Lateral cuneiform L
        Metatarsals L
            Metatarsal 1 L
            Metatarsal 2 L
            Metatarsal 3 L
            Metatarsal 4 L
            Metatarsal 5 L
        Phalanges L
            Prox. Phalang. L (no)
            Mid. Phalang. L (no)
            Distal Phalang. L (no)
            Sesamoid L (no.)
"""

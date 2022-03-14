from typing import Any, Dict, Union

from flask import g

from openatlas.database.anthropology import Anthropology
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type


class SexEstimation:

    options = {
        '': 0,
        'Female': -2,
        'Female?': -1,
        'Indifferent': 0,
        'Male?': 1,
        'Male': 2,
        'Not preserved': 0}

    features = {
        'Skull': {
            'Glabella': {
                'value': 3,
                'female': 'smooth, non-projecting',
                'male': 'prominent, projecting'},
            'Arcus superciliaris': {
                'value': 2,
                'female': 'slight',
                'male': 'prominent'},
            'Tuber frontalis and parietalis': {
                'value': 2,
                'female': 'marked',
                'male': 'reduced or absent'},
            'Inclinatio frontalis': {
                'value': 1,
                'female': 'vertical',
                'male': 'inclined posteriorly'},
            'Processus mastoideus': {
                'value': 3,
                'female': 'small, inflected below vault',
                'male': 'large, vertical or everted'},
            'Relief of planum nuchale': {
                'value': 3,
                'female': 'smooth',
                'male': 'ridged'},
            'Protuberantia occipitalis externa': {
                'value': 2,
                'female': 'small',
                'male': 'large'},
            'Processus zygomaticus': {
                'value': 3,
                'female': 'narrow',
                'male': 'broad'},
            'Os zygomaticum': {
                'value': 2,
                'female': 'short, smooth lower margin',
                'male': 'tall, roughened lower margin'},
            'Crista supramastoideum': {
                'value': 2,
                'female': 'short',
                'male': 'long, extending posteriorly'},
            'Margo supraorbitalis': {
                'value': 1,
                'female': 'sharp edges',
                'male': 'rounded edges'},
            'Shape of orbita': {
                'value': 1,
                'female': 'circular',
                'male': 'quadrangular'}},
        'Mandible': {
            'Overall apperence': {
                'value': 3,
                'female': 'grazil',
                'male': 'pronounced'},
            'Mentum': {
                'value': 2,
                'female': 'small and rounded',
                'male': 'large and projecting'},
            'Angulus': {
                'value': 1,
                'female': 'obtuse',
                'male': 'perpendicular'},
            'Margo inferior (M2)': {
                'value': 1,
                'female': 'thin',
                'male': 'thick'},
            'Angle': {
                'value': 1,
                'female': 'smooth edges',
                'male': 'everted edges'}},
        'Pelvis': {
            'Sulcus praeauricularis': {
                'value': 3,
                'female': 'often present',
                'male': 'absent'},
            'Incisura ischiadica major': {
                'value': 3,
                'female': 'u-shaped, obtuse angle (>60°)',
                'male': 'v-shaped, acute angle (~30°)'},
            'Angulus pubis': {
                'value': 2,
                'female': 'broad, u-shaped',
                'male': 'narrow, v-shaped'},
            'Arc composé': {
                'value': 2,
                'female': 'double curve',
                'male': 'single curve'},
            'Os coxae': {
                'value': 2,
                'female':
                    'low, broad, with spreading alae ossis illii and '
                    'low muscle relief',
                'male': 'high, narrow, with strong muscle relief'},
            'Foramen obturatum': {
                'value': 2,
                'female': 'small, wide, triangular',
                'male': 'large, tall ovoid'},
            'Corpus ossis ischii': {
                'value': 2,
                'female': 'narrow',
                'male': 'broad'},
            'Crista iliaca': {
                'value': 1,
                'female': 'flat s-shaped',
                'male': 'pronounced s-shaped'},
            'Fossa iliaca': {
                'value': 1,
                'female': 'small, broad',
                'male': 'tall, narrow'},
            'Pelvis major': {
                'value': 1,
                'female': 'broad',
                'male': 'narrow'},
            'Auricular area': {
                'value': 1,
                'female': 'narrow, on elevated plateau',
                'male': 'wide, in plane of iliac surface'},
            'Sacrum': {
                'value': 1,
                'female':
                    'sacral ala broader than body of S1, curvature ectends '
                    'from S3 to S5',
                'male':
                    'sacral ala narrower than S1, curvature ectends '
                    'from S1 to S5'},
            'Fossa acetabuli': {
                'value': 1,
                'female': 'small, faces antero-laterally',
                'male': 'large, faces more laterally'}},
        'Robusticity': {
            'Humerus': {
                'value': 1,
                'female': 'grazil',
                'male': 'pronounced'},
            'Femur': {
                'value': 1,
                'female': 'grazil',
                'male': 'pronounced'}}}

    @staticmethod
    def calculate(entity: Entity) -> Union[float, None]:
        types = Anthropology.get_types(entity.id)
        if not types:
            return None
        result = 0
        weight = 0

        # to do: remove code duplication from view
        for group_id in Type.get_types('Features for sexing'):
            group = g.types[group_id]
            for type_id in group.subs:
                type_ = g.types[type_id]
                SexEstimation.features[group.name][type_.name][
                    'type_id'] = type_.id

        for row in types:
            if row['description'] in ['', 'Not preserved']:
                continue
            name = g.types[row['id']].name
            feature = SexEstimation.get_by_name2(name)
            result += feature['value'] * SexEstimation.options[row['description']]
            weight += feature['value']
        if weight == 0:
            return None
        return round((result / weight), 2)

    @staticmethod
    def get_by_name2(feature_name):
        for group in SexEstimation.features.values():
            for name, values in group.items():
                if name == feature_name:
                    return values

    @staticmethod
    def get_by_name(feature_name):
        for group in SexEstimation.features.values():
            for name, values in group.items():
                if name == feature_name:
                    return values['type_id']

    @staticmethod
    def save(
            entity: Entity,
            data: Dict[str, str],
            types: [Dict[str, Any]]) -> None:
        for dict_ in types:
            Link.delete_(dict_['link_id'])
        for key, item in data.items():
            entity.link('P2', g.types[SexEstimation.get_by_name(key)], item)

    @staticmethod
    def get_types(entity: Entity) -> list[dict[str, Any]]:
        return Anthropology.get_types(entity.id)

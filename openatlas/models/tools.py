from __future__ import annotations

import json
from typing import Any, Optional, TYPE_CHECKING

from flask import g

from openatlas.database import tools as db

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity, Link


def get_sex_types(id_: int) -> list[dict[str, Any]]:
    return db.get_sex_types(id_)


def get_carbon_link(entity: Entity) -> Optional[Link]:
    for link_ in entity.get_links('P2'):
        if link_.range.name == 'Radiocarbon':
            return link_
    return None


def update_carbon(
        entity: Entity,
        data: dict[str, Any],
        link_: Optional[Link]) -> None:
    if link_:
        link_.description = json.dumps(data)
        link_.update()
    else:
        entity.link('P2', g.radiocarbon_type, json.dumps(data))


class SexEstimation:
    result = {
        'female': -0.7,         # -2  to -0.7
        'likely female': -0.3,  # -0,69 to -0.31
        'indifferent': 0.3,     # -0.3 to 0.3
        'likely male': 0.7,     # 0.31 to 0.69
        'male': 2}              # 0.7 to 2
    options = {
        '': 0,
        'Female': -2,
        'Female?': -1,
        'Indifferent': 0,
        'Male?': 1,
        'Male': 2,
        'Not preserved': 0}
    features: dict[str, dict[str, Any]] = {
        'Glabella': {
            'category': 'Skull',
            'value': 3,
            'female': 'smooth, non-projecting',
            'male': 'prominent, projecting'},
        'Arcus superciliaris': {
            'category': 'Skull',
            'value': 2,
            'female': 'slight',
            'male': 'prominent'},
        'Tuber frontalis and parietalis': {
            'category': 'Skull',
            'value': 2,
            'female': 'marked',
            'male': 'reduced or absent'},
        'Inclinatio frontalis': {
            'category': 'Skull',
            'value': 1,
            'female': 'vertical',
            'male': 'inclined posteriorly'},
        'Processus mastoideus': {
            'category': 'Skull',
            'value': 3,
            'female': 'small, inflected below vault',
            'male': 'large, vertical or everted'},
        'Relief of planum nuchale': {
            'category': 'Skull',
            'value': 3,
            'female': 'smooth',
            'male': 'ridged'},
        'Protuberantia occipitalis externa': {
            'category': 'Skull',
            'value': 2,
            'female': 'small',
            'male': 'large'},
        'Processus zygomaticus': {
            'category': 'Skull',
            'value': 3,
            'female': 'narrow',
            'male': 'broad'},
        'Os zygomaticum': {
            'category': 'Skull',
            'value': 2,
            'female': 'short, smooth lower margin',
            'male': 'tall, roughened lower margin'},
        'Crista supramastoideum': {
            'category': 'Skull',
            'value': 2,
            'female': 'short',
            'male': 'long, extending posteriorly'},
        'Margo supraorbitalis': {
            'category': 'Skull',
            'value': 1,
            'female': 'sharp edges',
            'male': 'rounded edges'},
        'Shape of orbita': {
            'category': 'Skull',
            'value': 1,
            'female': 'circular',
            'male': 'quadrangular'},
        'Overall apperence': {
            'category': 'Mandible',
            'value': 3,
            'female': 'grazil',
            'male': 'pronounced'},
        'Mentum': {
            'category': 'Mandible',
            'value': 2,
            'female': 'small and rounded',
            'male': 'large and projecting'},
        'Angulus': {
            'category': 'Mandible',
            'value': 1,
            'female': 'obtuse',
            'male': 'perpendicular'},
        'Margo inferior (M2)': {
            'category': 'Mandible',
            'value': 1,
            'female': 'thin',
            'male': 'thick'},
        'Angle': {
            'category': 'Mandible',
            'value': 1,
            'female': 'smooth edges',
            'male': 'everted edges'},
        'Sulcus praeauricularis': {
            'category': 'Pelvis',
            'value': 3,
            'female': 'often present',
            'male': 'absent'},
        'Incisura ischiadica major': {
            'category': 'Pelvis',
            'value': 3,
            'female': 'u-shaped, obtuse angle (>60°)',
            'male': 'v-shaped, acute angle (~30°)'},
        'Angulus pubis': {
            'category': 'Pelvis',
            'value': 2,
            'female': 'broad, u-shaped',
            'male': 'narrow, v-shaped'},
        'Arc composé': {
            'category': 'Pelvis',
            'value': 2,
            'female': 'double curve',
            'male': 'single curve'},
        'Os coxae': {
            'category': 'Pelvis',
            'value': 2,
            'female':
                'low, broad, with spreading alae ossis illii and '
                'low muscle relief',
            'male': 'high, narrow, with strong muscle relief'},
        'Foramen obturatum': {
            'category': 'Pelvis',
            'value': 2,
            'female': 'small, wide, triangular',
            'male': 'large, tall ovoid'},
        'Corpus ossis ischii': {
            'category': 'Pelvis',
            'value': 2,
            'female': 'narrow',
            'male': 'broad'},
        'Crista iliaca': {
            'category': 'Pelvis',
            'value': 1,
            'female': 'flat s-shaped',
            'male': 'pronounced s-shaped'},
        'Fossa iliaca': {
            'category': 'Pelvis',
            'value': 1,
            'female': 'small, broad',
            'male': 'tall, narrow'},
        'Pelvis major': {
            'category': 'Pelvis',
            'value': 1,
            'female': 'broad',
            'male': 'narrow'},
        'Auricular area': {
            'category': 'Pelvis',
            'value': 1,
            'female': 'narrow, on elevated plateau',
            'male': 'wide, in plane of iliac surface'},
        'Sacrum': {
            'category': 'Pelvis',
            'value': 1,
            'female':
                'sacral ala broader than body of S1, curvature ectends '
                'from S3 to S5',
            'male':
                'sacral ala narrower than S1, curvature ectends '
                'from S1 to S5'},
        'Fossa acetabuli': {
            'category': 'Pelvis',
            'value': 1,
            'female': 'small, faces antero-laterally',
            'male': 'large, faces more laterally'},
        'Humerus': {
            'category': 'Robusticity',
            'value': 1,
            'female': 'grazil',
            'male': 'pronounced'},
        'Femur': {
            'category': 'Robusticity',
            'value': 1,
            'female': 'grazil',
            'male': 'pronounced'}}

    @staticmethod
    def prepare_feature_types() -> None:
        for category_id in g.sex_type.subs:
            for id_ in g.types[category_id].subs:
                SexEstimation.features[g.types[id_].name]['id'] = \
                    g.types[id_].id

    @staticmethod
    def calculate(entity: Entity) -> Optional[float]:
        types = get_sex_types(entity.id)
        if not types:
            return None
        SexEstimation.prepare_feature_types()
        result = 0
        weight = 0
        for row in types:
            if row['description'] not in ['', 'Not preserved']:
                value = SexEstimation.features[
                    g.types[row['id']].name]['value']
                weight += value
                result += value * SexEstimation.options[row['description']]
        return None if weight == 0 else round(result / weight, 2)

    @staticmethod
    def save(
            entity: Entity,
            data: dict[str, str],
            types: list[dict[str, Any]]) -> None:
        from openatlas.models.entity import Link
        for dict_ in types:
            Link.delete_(dict_['link_id'])
        SexEstimation.prepare_feature_types()
        for name, item in data.items():
            entity.link(
                'P2',
                g.types[SexEstimation.features[name]['id']],
                item)

    @staticmethod
    def get_types(entity: Entity) -> list[dict[str, Any]]:
        return get_sex_types(entity.id)

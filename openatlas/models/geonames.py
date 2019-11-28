from typing import Optional

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.link import Link
from openatlas.models.node import NodeMapper


class GeonamesMapper:

    @staticmethod
    def get_geonames_link(object_: Entity) -> Optional[Link]:
        for link_ in object_.get_links('P67', inverse=True):
            if link_.domain.system_type == 'external reference geonames':
                return link_
        return None

    @staticmethod
    def update_geonames(form: FlaskForm, object_: Entity) -> None:
        new_geonames_id = form.geonames_id.data
        geonames_link = GeonamesMapper.get_geonames_link(object_)
        geonames_entity = geonames_link.domain if geonames_link else None

        if not new_geonames_id:
            if geonames_entity:
                if len(geonames_entity.get_links(['P67'])) > 1:  # pragma: no cover
                    if geonames_link:
                        geonames_link.delete()  # There are more linked so only remove this link
                else:
                    geonames_entity.delete()  # Nothing else is linked to the reference so delete it
            return

        # Get id of the match type
        match_id = None
        for node_id in NodeMapper.get_hierarchy_by_name('External Reference Match').subs:
            if g.nodes[node_id].name == 'exact match' and form.geonames_precision.data:
                match_id = node_id
                break
            if g.nodes[node_id].name == 'close match' and not form.geonames_precision.data:
                match_id = node_id
                break

        # There wasn't one linked before
        if not geonames_entity:
            reference = EntityMapper.get_by_name_and_system_type(new_geonames_id,
                                                                 'external reference geonames')
            if not reference:  # The selected reference doesn't exist so create it
                reference = EntityMapper.insert('E31', new_geonames_id,
                                                'external reference geonames',
                                                description='GeoNames ID')
            object_.link('P67', [reference], inverse=True, type_id=match_id)
            return

        if geonames_link and int(new_geonames_id) == int(geonames_entity.name) \
                and match_id == geonames_link.type.id:
            return  # It's the same link so do nothing

        # Only the match type change so delete and recreate the link
        if geonames_link and int(new_geonames_id) == int(geonames_entity.name):
            geonames_link.delete()
            object_.link('P67', geonames_entity, inverse=True, type_id=match_id)
            return

        # Its linked to a different geonames reference
        if geonames_link and len(geonames_entity.get_links(['P67'])) > 1:
            geonames_link.delete()  # There are more linked so only remove this link
        else:  # pragma: no cover
            geonames_entity.delete()  # Nothing else is linked to the reference so delete it
        reference = EntityMapper.get_by_name_and_system_type(new_geonames_id,
                                                             'external reference geonames')

        if not reference:  # The selected reference doesn't exist so create it
            reference = EntityMapper.insert('E31', new_geonames_id, 'external reference geonames',
                                            description='GeoNames ID')
        object_.link('P67', [reference], inverse=True, type_id=match_id)

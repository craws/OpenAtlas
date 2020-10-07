from typing import Optional

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node


class Geonames:

    @staticmethod
    def get_geonames_link(object_: Entity) -> Optional[Link]:
        for link_ in object_.get_links('P67', inverse=True):
            if link_.domain.system_type == 'external reference geonames':
                return link_
        return None

    @staticmethod
    def update_geonames(form: FlaskForm, object_: Entity) -> None:
        new_id = form.geonames_id.data
        link_ = Geonames.get_geonames_link(object_)
        reference = link_.domain if link_ else None  # former external reference

        if not new_id:
            if reference:
                if len(reference.get_links(['P67'])) > 1:  # pragma: no cover
                    if link_:
                        link_.delete()  # There are more linked so only remove this link
                else:
                    reference.delete()  # Nothing else is linked to the reference so delete it
            return

        # Get id of the match type
        match_id = None
        for node_id in Node.get_hierarchy('External Reference Match').subs:
            if g.nodes[node_id].name == 'exact match' and form.geonames_precision.data:
                match_id = node_id
                break
            if g.nodes[node_id].name == 'close match' and not form.geonames_precision.data:
                match_id = node_id
                break

        # There wasn't one linked before
        if not reference:
            reference = Entity.get_by_name_and_system_type(new_id, 'external reference geonames')
            if not reference:  # The selected reference doesn't exist so create it
                reference = Entity.insert('E31',
                                          new_id,
                                          'external reference geonames',
                                          description='GeoNames ID')
            object_.link('P67', reference, inverse=True, type_id=match_id)
            return

        if link_ and int(new_id) == int(reference.name) and match_id == link_.type.id:
            return  # It's the same link so do nothing

        # Only the match type changed so delete and recreate the link
        if link_ and int(new_id) == int(reference.name):
            link_.delete()
            object_.link('P67', reference, inverse=True, type_id=match_id)
            return

        # It's linked to a different geonames reference
        if link_ and len(reference.get_links(['P67'])) > 1:
            link_.delete()  # There are more linked so only remove this link
        else:  # pragma: no cover
            reference.delete()  # Nothing else is linked to the reference so delete it
        reference = Entity.get_by_name_and_system_type(new_id, 'external reference geonames')

        if not reference:  # The selected reference doesn't exist so create it
            reference = Entity.insert('E31',
                                      new_id,
                                      'external reference geonames',
                                      description='GeoNames ID')
        object_.link('P67', reference, inverse=True, type_id=match_id)

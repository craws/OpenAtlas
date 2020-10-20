from typing import Optional

from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.display import uc_first


class Reference:
    # Tools for external references like Wikidata or GeoNames

    @staticmethod
    def get_link(entity: Entity, name) -> Optional[Link]:
        for link_ in entity.get_links('P67', inverse=True):
            if link_.domain.system_type == 'external reference ' + name:
                return link_
        return None

    @staticmethod
    def update(form: FlaskForm, object_: Entity) -> None:
        for name in g.external:
            if not current_user.settings['module_' + name] or not hasattr(form, name + '_id'):
                continue
            new_id = getattr(form, name + '_id').data
            link_ = Reference.get_link(object_, name)
            reference = link_.domain if link_ else None  # former external reference

            if not new_id:
                if reference:
                    if len(reference.get_links(['P67'])) > 1:  # pragma: no cover
                        if link_:
                            link_.delete()  # There are more linked so only remove this link
                    else:
                        reference.delete()  # Nothing else is linked to the reference so delete it
                continue

            # Get id of the match type
            match_id = None
            for node_id in Node.get_hierarchy('External Reference Match').subs:
                match_name = g.nodes[node_id].name
                if match_name == 'exact match' and getattr(form, name + '_precision').data:
                    match_id = node_id
                    break
                if match_name == 'close match' and not getattr(form, name + '_precision').data:
                    match_id = node_id
                    break

            # There wasn't one linked before
            if not reference:
                reference = Entity.get_by_name_and_system_type(new_id, 'external reference ' + name)
                if not reference:  # The selected reference doesn't exist so create it
                    reference = Entity.insert('E31',
                                              new_id,
                                              'external reference ' + name,
                                              description=uc_first(name) + ' Id')
                object_.link('P67', reference, inverse=True, type_id=match_id)
                continue

            if link_ and str(new_id) == str(reference.name) and match_id == link_.type.id:
                continue  # It's the same link so do nothing

            # Only the match type changed so delete and recreate the link
            if link_ and str(new_id) == str(reference.name):
                link_.delete()
                object_.link('P67', reference, inverse=True, type_id=match_id)
                continue

            # It's linked to a different reference
            if link_ and len(reference.get_links(['P67'])) > 1:
                link_.delete()  # There are more linked so only remove this link
            else:  # pragma: no cover
                reference.delete()  # Nothing else is linked to the reference so delete it
            reference = Entity.get_by_name_and_system_type(new_id, 'external reference ' + name)

            if not reference:  # The selected reference doesn't exist so create it
                reference = Entity.insert('E31',
                                          new_id,
                                          'external reference ' + name,
                                          description=uc_first(name) + ' Id')
            object_.link('P67', reference, inverse=True, type_id=match_id)

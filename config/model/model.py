from typing import Any

from flask_babel import lazy_gettext as _

from config.model.classes import (
    actor, artifact, event, file, place, reference, reference_system, source,
    type)

# Todo: Needed for translation, to be removed after implemented
_('first')
_('last')
_('involvement')
_('type tools')
_('page')

model: dict[str, Any] = {
    'acquisition': event.acquisition,
    'activity': event.activity,
    'administrative_unit': type.administrative_unit,
    'appellation': {'attributes': {}},
    'artifact': artifact.artifact,
    'bibliography': reference.bibliography,
    'edition': reference.edition,
    'external_reference': reference.external_reference,
    'feature': place.feature,
    'file': file.file,
    'group': actor.group,
    'human_remains': artifact.human_remains,
    'modification': event.modification,
    'move': event.move,
    'object_location': {'label': _('object location'), 'attributes': {}},
    'person': actor.person,
    'place': place.place,
    'production': event.production,
    'reference_system': reference_system.reference_system,
    'source': source.source,
    'source_translation': source.source_translation,
    'stratigraphic_unit': place.stratigraphic_unit,
    'type': type.type_,
    'type_tools': {'attributes': {}}}


# Todo: re-implement root places shown at types, see former code below
# def add_tabs(self) -> None:
#     entity = self.entity
#     self.tabs['entities'] = Tab('entities', entity=entity)
#     if entity.category == 'value':
#         self.tabs['entities'].table.columns = \
#             [_('name'), _('value'), _('class'), _('info')]
#     classes_ = [
#         'feature',
#         'stratigraphic_unit',
#         'artifact',
#         'human_remains']
#     possible_sub_unit = False
#     if any(item in g.types[entity.root[0]].classes for item in classes_):
#         possible_sub_unit = True
#         self.tabs['entities'].table.columns.append('place')
#     root = g.types[entity.root[0]] if entity.root else entity
#     if root.name in app.config['PROPERTY_TYPES']:
#         self.tabs['entities'].table.columns = [_('domain'), _('range')]
#         for row in Link.get_links_by_type(entity):
#             self.tabs['entities'].table.rows.append([
#                 link(Entity.get_by_id(row['domain_id'])),
#                 link(Entity.get_by_id(row['range_id']))])
#     else:
#         entities = entity.get_linked_entities(
#             ['P2', 'P89'],
#             inverse=True,
#             types=True,
#             sort=True)
#         root_places = {}
#         if possible_sub_unit and entities:
#             root_places = Entity.get_roots(
#                 'P46',
#                 [e.id for e in entities],
#                 inverse=True)
#         for item in entities:
#             if item.class_.name == 'object_location':
#                 item = item.get_linked_entity_safe('P53', inverse=True)
#             data = [link(item)]
#             if entity.category == 'value':
#                 data.append(format_number(item.types[entity]))
#             data.append(item.class_.label)
#             data.append(item.description)
#             data.append(
#                 link(
#                     root_places[item.id]['name'],
#                     url_for('view', id_=root_places[item.id]['id']))
#                 if item.id in root_places else '')
#             self.tabs['entities'].table.rows.append(data)

# Todo: re-implement relations, see code below
# class ActorFunctionManager(BaseManager):
#     fields = ['date', 'description', 'continue']
#
#     def top_fields(self) -> dict[str, Any]:
#         if self.link_:
#             return {}
#         if 'membership' in request.url:
#             field_name = 'group'
#             entities = Entity.get_by_class('group', aliases=self.aliases)
#         else:
#             field_name = 'actor'
#             entities = Entity.get_by_class('actor', aliases=self.aliases)
#         return {
#             'member_origin_id': HiddenField(),
#             field_name:
#                 TableMultiField(
#                     entities,
#                     filter_ids=[self.origin.id],
#                     validators=[InputRequired()])}
#
#     def populate_insert(self) -> None:
#         self.form.member_origin_id.data = self.origin.id
#
#     def process_form(self) -> None:
#         link_type = self.get_link_type()
#         class_ = 'group' if hasattr(self.form, 'group') else 'actor'
#         for actor in Entity.get_by_ids(
#                 ast.literal_eval(getattr(self.form, class_).data)):
#             self.add_link(
#                 'P107',
#                 actor,
#                 self.form.description.data,
#                 inverse=(class_ == 'group'),
#                 type_id=link_type.id if link_type else None)
#
#     def process_link_form(self) -> None:
#         type_id = getattr(
#             self.form,
#             str(g.classes['actor_function'].standard_type_id)).data
#         self.link_.type = g.types[int(type_id)] if type_id else None
#
#
# class ActorRelationManager(BaseManager):
#     fields = ['date', 'description', 'continue']
#
#     def top_fields(self) -> dict[str, Any]:
#         fields = {}
#         if not self.link_:
#             fields['actor'] = TableMultiField(
#                 Entity.get_by_class('person', aliases=self.aliases),
#                 filter_ids=[self.origin.id],
#                 validators=[InputRequired()])
#             fields['relation_origin_id'] = HiddenField()
#         return fields
#
#     def additional_fields(self) -> dict[str, Any]:
#         return {'inverse': BooleanField(_('inverse'))}
#
#     def populate_insert(self) -> None:
#         self.form.relation_origin_id.data = self.origin.id
#
#     def process_form(self) -> None:
#         for actor in Entity.get_by_ids(
#                 ast.literal_eval(self.form.actor.data)):
#             link_type = self.get_link_type()
#             self.add_link(
#                 'OA7',
#                 actor,
#                 self.form.description.data,
#                 inverse=bool(self.form.inverse.data),
#                 type_id=link_type.id if link_type else None)
#
#     def process_link_form(self) -> None:
#         type_id = getattr(
#             self.form,
#             str(g.classes['actor_relation'].standard_type_id)).data
#         self.link_.type = g.types[int(type_id)] if type_id else None
#         inverse = self.form.inverse.data
#         if (self.origin.id == self.link_.domain.id and inverse) or \
#                 (self.origin.id == self.link_.range.id and not inverse):
#             new_range = self.link_.domain
#             self.link_.domain = self.link_.range
#             self.link_.range = new_range
#
#     def populate_update(self) -> None:
#         if self.origin.id == self.link_.range.id:
#             self.form.inverse.data = True
#
#
# class InvolvementManager(BaseManager):
#     fields = ['date', 'description', 'continue']
#
#     def top_fields(self) -> dict[str, Any]:
#         event_class_name = ''
#         if self.link_:
#             event_class_name = self.link_.domain.class_.name
#         elif self.origin and self.origin.class_.view != 'actor':
#             event_class_name = self.origin.class_.name
#         fields = {}
#         if self.insert and self.origin:
#           class_ = 'actor' if self.origin.class_.view == 'event' else 'event'
#             fields[class_] = TableMultiField(
#                 Entity.get_by_class(class_, True, self.aliases),
#                 validators=[InputRequired()])
#         choices = [('P11', g.properties['P11'].name)]
#         if event_class_name in [
#             'acquisition', 'activity', 'modification', 'production']:
#             choices.append(('P14', g.properties['P14'].name))
#             if event_class_name == 'acquisition':
#                 choices.append(('P22', g.properties['P22'].name))
#                 choices.append(('P23', g.properties['P23'].name))
#         fields['activity'] = SelectField(_('activity'), choices=choices)
#         return fields
#
#     def populate_update(self) -> None:
#         self.form.activity.data = self.link_.property.code
#
#     def process_form(self) -> None:
#         if self.origin.class_.view == 'event':
#            actors = Entity.get_by_ids(ast.literal_eval(self.form.actor.data))
#             for actor in actors:
#                 link_type = self.get_link_type()
#                 self.add_link(
#                     self.form.activity.data,
#                     actor,
#                     self.form.description.data,
#                     type_id=link_type.id if link_type else None)
#         else:
#            events = Entity.get_by_ids(ast.literal_eval(self.form.event.data))
#             for event in events:
#                 link_type = self.get_link_type()
#                 self.add_link(
#                     self.form.activity.data,
#                     event,
#                     self.form.description.data,
#                     inverse=True,
#                     type_id=link_type.id if link_type else None)
#
#     def process_link_form(self) -> None:
#         type_id = getattr(
#             self.form,
#             str(g.classes['involvement'].standard_type_id)).data
#         self.link_.type = g.types[int(type_id)] if type_id else None
#         self.link_.property = g.properties[self.form.activity.data]

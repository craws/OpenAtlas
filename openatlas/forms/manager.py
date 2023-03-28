import ast
from typing import Any

from flask import g, request
from flask_babel import lazy_gettext as _
from wtforms import (
    BooleanField, HiddenField, SelectField, SelectMultipleField, StringField,
    TextAreaField, widgets)
from wtforms.validators import InputRequired, Optional, URL

from openatlas.forms.base_manager import (
    ActorBaseManager, ArtifactBaseManager, BaseManager, EventBaseManager,
    HierarchyBaseManager, TypeBaseManager)
from openatlas.forms.field import (
    DragNDropField, SubmitField, TableField, TableMultiField, TreeField)
from openatlas.forms.validation import file
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


class AcquisitionManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'given_place': TableMultiField(_('given place')),
            'artifact': TableMultiField(_('given artifact'))})

    def populate_update(self) -> None:
        super().populate_update()
        data: dict[str, list[int]] = {'place': [], 'artifact': []}
        for entity in self.entity.get_linked_entities('P24'):
            var = 'artifact' if entity.class_.name == 'artifact' else 'place'
            data[var].append(entity.id)
        self.form.given_place.data = data['place']
        self.form.artifact.data = data['artifact']

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P24')
        self.add_link('P24', self.form.given_place.data)
        self.add_link('P24', self.form.artifact.data)


class ActorRelationManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        fields = {'inverse': BooleanField(_('inverse'))}
        if not self.link_:
            fields['actor'] = TableMultiField(
                _('actor'),
                [InputRequired()],
                filter_ids=[self.origin.id])
            fields['relation_origin_id'] = HiddenField()
        return fields

    def populate_insert(self) -> None:
        self.form.relation_origin_id.data = self.origin.id

    def populate_update(self) -> None:
        super().populate_update()
        if self.origin.id == self.link_.range.id:
            self.form.inverse.data = True

    def process_form(self) -> None:
        super().process_form()
        for actor in Entity.get_by_ids(
                ast.literal_eval(self.form.actor.data)):
            link_type = self.get_link_type()
            self.add_link(
                'OA7',
                actor,
                self.form.description.data,
                inverse=bool(self.form.inverse.data),
                type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['actor_relation'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None
        inverse = self.form.inverse.data
        if (self.origin.id == self.link_.domain.id and inverse) or \
                (self.origin.id == self.link_.range.id and not inverse):
            new_range = self.link_.domain
            self.link_.domain = self.link_.range
            self.link_.range = new_range


class ActorFunctionManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        if self.link_:
            return {}
        return {
            'member_origin_id': HiddenField(),
            'group' if 'membership' in request.url else 'actor':
                TableMultiField(
                    _('actor'),
                    [InputRequired()],
                    filter_ids=[self.origin.id])}

    def populate_insert(self) -> None:
        self.form.member_origin_id.data = self.origin.id

    def process_form(self) -> None:
        super().process_form()
        link_type = self.get_link_type()
        class_ = 'group' if hasattr(self.form, 'group') else 'actor'
        for actor in Entity.get_by_ids(
                ast.literal_eval(getattr(self.form, class_).data)):
            self.add_link(
                'P107',
                actor,
                self.form.description.data,
                inverse=(class_ == 'group'),
                type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['actor_function'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None


class ActivityManager(EventBaseManager):
    pass


class AdministrativeUnitManager(TypeBaseManager):

    def process_form(self) -> None:
        super().process_form()
        type_ = self.origin if isinstance(self.origin, Type) else self.entity
        root = self.get_root_type()
        super_id = g.types[type_.root[-1]] if type_.root else type_
        new_super_id = getattr(self.form, str(root.id)).data
        new_super = g.types[int(new_super_id)] if new_super_id else root
        if super_id != new_super.id:
            self.data['links']['delete'].add('P89')
            self.add_link('P89', new_super)


class ArtifactManager(ArtifactBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if entity := self.entity:
            filter_ids = \
                [entity.id] + \
                [e.id for e in entity.get_linked_entities_recursive('P46')]
        return dict(super().additional_fields(), **{
            'artifact_super': TableField(
                _('super'),
                filter_ids=filter_ids,
                add_dynamic=['place'])})

    def populate_insert(self) -> None:
        super().populate_insert()
        if self.origin and self.origin.class_.view in ['artifact', 'place']:
            self.form.artifact_super.data = str(self.origin.id)

    def populate_update(self) -> None:
        super().populate_update()
        if super_ := self.entity.get_linked_entity('P46', inverse=True):
            self.form.artifact_super.data = super_.id

    def process_form(self) -> None:
        super().process_form()
        if self.form.artifact_super.data:
            self.add_link('P46', self.form.artifact_super.data, inverse=True)


class BibliographyManager(BaseManager):
    fields = ['name', 'description', 'continue']


class CreationManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'file': TableMultiField(_('document'))})

    def populate_insert(self) -> None:
        super().populate_insert()
        if self.origin and self.origin.class_.name == 'file':
            self.form.file.data = [self.origin.id]

    def populate_update(self) -> None:
        super().populate_update()
        self.form.file.data = [
            entity.id for entity in self.entity.get_linked_entities('P94')]

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P94')
        self.add_link('P94', self.form.file.data)


class EditionManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EventManager(EventBaseManager):
    pass


class ExternalReferenceManager(BaseManager):
    fields = ['url', 'description', 'continue']


class FeatureManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(
                    _('insert and add') + ' ' + _('stratigraphic unit')))

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'feature_super': TableField(
                _('super'),
                [InputRequired()],
                add_dynamic=['place'])})

    def populate_insert(self) -> None:
        super().populate_insert()
        if self.origin and self.origin.class_.name == 'place':
            self.form.feature_super.data = str(self.origin.id)

    def populate_update(self) -> None:
        super().populate_update()
        self.form.feature_super.data = \
            self.entity.get_linked_entity_safe('P46', inverse=True).id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.feature_super.data)),
            inverse=True)


class FileManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        fields = {}
        if not self.entity:
            fields['file'] = DragNDropField(_('file'), [InputRequired()])
            setattr(self.form_class, 'validate_file', file)
        if not self.entity \
                and self.origin \
                and self.origin.class_.view == 'reference':
            fields['page'] = StringField()  # Needed to link file after insert
        return fields


class GroupManager(ActorBaseManager):
    pass


class HumanRemainsManager(ArtifactBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if entity := self.entity:
            filter_ids = \
                [entity.id] + \
                [e.id for e in entity.get_linked_entities_recursive('P46')]
        return dict(super().additional_fields(), **{
            'human_remains_super': TableField(
                _('super'),
                filter_ids=filter_ids,
                add_dynamic=['place'])})

    def populate_insert(self) -> None:
        super().populate_insert()
        if self.origin and self.origin.class_.view in ['artifact', 'place']:
            self.form.human_remains_super.data = str(self.origin.id)

    def populate_update(self) -> None:
        super().populate_update()
        if super_ := self.entity.get_linked_entity('P46', inverse=True):
            self.form.human_remains_super.data = super_.id

    def process_form(self) -> None:
        super().process_form()
        if self.form.human_remains_super.data:
            self.add_link(
                'P46',
                self.form.human_remains_super.data,
                inverse=True)


class HierarchyCustomManager(HierarchyBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        tooltip = _('tooltip hierarchy multiple')
        return {
            **{'multiple': BooleanField(_('multiple'), description=tooltip)},
            **super().additional_fields()}


class HierarchyValueManager(HierarchyBaseManager):
    pass


class InvolvementManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        event_class_name = ''
        if self.link_:
            event_class_name = self.link_.domain.class_.name
        elif self.origin and self.origin.class_.view != 'actor':
            event_class_name = self.origin.class_.name
        choices = [('P11', g.properties['P11'].name)]
        if event_class_name in \
                ['acquisition', 'activity', 'creation', 'production']:
            choices.append(('P14', g.properties['P14'].name))
            if event_class_name == 'acquisition':
                choices.append(('P22', g.properties['P22'].name))
                choices.append(('P23', g.properties['P23'].name))
        fields = {'activity': SelectField(_('activity'), choices=choices)}
        if not self.entity and not self.link_ and self.origin:
            name = 'actor' if self.origin.class_.view == 'event' else 'event'
            fields[name] = TableMultiField(_(name), [InputRequired()])
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        self.form.activity.data = self.link_.property.code

    def process_form(self) -> None:
        super().process_form()
        if self.origin.class_.view == 'event':
            actors = Entity.get_by_ids(ast.literal_eval(self.form.actor.data))
            for actor in actors:
                link_type = self.get_link_type()
                self.add_link(
                    self.form.activity.data,
                    actor,
                    self.form.description.data,
                    type_id=link_type.id if link_type else None)
        else:
            events = Entity.get_by_ids(ast.literal_eval(self.form.event.data))
            for event in events:
                link_type = self.get_link_type()
                self.add_link(
                    self.form.activity.data,
                    event,
                    self.form.description.data,
                    inverse=True,
                    type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['involvement'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None
        self.link_.property = g.properties[self.form.activity.data]


class MoveManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'place_from': TableField(_('from'), add_dynamic=['place']),
            'place_to': TableField(_('to'), add_dynamic=['place']),
            'artifact': TableMultiField(),
            'person': TableMultiField()})

    def populate_update(self) -> None:
        super().populate_update()
        if place_from := self.entity.get_linked_entity('P27'):
            self.form.place_from.data = \
                place_from.get_linked_entity_safe('P53', True).id
        if place_to := self.entity.get_linked_entity('P26'):
            self.form.place_to.data = \
                place_to.get_linked_entity_safe('P53', True).id
        person_data = []
        object_data = []
        for linked_entity in self.entity.get_linked_entities('P25'):
            if linked_entity.class_.name == 'person':
                person_data.append(linked_entity.id)
            elif linked_entity.class_.view == 'artifact':
                object_data.append(linked_entity.id)
        self.form.person.data = person_data
        self.form.artifact.data = object_data

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].update(['P25', 'P26', 'P27'])
        if self.form.artifact.data:
            self.add_link('P25', self.form.artifact.data)
        if self.form.person.data:
            self.add_link('P25', self.form.person.data)
        if self.form.place_from.data:
            self.add_link(
                'P27',
                Link.get_linked_entity_safe(
                    int(self.form.place_from.data),
                    'P53'))
        if self.form.place_to.data:
            self.add_link(
                'P26',
                Link.get_linked_entity_safe(
                    int(self.form.place_to.data),
                    'P53'))


class PersonManager(ActorBaseManager):

    def customize_labels(self) -> None:
        self.form.begins_in.label.text = _('born in')
        self.form.ends_in.label.text = _('died in')


class PlaceManager(BaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(_('insert and add') + ' ' + _('feature')))

    def populate_insert(self) -> None:
        self.form.alias.append_entry('')


class ProductionManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'artifact': TableMultiField()})

    def populate_update(self) -> None:
        super().populate_update()
        self.form.artifact.data = \
            [entity.id for entity in self.entity.get_linked_entities('P108')]

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P108')
        self.add_link('P108', self.form.artifact.data)


class ReferenceSystemManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        precision_id = str(Type.get_hierarchy('External reference match').id)
        choices = ReferenceSystem.get_class_choices(self.entity)
        return {
            'website_url': StringField(_('website URL'), [Optional(), URL()]),
            'resolver_url': StringField(
                _('resolver URL'),
                [Optional(), URL()]),
            'placeholder': StringField(_('example ID')),
            precision_id: TreeField(precision_id),
            'classes': SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                choices=choices,
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))
            if choices else None}

    def process_form(self) -> None:
        super().process_form()
        self.data['reference_system'] = {
            'website_url': self.form.website_url.data,
            'resolver_url': self.form.resolver_url.data,
            'placeholder': self.form.placeholder.data,
            'classes': self.form.classes.data if self.form.classes else None}


class SourceManager(BaseManager):
    fields = ['name', 'continue', 'description']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'artifact': TableMultiField(description=_(
                'Link artifacts as the information carrier of the source'))}

    def populate_insert(self) -> None:
        if self.origin and self.origin.class_.name == 'artifact':
            self.form.artifact.data = [self.origin.id]

    def populate_update(self) -> None:
        super().populate_update()
        self.form.artifact.data = [
            item.id for item in
            self.entity.get_linked_entities('P128', inverse=True)]

    def process_form(self) -> None:
        super().process_form()
        if not self.origin:
            self.data['links']['delete_inverse'].add('P128')
            if self.form.artifact.data:
                self.add_link('P128', self.form.artifact.data, inverse=True)


class SourceTranslationManager(BaseManager):
    fields = ['name', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        return {'description': TextAreaField(_('content'))}

    def process_form(self) -> None:
        super().process_form()
        if self.origin:
            self.add_link('P73', self.origin, inverse=True)


class StratigraphicUnitManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(_('insert and add') + ' ' + _('artifact')))
            setattr(
                self.form_class,
                'insert_continue_human_remains',
                SubmitField(_('insert and add') + ' ' + _('human remains')))

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'stratigraphic_super': TableField(
                _('super'),
                [InputRequired()])})

    def populate_insert(self) -> None:
        super().populate_insert()
        if self.origin and self.origin.class_.name == 'feature':
            self.form.stratigraphic_super.data = str(self.origin.id)

    def populate_update(self) -> None:
        super().populate_update()
        self.form.stratigraphic_super.data = \
            self.entity.get_linked_entity_safe('P46', inverse=True).id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.stratigraphic_super.data)),
            inverse=True)


class TypeManager(TypeBaseManager):

    def process_form(self) -> None:
        super().process_form()
        type_ = self.origin if isinstance(self.origin, Type) else self.entity
        root = self.get_root_type()
        super_id = g.types[type_.root[-1]] if type_.root else type_
        new_super_id = getattr(self.form, str(root.id)).data
        new_super = g.types[int(new_super_id)] if new_super_id else root
        if super_id != new_super.id:
            self.data['links']['delete'].add('P127')
            self.add_link('P127', new_super)

from typing import Any

from flask import g, request
from flask_babel import lazy_gettext as _
from wtforms import (
    BooleanField, HiddenField, MultipleFileField, SelectField,
    SelectMultipleField, StringField, SubmitField, TextAreaField, widgets)
from wtforms.validators import (
    InputRequired, Optional as OptionalValidator, URL)

from openatlas.forms.base_manager import (
    ActorBaseManager, BaseManager, EventBaseManager, HierarchyBaseManager)
from openatlas.forms.field import TableField, TableMultiField, TreeField
from openatlas.forms.validation import \
    (actor_relation, file, membership, type_super)
from openatlas.models.link import Link
from openatlas.models.openatlas_class import uc_first
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


class AcquisitionManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'given_place': TableMultiField(_('given place'))})

    def populate_update(self) -> None:
        super().populate_update()
        self.form.given_place.data = [
            entity.id for entity in self.entity.get_linked_entities('P24')]

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P24')
        self.data['links']['insert'].append({
            'property': 'P24',
            'range': self.form.given_place.data})


class ActorFunctionManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        if self.link_:
            return {}
        target = 'group' if 'membership' in request.url else 'actor'
        setattr(self.form_class, f'validate_{target}', membership)
        return {
            'member_origin_id': HiddenField(),
            target: TableMultiField(_('actor'), [InputRequired()])}

    def populate_insert(self) -> None:
        self.form.member_origin_id.data = self.origin.id


class ActivityManager(EventBaseManager):
    pass


class ActorActorRelationManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        fields = {'inverse': BooleanField(_('inverse'))}
        if not self.link_:
            fields['actor'] = TableMultiField(_('actor'), [InputRequired()])
            fields['relation_origin_id'] = HiddenField()
        setattr(self.form_class, 'validate_actor', actor_relation)
        return fields

    def populate_insert(self) -> None:
        self.form.relation_origin_id.data = self.origin.id

    def populate_update(self) -> None:
        super().populate_update()
        if self.origin.id == self.link_.range.id:
            self.form.inverse.data = True


class AdministrativeUnitManager(BaseManager):
    fields = ['name', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        root = self.get_root_type()
        return {
            'is_type_form': HiddenField(),
            str(root.id): TreeField(str(root.id))}

    def populate_update(self) -> None:
        super().populate_update()
        if isinstance(self.entity, Type):
            root = g.types[self.entity.root[0]] \
                if self.entity.root else self.entity
            if root:  # Set super if exists and is not same as root
                super_ = g.types[self.entity.root[-1]]
                getattr(
                    self.form,
                    str(root.id)).data = super_.id \
                    if super_.id != root.id else None

    def process_form(self) -> None:
        super().process_form()
        type_ = self.origin if isinstance(self.origin, Type) else self.entity
        root = self.get_root_type()
        super_id = g.types[type_.root[-1]] if type_.root else type_
        new_super_id = getattr(self.form, str(root.id)).data
        new_super = g.types[int(new_super_id)] if new_super_id else root
        if super_id != new_super.id:
            self.data['links']['delete'].add('P89')
            self.data['links']['insert'].append({
                'property': 'P89',
                'range': new_super})


class ArtifactManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        return {'actor': TableField(_('owned by'))}

    def populate_update(self) -> None:
        super().populate_update()
        if owner := self.entity.get_linked_entity('P52'):
            self.form.actor.data = owner.id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P52')
        if self.origin and self.origin.class_.name == 'stratigraphic_unit':
            self.data['links']['insert'].append({
                'property': 'P46',
                'range': self.origin,
                'inverse': True})
        if self.form.actor.data:
            self.data['links']['insert'].append({
                'property': 'P52',
                'range': self.form.actor.data})


class BibliographyManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EditionManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EventManager(EventBaseManager):
    pass


class ExternalReferenceManager(BaseManager):
    fields = ['url', 'description', 'continue']


class FeatureManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def process_form(self) -> None:
        super().process_form()
        if self.origin and self.origin.class_.name == 'place':
            self.data['links']['insert'].append({
                'property': 'P46',
                'range': self.origin,
                'inverse': True})

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(
                    f"{uc_first(_('insert and add'))} "
                    f"{_('stratigraphic unit')}"))


class FileManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        fields = {}
        if not self.entity:
            fields['file'] = MultipleFileField(_('file'), [InputRequired()])
            setattr(self.form_class, 'validate_file', file)
        if not self.entity \
                and self.origin \
                and self.origin.class_.view == 'reference':
            fields['page'] = StringField()  # Needed to link file after insert
        return fields


class GroupManager(ActorBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return {
            'residence': TableField(_('residence')),
            'begins_in': TableField(_('begins in')),
            'ends_in': TableField(_('ends in'))}


class HumanRemainsManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        return {'actor': TableField(_('owned by'))}

    def populate_update(self) -> None:
        super().populate_update()
        if owner := self.entity.get_linked_entity('P52'):
            self.form.actor.data = owner.id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P52')
        if self.origin and self.origin.class_.name == 'stratigraphic_unit':
            self.data['links']['insert'].append({
                'property': 'P46',
                'range': self.origin,
                'inverse': True})
        if self.form.actor.data:
            self.data['links']['insert'].append({
                'property': 'P52',
                'range': self.form.actor.data})


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
        if event_class_name in ['acquisition', 'activity']:
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


class MoveManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'place_from': TableField(_('from')),
            'place_to': TableField(_('to')),
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
            self.data['links']['insert'].append({
                'property': 'P25',
                'range': self.form.artifact.data})
        if self.form.person.data:
            self.data['links']['insert'].append({
                'property': 'P25',
                'range': self.form.person.data})
        if self.form.place_from.data:
            self.data['links']['insert'].append({
                'property': 'P27',
                'range': Link.get_linked_entity_safe(
                    int(self.form.place_from.data),
                    'P53')})
        if self.form.place_to.data:
            self.data['links']['insert'].append({
                'property': 'P26',
                'range': Link.get_linked_entity_safe(
                    int(self.form.place_to.data),
                    'P53')})


class PersonManager(ActorBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return {
            'residence': TableField(_('residence')),
            'begins_in': TableField(_('born in')),
            'ends_in': TableField(_('died in'))}


class PlaceManager(BaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(f"{uc_first(_('insert and add'))} {_('feature')}"))


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
        self.data['links']['insert'].append({
            'property': 'P108',
            'range': self.form.artifact.data})


class ReferenceSystemManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        precision_id = str(Type.get_hierarchy('External reference match').id)
        choices = ReferenceSystem.get_class_choices(self.entity)
        return {
            'website_url': StringField(
                _('website URL'),
                [OptionalValidator(), URL()]),
            'resolver_url': StringField(
                _('resolver URL'),
                [OptionalValidator(), URL()]),
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
    fields = ['name', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'artifact': TableMultiField(description=_(
                'Link artifacts as the information carrier of the source')),
            'description': TextAreaField(_('content'))}

    def populate_update(self) -> None:
        self.form.artifact.data = [
            item.id for item in
            self.entity.get_linked_entities('P128', inverse=True)]

    def process_form(self) -> None:
        super().process_form()
        if not self.origin:
            self.data['links']['delete_inverse'].add('P128')
            if self.form.artifact.data:
                self.data['links']['insert'].append({
                    'property': 'P128',
                    'range': self.form.artifact.data,
                    'inverse': True})


class SourceTranslationManager(BaseManager):
    fields = ['name', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        return {'description': TextAreaField(_('content'))}

    def process_form(self) -> None:
        super().process_form()
        if self.origin:
            self.data['links']['insert'].append({
                'property': 'P73',
                'range': self.origin,
                'inverse': True})


class StratigraphicUnitManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def process_form(self) -> None:
        super().process_form()
        if self.origin and self.origin.class_.name == 'feature':
            self.data['links']['insert'].append({
                'property': 'P46',
                'range': self.origin,
                'inverse': True})

    def add_buttons(self) -> None:
        super().add_buttons()
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(
                    f"{uc_first(_('insert and add'))} {_('artifact')}"))
            setattr(
                self.form_class,
                'insert_continue_human_remains',
                SubmitField(
                    f"{uc_first(_('insert and add'))} {_('human remains')}"))


class TypeManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        root = self.get_root_type()
        fields = {
            'is_type_form': HiddenField(),
            str(root.id): TreeField(str(root.id)) if root else None}
        if root.directional:
            fields['name_inverse'] = StringField(_('inverse'))
        if self.entity:
            setattr(self.form_class, f'validate_{root.id}', type_super)
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        if hasattr(self.form, 'name_inverse'):  # e.g. actor relation
            name_parts = self.entity.name.split(' (')
            self.form.name.data = name_parts[0]
            if len(name_parts) > 1:
                self.form.name_inverse.data = name_parts[1][:-1]  # remove ")"
        if isinstance(self.entity, Type):  # Set super if it isn't the root
            super_ = g.types[self.entity.root[-1]]
            root = g.types[self.entity.root[0]]
            if super_.id != root.id:
                getattr(self.form, str(root.id)).data = super_.id

    def process_form(self) -> None:
        super().process_form()
        type_ = self.origin if isinstance(self.origin, Type) else self.entity
        root = self.get_root_type()
        super_id = g.types[type_.root[-1]] if type_.root else type_
        new_super_id = getattr(self.form, str(root.id)).data
        new_super = g.types[int(new_super_id)] if new_super_id else root
        if super_id != new_super.id:
            self.data['links']['delete'].add('P127')
            self.data['links']['insert'].append({
                'property': 'P127',
                'range': new_super})
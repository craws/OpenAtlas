import ast
from typing import Any

from flask import g, request, url_for
from flask_babel import lazy_gettext as _
from wtforms import (
    BooleanField, HiddenField, SelectField, SelectMultipleField, StringField,
    widgets)
from wtforms.validators import InputRequired, Optional, URL

from openatlas.forms.base_manager import (
    ActorBaseManager, ArtifactBaseManager, BaseManager, EventBaseManager,
    HierarchyBaseManager, PlaceBaseManager, SourceBaseManager, TypeBaseManager)
from openatlas.forms.field import (
    DragNDropField, SubmitField, TableField, TableMultiField,
    TextAnnotationField, TreeField)
from openatlas.forms.validation import file
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem


class AcquisitionManager(EventBaseManager):
    _('given place')
    _('given artifact')

    def additional_fields(self) -> dict[str, Any]:
        data: dict[str, list[Any]] = {'place': [], 'artifact': []}
        if not self.insert:
            for entity in self.entity.get_linked_entities('P24', sort=True):
                data[
                    'artifact' if entity.class_.name == 'artifact'
                    else 'place'].append(entity)
        fields = super().additional_fields()
        fields['given_place'] = TableMultiField(
            self.table_items['place'],
            data['place'])
        fields['given_artifact'] = TableMultiField(
            Entity.get_by_class('artifact', True),
            data['artifact'])
        return fields

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P24')
        self.add_link('P24', self.form.given_place.data)
        self.add_link('P24', self.form.given_artifact.data)


class ActorFunctionManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def top_fields(self) -> dict[str, Any]:
        if self.link_:
            return {}
        if 'membership' in request.url:
            field_name = 'group'
            entities = Entity.get_by_class('group', aliases=self.aliases)
        else:
            field_name = 'actor'
            entities = Entity.get_by_view('actor', aliases=self.aliases)
        return {
            'member_origin_id': HiddenField(),
            field_name:
                TableMultiField(
                    entities,
                    filter_ids=[self.origin.id],
                    validators=[InputRequired()])}

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


class ActorRelationManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def top_fields(self) -> dict[str, Any]:
        fields = {}
        if not self.link_:
            fields['actor'] = TableMultiField(
                Entity.get_by_class('person', aliases=self.aliases),
                filter_ids=[self.origin.id],
                validators=[InputRequired()])
            fields['relation_origin_id'] = HiddenField()
        return fields

    def additional_fields(self) -> dict[str, Any]:
        return {'inverse': BooleanField(_('inverse'))}

    def populate_insert(self) -> None:
        self.form.relation_origin_id.data = self.origin.id

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

    def populate_update(self) -> None:
        super().populate_update()
        if self.origin.id == self.link_.range.id:
            self.form.inverse.data = True


class ActivityManager(EventBaseManager):
    pass


class AdministrativeUnitManager(TypeBaseManager):
    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P89')
        self.add_link('P89', g.types[self.super_id])


class ArtifactManager(ArtifactBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if self.entity:
            filter_ids = [self.entity.id] + [
                e.id for e in self.entity.get_linked_entities_recursive('P46')]
        if self.insert:
            selection = self.origin if self.origin \
                and self.origin.class_.view in ['artifact', 'place'] else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return super().additional_fields() | {
            'super': TableField(
                Entity.get_by_class(
                    g.view_class_mapping['place'] + ['artifact'],
                    types=True,
                    aliases=self.aliases),
                selection,
                filter_ids,
                add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        if self.form.super.data:
            self.add_link('P46', self.form.super.data, inverse=True)


class BibliographyManager(BaseManager):
    fields = ['name', 'description', 'continue']


class CreationManager(EventBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        selection = None
        if self.insert:
            if self.origin and self.origin.class_.name == 'file':
                selection = [self.origin]
        else:
            selection = self.entity.get_linked_entities('P94', sort=True)
        return super().additional_fields() | {
            'document':
                TableMultiField(Entity.get_by_class('file'), selection)}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P94')
        self.add_link('P94', self.form.document.data)


class EditionManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EventManager(EventBaseManager):
    pass


class ExternalReferenceManager(BaseManager):
    fields = ['url', 'description', 'continue']

    def add_name_fields(self) -> None:
        setattr(
            self.form_class,
            'name',
            StringField(
                _('URL'),
                [InputRequired(), URL()],
                render_kw={'autofocus': True}))


class FeatureManager(PlaceBaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        super().add_buttons()
        if self.entity:
            return
        setattr(
            self.form_class,
            'insert_continue_sub',
            SubmitField(_('insert and add') + ' ' + _('stratigraphic unit')))

    def additional_fields(self) -> dict[str, Any]:
        if self.insert:
            selection = self.origin if self.origin \
                and self.origin.class_.name == 'place' else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return super().additional_fields() | {
            'super':
                TableField(
                    Entity.get_by_class('place', True, self.aliases),
                    selection,
                    validators=[InputRequired()],
                    add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.super.data)),
            inverse=True)


class FileManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        fields = {}
        if not self.entity:
            fields['file'] = DragNDropField(_('file'), [InputRequired()])
            setattr(self.form_class, 'validate_file', file)
        fields['public'] = BooleanField(_('public sharing allowed'))
        fields['creator'] = StringField(_('creator'))
        fields['license_holder'] = StringField(_('license holder'))
        if not self.entity \
                and self.origin \
                and self.origin.class_.view == 'reference':
            fields['page'] = StringField(_('page'))
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        self.form.public.data = self.entity.public
        self.form.creator.data = self.entity.creator
        self.form.license_holder.data = self.entity.license_holder


class GroupManager(ActorBaseManager):
    pass


class HumanRemainsManager(ArtifactBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if self.entity:
            filter_ids = [self.entity.id] + [
                e.id for e in self.entity.get_linked_entities_recursive('P46')]
        if self.insert:
            selection = self.origin if self.origin \
                and self.origin.class_.view in ['artifact', 'place'] else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return super().additional_fields() | {
            'super': TableField(
                Entity.get_by_class(
                    g.view_class_mapping['place'] + ['human remains'],
                    types=True,
                    aliases=self.aliases),
                selection,
                filter_ids,
                add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        if self.form.super.data:
            self.add_link('P46', self.form.super.data, inverse=True)


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

    def top_fields(self) -> dict[str, Any]:
        event_class_name = ''
        if self.link_:
            event_class_name = self.link_.domain.class_.name
        elif self.origin and self.origin.class_.view != 'actor':
            event_class_name = self.origin.class_.name
        fields = {}
        if self.insert and self.origin:
            class_ = 'actor' if self.origin.class_.view == 'event' else 'event'
            fields[class_] = TableMultiField(
                Entity.get_by_view(class_, True, self.aliases),
                validators=[InputRequired()])
        choices = [('P11', g.properties['P11'].name)]
        if event_class_name in [
                'acquisition', 'activity', 'creation', 'modification',
                'production']:
            choices.append(('P14', g.properties['P14'].name))
            if event_class_name == 'acquisition':
                choices.append(('P22', g.properties['P22'].name))
                choices.append(('P23', g.properties['P23'].name))
        fields['activity'] = SelectField(_('activity'), choices=choices)
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


class ModificationManager(EventBaseManager):
    _('modified place')

    def additional_fields(self) -> dict[str, Any]:
        artifacts = []
        places = []
        if not self.insert:
            for item in self.entity.get_linked_entities('P31', sort=True):
                if item.class_.name == 'artifact':
                    artifacts.append(item)
                elif item.cidoc_class.code == 'E18':
                    places.append(item)
        return super().additional_fields() | {
            'artifact': TableMultiField(
                Entity.get_by_class('artifact', True),
                artifacts),
            'modified_place': TableMultiField(
                self.table_items['place'],
                places)}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P31')
        if self.form.artifact.data:
            self.add_link('P31', self.form.artifact.data)
        if self.form.modified_place.data:
            self.add_link('P31', self.form.modified_place.data)


class MoveManager(EventBaseManager):
    _('moved artifact')
    _('moved person')
    _('place to')
    _('place from')

    def additional_fields(self) -> dict[str, Any]:
        place_from = None
        place_to = None
        data: dict[str, list[Any]] = {'artifact': [], 'person': []}
        if self.entity:
            if place := self.entity.get_linked_entity('P27'):
                place_from = place.get_linked_entity_safe('P53', True)
            if place := self.entity.get_linked_entity('P26'):
                place_to = place.get_linked_entity_safe('P53', True)
            for linked_entity in self.entity.get_linked_entities(
                    'P25',
                    sort=True):
                data[linked_entity.class_.name].append(linked_entity)
        elif self.origin:
            if self.origin.class_.view == 'artifact':
                data['artifact'] = [self.origin]
            elif self.origin.class_.view == 'place':
                place_from = self.origin
        return super().additional_fields() | {
            'place_from': TableField(
                self.table_items['place'],
                place_from,
                add_dynamic=['place']),
            'place_to': TableField(
                self.table_items['place'],
                place_to,
                add_dynamic=['place']),
            'moved_artifact': TableMultiField(
                Entity.get_by_class('artifact', True),
                data['artifact']),
            'moved_person': TableMultiField(
                Entity.get_by_class('person', aliases=self.aliases),
                data['person'])}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].update(['P25', 'P26', 'P27'])
        if self.form.moved_artifact.data:
            self.add_link('P25', self.form.moved_artifact.data)
        if self.form.moved_person.data:
            self.add_link('P25', self.form.moved_person.data)
        if self.form.place_from.data:
            self.add_link(
                'P27',
                Entity.get_linked_entity_safe_static(
                    int(self.form.place_from.data),
                    'P53'))
        if self.form.place_to.data:
            self.add_link(
                'P26',
                Entity.get_linked_entity_safe_static(
                    int(self.form.place_to.data),
                    'P53'))


class PersonManager(ActorBaseManager):
    def customize_labels(self) -> None:
        self.form.begins_in.label.text = _('born in')
        self.form.ends_in.label.text = _('died in')


class PlaceManager(PlaceBaseManager):
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
        selection = None
        if not self.insert and self.entity:
            selection = self.entity.get_linked_entities('P108', sort=True)
        return super().additional_fields() | {
            'artifact': TableMultiField(
                Entity.get_by_class('artifact', True),
                selection)}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P108')
        self.add_link('P108', self.form.artifact.data)


class ReferenceSystemManager(BaseManager):
    fields = ['name', 'description']

    def add_name_fields(self) -> None:
        super().add_name_fields()
        if self.entity and self.entity.system:
            setattr(
                self.form_class,
                'name',
                StringField(
                    _('name'),
                    render_kw={'autofocus': True, 'readonly': True}))

    def additional_fields(self) -> dict[str, Any]:
        choices = []
        for class_ in g.classes.values():
            if not class_.reference_system_allowed \
                    or (self.entity and class_.name in self.entity.classes) \
                    or (
                    self.entity
                    and self.entity.name == 'GeoNames'
                    and class_.name != 'Place'):
                continue
            choices.append((class_.name, g.classes[class_.name].label))
        precision_id = str(g.reference_match_type.id)
        return {
            'website_url': StringField(_('website URL'), [Optional(), URL()]),
            'resolver_url': StringField(
                _('resolver URL'),
                [Optional(), URL()]),
            'placeholder': StringField(_('example ID')),
            precision_id: TreeField(precision_id),
            'classes': SelectMultipleField(
                _('classes'),
                choices=choices,
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))
            if choices else None}

    def insert_entity(self) -> None:
        self.entity = ReferenceSystem.insert_system({
            'name': self.form.name.data,
            'description': self.form.description.data,
            'website_url': self.form.website_url.data,
            'resolver_url': self.form.resolver_url.data})

    def process_form(self) -> None:
        super().process_form()
        self.data['reference_system'] = {
            'website_url': self.form.website_url.data,
            'resolver_url': self.form.resolver_url.data,
            'placeholder': self.form.placeholder.data,
            'classes': self.form.classes.data if self.form.classes else None}


class SourceManager(SourceBaseManager):
    def add_description(self) -> None:
        text = ''
        linked_entities = []
        if self.entity:
            text = self.entity.get_annotated_text()
            for e in self.entity.get_linked_entities('P67'):
                linked_entities.append({'id': e.id, 'name': e.name})
        setattr(self.form_class, 'description', TextAnnotationField(
            label=_('content'),
            source_text=text,
            linked_entities=linked_entities))

    def additional_fields(self) -> dict[str, Any]:
        selection = None
        if not self.insert and self.entity:
            selection = self.entity.get_linked_entities('P128', True, True)
        elif self.origin and self.origin.class_.name == 'artifact':
            selection = [self.origin]
        return super().additional_fields() | {
            'artifact': TableMultiField(
                Entity.get_by_class('artifact', True),
                selection,
                description=
                _('Link artifacts as the information carrier of the source'))}

    def process_form(self) -> None:
        super().process_form()
        if not self.origin:
            self.data['links']['delete_inverse'].add('P128')
            if self.form.artifact.data:
                self.add_link('P128', self.form.artifact.data, inverse=True)


class SourceTranslationManager(SourceBaseManager):
    def add_description(self) -> None:
        text = ''
        linked_entities = []
        if self.entity:
            text = self.entity.get_annotated_text()
            source = self.entity.get_linked_entity_safe('P73', True)
            for e in source.get_linked_entities('P67'):
                linked_entities.append({'id': e.id, 'name': e.name})
        setattr(self.form_class, 'description', TextAnnotationField(
            label=_('content'),
            source_text=text,
            linked_entities=linked_entities))

    def get_crumbs(self) -> list[Any]:
        if not self.origin:
            self.crumbs = [
                [_('source'), url_for('index', view='source')],
                self.entity.get_linked_entity('P73', True)]
        return super().get_crumbs()

    def process_form(self) -> None:
        super().process_form()
        if self.origin:
            self.add_link('P73', self.origin, inverse=True)


class StratigraphicUnitManager(PlaceBaseManager):
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
        selection = None
        if not self.insert and self.entity:
            selection = self.entity.get_linked_entity_safe('P46', inverse=True)
        elif self.origin and self.origin.class_.name == 'feature':
            selection = self.origin
        return super().additional_fields() | {
            'super': TableField(
                Entity.get_by_class('feature', True),
                selection,
                validators=[InputRequired()])}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.super.data)),
            inverse=True)


class TypeManager(TypeBaseManager):
    def add_description(self) -> None:
        super().add_description()
        if self.get_root().category == 'value':
            del self.form_class.description  # pylint: disable=no-member
            setattr(self.form_class, 'description', StringField(_('unit')))

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P127')
        self.add_link('P127', g.types[self.super_id])

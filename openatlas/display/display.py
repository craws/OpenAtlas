from flask import g, url_for
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.display.base_display import (
    ActorDisplay, BaseDisplay, EventsDisplay, PlaceBaseDisplay,
    ReferenceBaseDisplay, TypeBaseDisplay)
from openatlas.display.tab import Tab
from openatlas.display.util import edit_link, remove_link
from openatlas.models.entity import Entity
from openatlas.util.table import Table
from openatlas.util.util import (
    button, external_link, get_base_table_data, get_file_path, is_authorized,
    link)


class AcquisitionDisplay(EventsDisplay):
    pass


class ActivityDisplay(EventsDisplay):
    pass


class AdministrativeUnitDisplay(TypeBaseDisplay):
    pass


class ArtifactDisplay(PlaceBaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for link_ in self.entity.get_links(['P24', 'P25', 'P108'], True):
            self.tabs['event'].table.rows.append(
                get_base_table_data(link_.domain))


class BibliographyDisplay(ReferenceBaseDisplay):
    pass


class FileDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for name in [
                'source', 'event', 'actor', 'place', 'feature',
                'stratigraphic_unit', 'artifact', 'reference', 'type']:
            self.tabs[name] = Tab(name, entity=self.entity)
        self.entity.image_id = self.entity.id \
            if get_file_path(self.entity.id) else None
        for link_ in self.entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data.append(remove_link(
                range_.name,
                link_,
                self.entity,
                range_.class_.name))
            self.tabs[range_.class_.view].table.rows.append(data)
        for link_ in self.entity.get_links('P67', True):
            data = get_base_table_data(link_.domain)
            data.append(link_.description)
            data.append(edit_link(
                url_for(
                    'link_update',
                    id_=link_.id,
                    origin_id=self.entity.id)))
            data.append(
                remove_link(
                    link_.domain.name,
                    link_,
                    self.entity,
                    'reference'))
            self.tabs['reference'].table.rows.append(data)


class EditionDisplay(ReferenceBaseDisplay):
    pass


class EventDisplay(EventsDisplay):
    pass


class ExternalReferenceDisplay(ReferenceBaseDisplay):
    pass


class FeatureDisplay(PlaceBaseDisplay):
    pass


class GroupDisplay(ActorDisplay):
    pass


class HumanRemainsDisplay(PlaceBaseDisplay):
    pass


class MoveDisplay(EventsDisplay):
    pass


class PersonDisplay(ActorDisplay):
    pass


class PlaceDisplay(PlaceBaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for link_ in self.entity.location.get_links(
                ['P74', 'OA8', 'OA9'],
                inverse=True):
            actor = Entity.get_by_id(link_.domain.id)
            self.tabs['actor'].table.rows.append([
                link(actor),
                g.properties[link_.property.code].name,
                actor.class_.name,
                actor.first,
                actor.last,
                actor.description])
        actor_ids = []
        for event in self.events:
            for actor in event.get_linked_entities(
                    ['P11', 'P14', 'P22', 'P23']):
                if actor.id in actor_ids:
                    continue  # pragma: no cover
                actor_ids.append(actor.id)
                self.tabs['actor'].table.rows.append([
                    link(actor),
                    f"{_('participated at an event')}",
                    event.class_.name, '', '', ''])


class ProductionDisplay(EventsDisplay):
    pass


class ReferenceSystemDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for name in self.entity.classes:
            self.tabs[name] = Tab(
                name,
                entity=self.entity,
                table=Table([_('entity'), 'id', _('precision')]))
        for link_ in self.entity.get_links('P67'):
            self.tabs[link_.range.class_.name].table.rows.append([
                link(link_.range),
                external_link(
                    f'{self.entity.resolver_url}{link_.description}',
                    link_.description)
                if self.entity.resolver_url else link_.description,
                link_.type.name])
        for name in self.entity.classes:
            self.tabs[name].buttons = []
            if not self.tabs[name].table.rows and is_authorized('manager'):
                self.tabs[name].buttons = [button(
                    _('remove'),
                    url_for(
                        'reference_system_remove_class',
                        system_id=self.entity.id,
                        class_name=name))]


class SourceDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for name in [
                'actor', 'artifact', 'feature', 'event', 'place',
                'stratigraphic_unit', 'text', 'reference', 'file']:
            self.tabs[name] = Tab(name, entity=self.entity)
        for text in self.entity.get_linked_entities('P73', types=True):
            self.tabs['text'].table.rows.append([
                link(text),
                next(iter(text.types)).name if text.types else '',
                text.description])
        for link_ in self.entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data.append(
                remove_link(
                    range_.name,
                    link_,
                    self.entity,
                    range_.class_.name))
            self.tabs[range_.class_.view].table.rows.append(data)
        for link_ in self.entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.class_.view == 'file':  # pragma: no cover
                extension = data[3]
                data.append(
                    self.get_profile_image_table_link(
                        domain,
                        extension))
                if not self.entity.image_id \
                        and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    self.entity.image_id = domain.id
            if domain.class_.view != 'file':
                data.append(link_.description)
                data.append(edit_link(
                    url_for(
                        'link_update',
                        id_=link_.id,
                        origin_id=self.entity.id)))
                if domain.class_.view == \
                        'reference_system':  # pragma: no cover
                    self.entity.reference_systems.append(link_)
                    continue
            data.append(
                remove_link(
                    domain.name,
                    link_,
                    self.entity,
                    domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)
        self.add_note_tab()


class SourceTranslationDisplay(BaseDisplay):
    pass


class StratigraphicUnitDisplay(PlaceBaseDisplay):
    pass


class TypeDisplay(TypeBaseDisplay):
    pass

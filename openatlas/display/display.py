from flask import g
from flask_babel import lazy_gettext as _

from openatlas import app
from openatlas.display.base_display import (
    ActorDisplay, BaseDisplay, EventsDisplay, PlaceBaseDisplay,
    ReferenceBaseDisplay, TypeBaseDisplay)
from openatlas.display.tab import Tab
from openatlas.display.util import remove_link
from openatlas.models.entity import Entity
from openatlas.util.util import get_base_table_data, link


class AcquisitionDisplay(EventsDisplay):
    pass

class ActivityDisplay(EventsDisplay):
    pass

class AdministrativeUnitDisplay(TypeBaseDisplay):
    pass

class ArtifactDisplay(PlaceBaseDisplay):
    pass

class BibliographyDisplay(ReferenceBaseDisplay):
    pass

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

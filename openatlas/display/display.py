from openatlas import app
from openatlas.display.base_display import (
    ActorDisplay, BaseDisplay, EventsDisplay)
from openatlas.display.tab import Tab
from openatlas.display.util import remove_link
from openatlas.util.util import get_base_table_data, link


class GroupDisplay(ActorDisplay):
    pass


class MoveDisplay(EventsDisplay):
    pass


class PersonDisplay(ActorDisplay):
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

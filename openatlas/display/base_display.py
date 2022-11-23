from typing import Union

from openatlas.database.type import Type
from openatlas.display.tab import Tab
from openatlas.models.entity import Entity


class BaseDisplay:

    entity: Union[Entity, Type]
    tabs: dict[str, Tab]

    def __init__(self, entity: Union[Entity, Type]):
        self.entity = entity
        self.add_tabs()
        # self.add_info_content()  # Call later because of profile image
        self.add_tabs_buttons()
        self.entity.image_id = entity.get_profile_image_id()

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_tabs_buttons(self) -> None:
        for tab in self.tabs.values():
            pass
            # tab.add_buttons(self.entity)

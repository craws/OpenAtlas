from typing import Optional

from flask import g, url_for
from flask_babel import lazy_gettext as _

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import is_authorized, link, uc_first


def remove_link(
        name: str,
        link_: Link,
        origin: Entity,
        tab: str) -> Optional[str]:
    if not is_authorized('contributor'):
        return None  # pragma: no cover
    url = url_for('link_delete', id_=link_.id, origin_id=origin.id)
    return link(
        _('remove'),
        f'{url}#tab-{tab}',
        js="return confirm('{x}')".format(
            x=_('Remove %(name)s?', name=name.replace("'", ''))))


def edit_link(url: str) -> Optional[str]:
    return link(_('edit'), url) if is_authorized('contributor') else None


def ext_references(links: list[Link]) -> str:
    if not links:
        return ''
    html = '<h2>' + uc_first(_("external reference systems")) + '</h2>'
    for link_ in links:
        system = g.reference_systems[link_.domain.id]
        html += link_.description if not system.resolver_url else \
            f'<a href="{ system.resolver_url + link_.description }"' \
            f' target="_blank"> { link_.description }</a>'
        html += \
            f' ({ g.types[link_.type.id].name } ' + _('at') + \
            f' { link(link_.domain) })<br>'
    return html

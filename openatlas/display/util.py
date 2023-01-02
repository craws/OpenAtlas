from typing import Any, Optional, Union

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type
from openatlas.util.image_processing import check_processed_image
from openatlas.util.util import (
    button, format_date, get_file_path, is_authorized, link, uc_first)


def remove_link(
        name: str,
        link_: Link,
        origin: Entity,
        tab: str) -> Optional[str]:
    if not is_authorized('contributor'):
        return None
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
        html += link(
            f'{system.resolver_url}{link_.description}',
            link_.description,
            external=True) if system.resolver_url else link_.description
        html += \
            f' ({ g.types[link_.type.id].name } ' + _('at') + \
            f' { link(link_.domain) })<br>'
    return html


def get_appearance(event_links: list[Link]) -> tuple[str, str]:
    # Get first/last appearance year from events for actors without begin/end
    first_year = None
    last_year = None
    first_string = ''
    last_string = ''
    for link_ in event_links:
        event = link_.domain
        actor = link_.range
        event_link = link(_('event'), url_for('view', id_=event.id))
        if not actor.first:
            if link_.first \
                    and (not first_year or int(link_.first) < int(first_year)):
                first_year = link_.first
                first_string = \
                    f"{format_entity_date(link_, 'begin', link_.object_)} " \
                    f"{_('at an')} {event_link}"
            elif event.first \
                    and (not first_year or int(event.first) < int(first_year)):
                first_year = event.first
                first_string = \
                    f"{format_entity_date(event, 'begin', link_.object_)}" \
                    f" {_('at an')} {event_link}"
        if not actor.last:
            if link_.last \
                    and (not last_year or int(link_.last) > int(last_year)):
                last_year = link_.last
                last_string = \
                    f"{format_entity_date(link_, 'end', link_.object_)} " \
                    f"{_('at an')} {event_link}"
            elif event.last \
                    and (not last_year or int(event.last) > int(last_year)):
                last_year = event.last
                last_string = \
                    f"{format_entity_date(event, 'end', link_.object_)} " \
                    f"{_('at an')} {event_link}"
    return first_string, last_string


def format_entity_date(
        entity: Union[Entity, Link],
        type_: str,  # begin or end
        object_: Optional[Entity] = None) -> str:
    html = link(object_) if object_ else ''
    if getattr(entity, f'{type_}_from'):
        html += ', ' if html else ''
        if getattr(entity, f'{type_}_to'):
            html += _(
                'between %(begin)s and %(end)s',
                begin=format_date(getattr(entity, f'{type_}_from')),
                end=format_date(getattr(entity, f'{type_}_to')))
        else:
            html += format_date(getattr(entity, f'{type_}_from'))
    comment = getattr(entity, f'{type_}_comment')
    return html + (f" ({comment})" if comment else '')


def profile_image(entity: Entity) -> str:
    if not entity.image_id:
        return ''
    path = get_file_path(entity.image_id)
    if not path:
        return ''
    resized = None
    size = app.config['IMAGE_SIZE']['thumbnail']
    if g.settings['image_processing'] and check_processed_image(path.name):
        if path_ := get_file_path(entity.image_id, size):
            resized = url_for('display_file', filename=path_.name, size=size)
    url = url_for('display_file', filename=path.name)
    src = resized or url
    style = f'max-width:{g.settings["profile_image_width"]}px;'
    ext = app.config["DISPLAY_FILE_EXTENSIONS"]
    if resized:
        style = f'max-width:{app.config["IMAGE_SIZE"]["thumbnail"]}px;'
        ext = app.config["ALLOWED_IMAGE_EXT"]
    if entity.class_.view == 'file':
        html = uc_first(_('no preview available'))
        if path.suffix.lower() in ext:
            html = link(
                f'<img style="{style}" alt="image" src="{src}">',
                url,
                external=True)
    else:
        html = link(
            f'<img style="{style}" alt="image" src="{src}">',
            url_for('view', id_=entity.image_id))
    return f'<div id="profile-image-div">{html}</div>'


def profile_image_table_link(
        entity: Entity,
        file: Entity,
        extension: str) -> str:
    if file.id == entity.image_id:
        return link(
            _('unset'),
            url_for('file_remove_profile_image', entity_id=entity.id))
    if extension in app.config['DISPLAY_FILE_EXTENSIONS'] or (
            g.settings['image_processing']
            and extension in app.config['ALLOWED_IMAGE_EXT']):
        return link(
            _('set'),
            url_for('set_profile_image', id_=file.id, origin_id=entity.id))
    return ''


def delete_link(entity: Entity) -> str:
    confirm = ''
    if isinstance(entity, Type):
        url = url_for('type_delete', id_=entity.id)
        if entity.count or entity.subs:
            url = url_for('type_delete_recursive', id_=entity.id)
    else:
        if current_user.group == 'contributor':
            info = g.logger.get_log_info(entity.id)
            if not info['creator'] or info['creator'].id != current_user.id:
                return ''
        url = url_for('index', view=entity.class_.view, delete_id=entity.id)
        confirm = _('Delete %(name)s?', name=entity.name.replace('\'', ''))
    return button(
        _('delete'),
        url,
        onclick=f"return confirm('{confirm}')" if confirm else '')


def siblings_pager(
        entity: Entity,
        structure: Optional[dict[str, list[Entity]]] = None) -> str:
    if not structure or len(structure['siblings']) < 2:
        return ''
    structure['siblings'].sort(key=lambda x: x.id)
    prev_id = None
    next_id = None
    position = None
    for counter, sibling in enumerate(structure['siblings']):
        position = counter + 1
        prev_id = sibling.id if sibling.id < entity.id else prev_id
        if sibling.id > entity.id:
            next_id = sibling.id
            position = counter
            break
    parts = []
    if prev_id:
        parts.append(button('<', url_for('view', id_=prev_id)))
    if next_id:
        parts.append(button('>', url_for('view', id_=next_id)))
    parts.append(f"{position} {_('of')} {len(structure['siblings'])}")
    return ' '.join(parts)


def get_system_data(entity: Entity) -> dict[str, Any]:
    data = {}
    if 'entity_show_class' in current_user.settings \
            and current_user.settings['entity_show_class']:
        data[_('class')] = link(entity.cidoc_class)
    info = g.logger.get_log_info(entity.id)
    if 'entity_show_dates' in current_user.settings \
            and current_user.settings['entity_show_dates']:
        data[_('created')] = \
            f"{format_date(entity.created)} {link(info['creator'])}"
        if info['modified']:
            data[_('modified')] = \
                f"{format_date(info['modified'])} {link(info['modifier'])}"
    if 'entity_show_import' in current_user.settings \
            and current_user.settings['entity_show_import']:
        data[_('imported from')] = link(info['project'])
        data[_('imported by')] = link(info['importer'])
        data['origin ID'] = info['origin_id']
    if 'entity_show_api' in current_user.settings \
            and current_user.settings['entity_show_api']:
        data['API'] = render_template('util/api_links.html', entity=entity)
    return data

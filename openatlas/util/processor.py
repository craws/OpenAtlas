from pathlib import Path
from typing import Union

from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField

from openatlas import app
from openatlas.util.util import get_file_extension


class GlobalSearchForm(FlaskForm):
    term = StringField('', render_kw={"placeholder": _('search term')})


@app.context_processor
def inject_template_functions() -> dict[str, Union[str, GlobalSearchForm]]:
    def get_logo() -> str:
        if g.settings['logo_file_id']:
            ext = get_file_extension(int(g.settings['logo_file_id']))
            if ext != 'N/A':
                return url_for(
                    'display_logo',
                    filename=f"{g.settings['logo_file_id']}{ext}")
        return str(Path('/static') / 'images' / 'layout' / 'logo.png')
    return dict(
        get_logo=get_logo(),
        search_form=GlobalSearchForm(prefix='global'))

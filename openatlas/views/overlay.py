# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.overlay import OverlayMapper
from openatlas.util.util import required_group, uc_first


class OverlayForm(Form):
    top_left_easting = FloatField('', [InputRequired()], render_kw={'autofocus': True})
    top_left_northing = FloatField('', [InputRequired()])
    bottom_right_easting = FloatField('', [InputRequired()])
    bottom_right_northing = FloatField('', [InputRequired()])
    save = SubmitField()


@app.route('/overlay/insert/<int:image_id>/<int:place_id>', methods=['POST', 'GET'])
@required_group('editor')
def overlay_insert(image_id: int, place_id: int) -> str:
    place = EntityMapper.get_by_id(place_id)
    image = EntityMapper.get_by_id(image_id)
    form = OverlayForm()
    if form.validate_on_submit():
        OverlayMapper.insert(form=form, image=image, place=place)
        return redirect(url_for('place_view', id_=place.id) + '#tab-file')
    form.save.label.text = uc_first(_('insert'))
    return render_template('overlay/insert.html', form=form, place=place, image=image)


@app.route('/overlay/update/<int:id_>', methods=['POST', 'GET'])
@required_group('editor')
def overlay_update(id_: int) -> str:
    overlay = OverlayMapper.get_by_id(id_)
    form = OverlayForm()
    if form.validate_on_submit():
        OverlayMapper.update(form=form, image_id=overlay.image_id, place_id=overlay.place_id)
        flash(_('info update'), 'info')
        return redirect(url_for('place_view', id_=overlay.place_id) + '#tab-file')
    bounding = ast.literal_eval(overlay.bounding_box)
    form.top_left_easting.data = bounding[0][0]
    form.top_left_northing.data = bounding[0][1]
    form.bottom_right_easting.data = bounding[1][0]
    form.bottom_right_northing.data = bounding[1][1]
    return render_template('overlay/update.html', form=form, overlay=overlay,
                           place=EntityMapper.get_by_id(overlay.place_id),
                           image=EntityMapper.get_by_id(overlay.image_id))


@app.route('/overlay/remove/<int:id_>/<int:place_id>')
@required_group('editor')
def overlay_remove(id_: int, place_id: int):
    OverlayMapper.remove(id_)
    return redirect(url_for('place_view', id_=place_id) + '#tab-file')

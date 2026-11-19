import ast
import math
from typing import Any

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import FloatField
from wtforms.validators import InputRequired, NumberRange

from openatlas import app
from openatlas.display.util import button, link, required_group
from openatlas.display.util2 import manual
from openatlas.forms.field import SubmitField
from openatlas.models.entity import Entity
from openatlas.models.overlay import Overlay


class OverlayForm(FlaskForm):
    top_left_easting = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lon_range)],
        render_kw={'autofocus': True})
    top_left_northing = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lat_range)])
    top_right_easting = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lon_range)])
    top_right_northing = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lat_range)])
    bottom_left_easting = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lon_range)])
    bottom_left_northing = FloatField(
        '',
        [InputRequired(), NumberRange(*Overlay.lat_range)])
    save = SubmitField(_('save'))

    def validate(self, extra_validators: Any = None) -> bool:
        valid = FlaskForm.validate(self, extra_validators=extra_validators)
        fields = (
            self.top_left_easting,
            self.top_left_northing,
            self.top_right_easting,
            self.top_right_northing,
            self.bottom_left_easting,
            self.bottom_left_northing)
        coords: list[float] = []
        for coord_field in fields:
            if (coord_field.data is None
                    or not math.isfinite(coord_field.data)):
                if coord_field.data is not None:
                    coord_field.errors = [
                        *coord_field.errors,
                        str(_('Invalid geom entered'))]
                valid = False
            else:
                coords.append(coord_field.data)
        if not valid:
            return False
        if not Overlay.has_nonzero_area([
                (coords[0], coords[1]),
                (coords[2], coords[3]),
                (coords[4], coords[5])]):
            self.top_left_easting.errors = [
                *self.top_left_easting.errors,
                str(_('Invalid geom entered'))]
            return False
        return True


@app.route(
    '/overlay/insert/<int:image_id>/<int:place_id>',
    methods=['GET', 'POST'])
@required_group('editor')
def overlay_insert(image_id: int, place_id: int) -> str | Response:
    form = OverlayForm()
    if form.validate_on_submit():
        Overlay.insert({
            'image_id': image_id,
            'top_left_northing': form.top_left_northing.data,
            'top_left_easting': form.top_left_easting.data,
            'top_right_northing': form.top_right_northing.data,
            'top_right_easting': form.top_right_easting.data,
            'bottom_left_northing': form.bottom_left_northing.data,
            'bottom_left_easting': form.bottom_left_easting.data})
        return redirect(f"{url_for('view', id_=place_id)}#tab-file")
    place = Entity.get_by_id(place_id)
    return render_template(
        'util/overlay.html',
        buttons=[manual('tools/map')],
        form=form,
        crumbs=[
            link(place, index=True),
            place,
            Entity.get_by_id(image_id),
            _('overlay')])


@app.route(
    '/overlay/update/<int:place_id>/<int:overlay_id>',
    methods=['GET', 'POST'])
@required_group('editor')
def overlay_update(place_id: int, overlay_id: int) -> str | Response:
    overlay = Overlay.get_by_id(overlay_id)
    place = Entity.get_by_id(place_id)
    form = OverlayForm()
    if form.validate_on_submit():
        Overlay.update({
            'image_id': overlay.image_id,
            'top_left_northing': form.top_left_northing.data,
            'top_left_easting': form.top_left_easting.data,
            'top_right_northing': form.top_right_northing.data,
            'top_right_easting': form.top_right_easting.data,
            'bottom_left_northing': form.bottom_left_northing.data,
            'bottom_left_easting': form.bottom_left_easting.data})
        flash(_('info update'))
        return redirect(f'{url_for('view', id_=place.id)}#tab-file')
    if not form.is_submitted():
        bounding = [[0, 0], [0, 0], [0, 0]]  # For data entered before 6.4.0
        bounding_values = ast.literal_eval(overlay.bounding_box)
        overlay_point_count = 3
        if len(bounding_values) == overlay_point_count:
            bounding = bounding_values
        form.top_left_easting.data = bounding[0][1]
        form.top_left_northing.data = bounding[0][0]
        form.top_right_easting.data = bounding[1][1]
        form.top_right_northing.data = bounding[1][0]
        form.bottom_left_easting.data = bounding[2][1]
        form.bottom_left_northing.data = bounding[2][0]
    return render_template(
        'util/overlay.html',
        form=form,
        overlay=overlay,
        entity=place,
        buttons=[
            manual('tools/map'),
            button(
                _('remove'),
                url_for('overlay_remove', id_=overlay.id, place_id=place.id),
                onclick=f"return confirm('{_('remove')}?');")],
        crumbs=[
            link(place, index=True),
            place,
            Entity.get_by_id(overlay.image_id),
            _('update overlay')])


@app.route('/overlay/remove/<int:id_>/<int:place_id>')
@required_group('editor')
def overlay_remove(id_: int, place_id: int) -> Response:
    Overlay.remove(id_)
    return redirect(f"{url_for('view', id_=place_id)}#tab-file")

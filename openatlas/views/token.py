from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from flask import (
    flash, g, make_response, redirect, render_template, request, url_for)
from flask_babel import lazy_gettext as _
from flask_login import login_required
from flask_wtf import FlaskForm
from werkzeug.wrappers import Response
from wtforms import SelectField, StringField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import HiddenField

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import button, link, required_group
from openatlas.display.util2 import manual, sanitize
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.token import Token
from openatlas.models.user import User


class GenerateTokenForm(FlaskForm):
    expiration = IntegerField(
        _('expiration'),
        default=30,
        description=_('expiration in days')
        + ', 0 = ' + _("no expiration date"))
    token_name = StringField(
        _('name'),
        default=f"Token_{datetime.today().strftime('%Y-%m-%d')}")
    user = SelectField(_('user'), choices=(), default=0, coerce=int)
    token_text = HiddenField()
    save = SubmitField(_('generate'))


class ListTokenForm(FlaskForm):
    user = SelectField(_('user'), choices=(), default=0, coerce=int)
    revoked = SelectField(
        _('revoked'),
        choices=(
            ('all', _('all')),
            ('true', _('revoked')),
            ('false', _('not revoked'))))
    valid = SelectField(
        _('valid'),
        choices=(
            ('all', _('all')),
            ('>', _('valid')),
            ('<', _('not valid'))))
    save = SubmitField(_('apply'))


@app.route('/admin/api_token', methods=['GET', 'POST'])
@app.route('/admin/api_token/<int:user_id>', methods=['GET', 'POST'])
@required_group('admin')
def api_token(user_id: int = 0) -> str | Response:
    form = ListTokenForm()
    form.user.choices = [(0, _('all'))] + User.get_users_for_form()
    user_id = user_id or 0
    revoked = 'all'
    valid = 'all'
    if form.validate_on_submit():
        user_id = int(form.user.data)
        revoked = form.revoked.data
        valid = form.valid.data
    form.user.data = user_id
    tabs = {
        'token': Tab(
            'token',
            content=display_form(form),
            buttons=[manual('admin/api')])}
    tabs['token'].buttons.append(
        button(_('generate'), url_for('generate_token')))
    tabs['token'].buttons.append(
        button(
            _('revoke all tokens'),
            url_for('revoke_all_tokens'),
            onclick=f"return confirm('{_('revoke all tokens')}?')"))
    tabs['token'].buttons.append(
        button(
            _('authorize all tokens'),
            url_for('authorize_all_tokens'),
            onclick=f"return confirm('{_('authorize all tokens')}?')"))
    tabs['token'].buttons.append(
        button(
            _('delete revoked tokens'),
            url_for('delete_revoked_tokens'),
            onclick=f"return confirm('{_('delete all revoked tokens')}?')"))
    tabs['token'].buttons.append(
        button(
            _('delete invalid tokens'),
            url_for('delete_invalid_tokens'),
            onclick=f"return confirm('{_('delete all invalid tokens')}?')"))
    token_table = Table([
        _('valid'),
        _('name'),
        'jti',
        _('valid from'),
        _('valid until'),
        _('user'),
        _('creator'),
        _('revoked')])
    for token in Token.get_tokens(user_id, revoked, valid):
        delete_link = link(
            _('delete'),
            url_for('delete_token', id_=token['id']),
            js="return confirm('" + _('delete') + "?')")
        revoke_link = link(
            _('revoke'),
            url_for('revoke_token', id_=token['id']))
        if token['revoked']:
            revoke_link = link(
                _('authorize'),
                url_for('authorize_token', id_=token['id']))
        user = User.get_by_id_without_bookmarks(token['user_id'])
        token_table.rows.append([
            get_token_valid_column(token, user),
            token['name'],
            token['jti'],
            token['valid_from'],
            token['valid_until'],
            link(user),
            link(User.get_by_id_without_bookmarks(token['creator_id'])),
            token['revoked'],
            revoke_link,
            delete_link])
    tabs['token'].table = token_table
    return render_template(
        'tabs.html',
        tabs=tabs,
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}"],
            _('token')])


def get_token_valid_column(token: dict[str, Any], user: User) -> str:
    html = '<span class="text-success bg-success">OK</span>'
    if not Token.is_valid(token, user):
        html = '<span class="text-danger bg-danger">NO</span>'
    return html


@app.route('/admin/api_token/generate_token', methods=['GET', 'POST'])
@required_group('admin')
def generate_token() -> str | Response:
    form = GenerateTokenForm()
    form.user.choices = User.get_users_for_form()
    if form.validate_on_submit():
        expiration = form.expiration.data
        token_name = sanitize(form.token_name.data)
        user_ = User.get_by_id_without_bookmarks(int(form.user.data))
        token = ''
        Transaction.begin()
        try:
            token = Token.generate_token(expiration, token_name, user_)
            Transaction.commit()
            flash(f"{_('token stored for')}: {user_.username}", 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        response = make_response(redirect(url_for('generate_token')))
        response.set_cookie(
            'jwt_token',
            token,
            httponly=True,
            secure=True,
            max_age=timedelta(seconds=1))
        return response
    form.token_text.data = request.cookies.get('jwt_token')
    return render_template(
        'content.html',
        content=display_form(form, manual_page='admin/api'),
        title=_('admin'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}"],
            [_('token'), f"{url_for('api_token')}"],
            _('generate')])


@app.route('/admin/api_token/revoke_token/<int:id_>')
@login_required
def revoke_token(id_: int) -> str | Response:
    Token.revoke_jwt_token(id_)
    flash(_('token revoked'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/authorize_token/<int:id_>')
@login_required
def authorize_token(id_: int) -> str | Response:
    Token.authorize_jwt_token(id_)
    flash(_('token authorized'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/delete_token/<int:id_>')
@login_required
def delete_token(id_: int) -> str | Response:
    Token.delete_token(id_)
    flash(_('token deleted'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/delete_revoked_tokens/')
@login_required
def delete_revoked_tokens() -> str | Response:
    Token.delete_all_revoked_tokens()
    flash(_('tokens deleted'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/delete_invalid_tokens/')
@login_required
def delete_invalid_tokens() -> str | Response:
    Token.delete_invalid_tokens()
    flash(_('tokens deleted'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/revoke_all_tokens/')
@login_required
def revoke_all_tokens() -> str | Response:
    Token.revoke_all_tokens()
    flash(_('all tokens revoked'), 'info')
    return redirect(f"{url_for('api_token')}")


@app.route('/admin/api_token/authorize_all_tokens/')
@login_required
def authorize_all_tokens() -> str | Response:
    Token.authorize_all_tokens()
    flash(_('all tokens authorized'), 'info')
    return redirect(f"{url_for('api_token')}")

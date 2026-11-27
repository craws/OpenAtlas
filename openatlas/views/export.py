import json
import os
from pathlib import Path
from typing import Any

import click
from flask import (
    abort, flash, g, jsonify, render_template, request, send_from_directory,
    url_for)
from flask_babel import gettext as _
from flask_wtf.csrf import generate_csrf
from markupsafe import escape
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import button, display_info, link, required_group
from openatlas.display.util2 import (
    convert_size, is_authorized, manual, uc_first)
from openatlas.models.arche_worker import (
    ACTIVE_STATUSES, get_arche_export_status, run_arche_export_job,
    start_arche_export_subprocess)
from openatlas.models.export import (
    rdf_export, sql_export, validate_case_study_ids, validate_license_ids)

ARCHE_POLL_INTERVAL_MS = 5000


def post_button(
        label: str,
        url: str,
        variant: str = 'primary',
        disabled: bool = False) -> str:
    token = escape(generate_csrf())
    css = app.config['CSS']['button'][variant]
    disabled_attr = ' disabled' if disabled else ''
    return (
        f'<form method="post" action="{escape(url)}" class="d-inline">'
        f'<input type="hidden" name="csrf_token" value="{token}">'
        f'<button type="submit" class="{css}"{disabled_attr}>'
        f'{escape(uc_first(label))}</button></form>')


def delete_post_form(url: str, confirm_text: str) -> str:
    token = escape(generate_csrf())
    return (
        f'<form method="post" action="{escape(url)}" class="d-inline" '
        f'onsubmit="return confirm(this.dataset.confirm)" '
        f'data-confirm="{escape(confirm_text)}">'
        f'<input type="hidden" name="csrf_token" value="{token}">'
        f'<button type="submit" class="btn btn-link p-0 align-baseline">'
        f'{escape(uc_first(_("delete")))}</button></form>')


def escape_optional(value: object) -> str:
    return str(escape(value)) if value else ''


def format_arche_id_list(
        configured_ids: list[Any] | None,
        valid_ids: set[int],
        invalid_label: str) -> str:
    items: list[str] = []
    for raw_id in configured_ids or []:
        if (not isinstance(raw_id, bool)
                and isinstance(raw_id, int)
                and raw_id in valid_ids):
            items.append(link(str(raw_id), url_for('view', id_=raw_id)))
        else:
            items.append(
                f'<span class="text-danger">{escape(str(raw_id))} '
                f'({escape(invalid_label)})</span>')
    return ', '.join(items)


def get_export_path(view: str) -> Path:
    match view:
        case 'arche':
            return app.config['ARCHE_PATH']
        case 'rdf':
            return app.config['RDF_PATH']
        case 'sql':
            return app.config['SQL_PATH']
        case _:
            abort(404)


@app.route('/download/export/<view>/<filename>')
@required_group('manager')
def download_export(view: str, filename: str) -> Response:
    if filename.startswith('.'):
        abort(404)
    return send_from_directory(
        get_export_path(view),
        filename,
        as_attachment=True)


@app.route('/delete_export/<view>/<filename>', methods=['POST'])
@required_group('admin')
def delete_export(view: str, filename: str) -> Response:
    base_path = get_export_path(view).resolve()
    try:
        target = (base_path / filename).resolve()
        if filename.startswith('.') or target.parent != base_path:
            raise ValueError(f'Invalid export filename: {filename}')
        target.unlink()
        g.logger.log('info', 'file', f'{view.upper()} file deleted')
        flash(_('file deleted'))
    except Exception as e:
        g.logger.log(
            'error',
            'file',
            f'{view.upper()} file deletion failed',
            e)
        flash(_('error file delete'), 'error')
    return redirect(f'{url_for('export_'+view)}#tab-export')


@app.route('/export/execute/<format_>', methods=['POST'])
@required_group('manager')
def export_execute(format_: str) -> Response:
    if os.access(app.config['SQL_PATH'], os.W_OK):
        if sql_export(format_):
            g.logger.log('info', 'database', 'SQL export')
            flash(_('data was exported'))
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'SQL export failed')
            flash(_('export failed'), 'error')
    return redirect(f"{url_for('export_sql')}#tab-export")


@app.route('/export/sql')
@required_group('manager')
def export_sql() -> str:
    return render_template(
        'tabs.html',
        tabs={
            'export': Tab(
                'export',
                _('export'),
                content=build_export_table('sql').display(),
                buttons=[
                    manual('admin/export'),
                    post_button(
                        _('export SQL'),
                        url_for('export_execute', format_='sql')),
                    post_button(
                        _('export database dump'),
                        url_for('export_execute', format_='dump'))])},
        title=_('export SQL'),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            _('export SQL')])


def render_arche_status_banner(status: dict[str, Any]) -> str:
    state = str(status.get('status', 'idle'))
    banner = ''
    if state in ACTIVE_STATUSES:
        started = escape_optional(status.get('started_at'))
        started_info = f' ({started})' if started else ''
        msg = escape(_('ARCHE export is running in the background.'))
        status_url = json.dumps(url_for('arche_export_status'))
        banner = (
            f'<div class="alert alert-info" role="status">'
            f'{msg}{started_info}</div>'
            f'<script>(function(){{'
            f'var u={status_url};'
            f'var t=setInterval(function(){{'
            f'fetch(u,{{credentials:"same-origin"}})'
            f'.then(function(r){{return r.json();}})'
            f'.then(function(d){{'
            f'if(d.status!=="starting"&&d.status!=="running"){{'
            f'clearInterval(t);window.location.reload();}}'
            f'}}).catch(function(){{}});'
            f'}},{ARCHE_POLL_INTERVAL_MS});'
            f'}})();</script>')
    elif state == 'done':
        filename = escape_optional(status.get('filename'))
        duration = status.get('duration_seconds')
        duration_info = (
            f' ({escape(str(duration))}s)'
            if duration is not None else '')
        msg = escape(_('Last ARCHE export finished:'))
        banner = (
            f'<div class="alert alert-success" role="status">'
            f'{msg} {filename}{duration_info}</div>')
    elif state == 'failed':
        error = escape_optional(status.get('error'))
        msg = escape(_('Last ARCHE export failed:'))
        error_part = f' {error}' if error else ''
        banner = (
            f'<div class="alert alert-danger" role="alert">'
            f'{msg}{error_part}</div>')
    return banner


@app.route('/export/arche/status')
@required_group('manager')
def arche_export_status() -> Response:
    return jsonify(get_arche_export_status())


@app.route('/export/arche')
@required_group('manager')
def export_arche() -> str:
    metadata = app.config['ARCHE_METADATA']
    status = get_arche_export_status()
    is_running = status.get('status') in ACTIVE_STATUSES
    valid_case_study_ids, _unused_case_studies = validate_case_study_ids(
        metadata.get('caseStudyIds'))
    valid_exclude_license_ids, _unused_licenses = validate_license_ids(
        metadata.get('excludeLicenseIds'))
    info_content = {
        'projectAcronym': escape_optional(metadata.get('projectAcronym')),
        'topCollection': escape_optional(metadata.get('topCollection')),
        'description': escape_optional(metadata.get('description')),
        'language': escape_optional(metadata.get('language')),
        'depositor': escape_optional(
            ', '.join(metadata.get('depositor', []))),
        'acceptedDate': escape_optional(metadata.get('acceptedDate')),
        'submissionDate': escape_optional(metadata.get('submissionDate')),
        'curator': escape_optional(', '.join(metadata.get('curator', []))),
        'editor': escape_optional(', '.join(metadata.get('editor', []))),
        'contact': escape_optional(', '.join(metadata.get('contact', []))),
        'owner': escape_optional(', '.join(metadata.get('owner', []))),
        'rightsHolder':
            escape_optional(', '.join(metadata.get('rightsHolder', []))),
        'licensor': escape_optional(', '.join(metadata.get('licensor', []))),
        'principalInvestigator': escape_optional(
            ', '.join(metadata.get('principalInvestigator', []))),
        'hasMetadataCreator': escape_optional(
            ', '.join(metadata.get('hasMetadataCreator', []))),
        'relatedDiscipline': escape_optional(
            ', '.join(metadata.get('relatedDiscipline', []))),
        'subject': escape_optional(', '.join(metadata.get('subject', []))),
        'licenseSummary': escape_optional(metadata.get('licenseSummary')),
        'datasetLicense': escape_optional(metadata.get('datasetLicense')),
        'lifeCycleStatus': escape_optional(metadata.get('lifeCycleStatus')),
        'url': escape_optional(metadata.get('url')),
        'excludeReferenceSystems': escape_optional(
            ', '.join(metadata.get('excludeReferenceSystems', []))),
        'caseStudyIds': format_arche_id_list(
            metadata.get('caseStudyIds'),
            set(valid_case_study_ids),
            _('not a case study')),
        'excludeLicenseIds': format_arche_id_list(
            metadata.get('excludeLicenseIds'),
            valid_exclude_license_ids,
            _('not a license'))}
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'info',
                content=display_info(info_content),
                buttons=[
                    manual('admin/export'),
                    button(
                        f'ARCHE {_('file checker')}',
                        url_for('check_files', arche='arche'))]),
            'export': Tab(
                'export',
                _('export'),
                content=(
                    render_arche_status_banner(status)
                    + build_export_table('arche').display()),
                buttons=[
                    manual('admin/export'),
                    post_button(
                        f'{_('export')} ARCHE',
                        url_for('arche_execute'),
                        disabled=is_running)
                    if is_authorized('admin') else ''])},
        title=f'{_('export')} ARCHE',
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            f'{_('export')} ARCHE'])


@app.route('/export/arche/execute', methods=['POST'])
@required_group('admin')
def arche_execute() -> Response:
    arche_path = app.config['ARCHE_PATH']
    if not os.access(arche_path, os.W_OK):  # pragma: no cover
        g.logger.log(
            'error',
            'database',
            f'ARCHE directory not writable: {arche_path}')
        flash(_('directory not writable'), 'error')
        return redirect(f"{url_for('export_arche')}#tab-export")
    if get_arche_export_status().get('status') in ACTIVE_STATUSES:
        flash(_('ARCHE export is already running'), 'info')
        return redirect(f"{url_for('export_arche')}#tab-export")
    if app.testing and not app.config.get('ARCHE_EXPORT_ASYNC', False):
        try:
            result = run_arche_export_job(base_url=request.url_root)
            if result is None:
                flash(_('ARCHE export is already running'), 'info')
            else:
                flash(_('data was exported'))
        except Exception:  # pragma: no cover
            flash(_('export failed'), 'error')
    else:  # pragma: no cover
        try:
            start_arche_export_subprocess(request.url_root)
            flash(_('ARCHE export started in background'), 'info')
        except Exception as e:
            g.logger.log(
                'error', 'database', 'ARCHE export start failed', e)
            flash(_('export failed'), 'error')
    return redirect(f"{url_for('export_arche')}#tab-export")


@app.cli.command('arche-export')
@click.option('--base-url', default='http://localhost/')
def arche_export_command(base_url: str) -> None:
    result = run_arche_export_job(base_url=base_url)
    if result is None:
        click.echo('ARCHE export is already running.', err=True)
        raise SystemExit(1)
    click.echo(f'ARCHE export completed: {result}')


@app.route('/export/rdf')
@required_group('manager')
def export_rdf() -> str:
    return render_template(
        'tabs.html',
        tabs={
            'export': Tab(
                'export',
                _('export'),
                content=build_export_table('rdf').display(),
                buttons=[
                    manual('admin/export'),
                    post_button(
                        f'{_('export')} RDF/NT',
                        url_for('rdf_execute'))])},
        title=f'{_('export')} RDF',
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            f'{_('export')} RDF'])


@app.route('/export/rdf/execute', methods=['POST'])
@required_group('manager')
def rdf_execute() -> Response:
    if os.access(app.config['RDF_PATH'], os.W_OK):
        if rdf_export():
            g.logger.log('info', 'database', 'RDF export')
            flash(_('data was exported'))
        else:  # pragma: no cover
            g.logger.log('error', 'database', 'RDF export failed')
            flash(_('export failed'), 'error')
    return redirect(f"{url_for('export_rdf')}#tab-export")


def build_export_table(view: str) -> Table:
    path = get_export_path(view)
    table = Table(['name', 'size'], order=[[0, 'desc']])
    if not path.is_dir():  # pragma: no cover
        return table
    for file in path.iterdir():
        if not file.is_file() or file.name.startswith('.'):
            continue
        data = [
            str(escape(file.name)),
            convert_size(file.stat().st_size),
            link(
                _('download'),
                url_for('download_export', view=view, filename=file.name))]
        if is_authorized('admin') and os.access(path, os.W_OK):
            data.append(
                delete_post_form(
                    url_for('delete_export', view=view, filename=file.name),
                    _('delete %(name)s?', name=file.name)))
        table.rows.append(data)
    return table

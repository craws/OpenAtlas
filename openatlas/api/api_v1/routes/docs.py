from flask import abort, render_template

from openatlas import app


@app.route('/api/1/docs/<doc_type>')
def api_reference(doc_type: str) -> str:
    if doc_type != 'swagger':
        abort(404)

    return render_template(f'api_docs/{doc_type}.html')

from flask import render_template
from openatlas import app


@app.route('/content')
def content_index():
    return render_template('content/index.html')

from flask import render_template_string

from openatlas import app


@app.route('/api/1/docs/redoc')
def redoc_api_reference() -> str:
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>OpenAtlas V1 - ReDoc</title>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>body { margin: 0; padding: 0; }</style>
    </head>
    <body>
      <redoc spec-url="/api/1/docs/openapi.json"></redoc>
      <script src="{{ url_for('static', filename='node_modules/redoc/bundles/redoc.standalone.js', v=config.VERSION) }}"></script>
    </body>
    </html>
    """
    return render_template_string(template)


@app.route('/api/1/docs/swagger')
def custom_swagger_ui() -> str:
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>OpenAtlas V1 - Swagger UI</title>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <link rel="stylesheet" href="{{ url_for('static', filename='node_modules/swagger-ui-dist/swagger-ui.css', v=config.VERSION) }}" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="{{ url_for('static', filename='node_modules/swagger-ui-dist/swagger-ui-bundle.js', v=config.VERSION) }}"></script>
      <script>
        window.onload = () => {
          window.ui = SwaggerUIBundle({
            url: '/api/1/docs/openapi.json',
            dom_id: '#swagger-ui',
          });
        };
      </script>
    </body>
    </html>
    """
    return render_template_string(template)


@app.route('/api/1/docs/scalar')
def scalar_api_reference() -> str:
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>OpenAtlas V1 - Scalar</title>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>
        body { margin: 0; padding: 0; }
      </style>
    </head>
    <body>
      <script
        id="api-reference"
        data-url="/api/1/docs/openapi.json">
      </script>
      <script src="{{ url_for('static', filename='node_modules/@scalar/api-reference/dist/browser/standalone.js', v=config.VERSION) }}"></script>
    </body>
    </html>
    """
    return render_template_string(template)

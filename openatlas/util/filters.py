import jinja2
import flask

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def uc_first(self, string):
    return string[0].upper() + string[1:]

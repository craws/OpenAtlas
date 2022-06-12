from openatlas.forms.base_form import BaseForm


class AcquisitionForm(BaseForm):
    fields = ['name', 'date', 'description', 'continue']

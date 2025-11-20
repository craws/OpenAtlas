from openatlas import app
from openatlas.models.entity import Entity

with app.test_request_context():
    app.preprocess_request()
    for text in Entity.get_by_class('source_translation', True):
        if "Simplified transcription of" in text.name:
            text.delete()
        if "Corrected transcription of" in text.name:
            new_name = text.name.replace("Corrected transcription", "Edition")
            text.update_attributes({'name': new_name})
        if "Transcription of" in text.name:
            new_name = text.name.replace("Transcription", "Diplomatic")
            text.update_attributes({'name': new_name})

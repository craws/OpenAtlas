SERVER_NAME = 'local.host'
DATABASE_NAME = 'openatlas_test'
DATABASE_PASS = 'CHANGE ME'
DEBUG = True

# Disable CSRF
WTF_CSRF_ENABLED = False
WTF_CSRF_METHODS: list[str] = []

ARCHE = {
    'id': 0,
    'collection_ids': [0],
    'base_url': 'https://arche-curation.acdh-dev.oeaw.ac.at/',
    'thumbnail_url': 'https://arche-thumbnails.acdh.oeaw.ac.at/'}


ARCHE_METADATA = {
            'topCollection': 'test collection',
            'language': 'en',
            'depositor': 'Sauron',
            'acceptedDate': "2024-01-01",
            'curator': ['Frodo', 'Sam'],
            'principalInvestigator': ['Gandalf'],
            'hasMetadataCreator': ['Gimli'],
            'relatedDiscipline':
                ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003'],
            'typeIds': [],
            'excludeReferenceSystems': []}

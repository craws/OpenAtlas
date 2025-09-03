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
    'topCollection': 'OpenAtlas Test Collection',
    'language': 'en',
    'depositor': ['Alice', 'https://orcid.org/0000-0001-7608-7446'],
    'acceptedDate': "2024-01-01",
    'hasMetadataCreator': ['https://orcid.org/0000-0003-2576-2266',
                           'https://orcid.org/0000-0001-7608-7446', 'Alice'],
    'curator': [
        'https://orcid.org/0000-0003-2576-2266',
        'https://orcid.org/0000-0002-4911-8451',
        'Alice'],
    'principalInvestigator': [
        'Stefan',
        'https://orcid.org/0000-0003-2576-2266',
        'https://orcid.org/0000-0002-4911-8451'],
    'relatedDiscipline':
        ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003',
         'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/602001'],
    'typeIds': [],
    'excludeReferenceSystems': []}

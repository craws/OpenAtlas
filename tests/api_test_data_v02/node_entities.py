class NodeEntities:
    @staticmethod
    def get_test_node_entities(params):
        return {'nodes': [
            {'id': params['austria_id'],
         'label': 'Austria',
         'url': 'http://local.host/api/0.2/entity/84'},
        {'id': params['czech_republic_id'],
         'label': 'Czech Republic',
         'url': 'http://local.host/api/0.2/entity/89'},
        {'id': params['germany_id'],
         'label': 'Germany',
         'url': 'http://local.host/api/0.2/entity/87'},
        {'id': params['italy_id'],
         'label': 'Italy',
         'url': 'http://local.host/api/0.2/entity/88'},
        {'id': params['slovakia_id'],
         'label': 'Slovakia',
         'url': 'http://local.host/api/0.2/entity/90'},
        {'id': params['slovenia_id'],
         'label': 'Slovenia',
         'url': 'http://local.host/api/0.2/entity/91'}]}

    @staticmethod
    def get_test_node_entities_all(params):
        return {'nodes': [
        {'id': params['austria_id'],
         'label': 'Austria',
         'url': 'http://local.host/api/0.2/entity/84'},
        {'id': params['czech_republic_id'],
         'label': 'Czech Republic',
         'url': 'http://local.host/api/0.2/entity/89'},
        {'id': params['germany_id'],
         'label': 'Germany',
         'url': 'http://local.host/api/0.2/entity/87'},
        {'id': params['italy_id'],
         'label': 'Italy',
         'url': 'http://local.host/api/0.2/entity/88'},
        {'id': params['slovakia_id'],
         'label': 'Slovakia',
         'url': 'http://local.host/api/0.2/entity/90'},
        {'id': params['slovenia_id'],
         'label': 'Slovenia',
         'url': 'http://local.host/api/0.2/entity/91'},
        {'id': params['niederösterreich_id'],
         'label': 'Niederösterreich',
         'url': 'http://local.host/api/0.2/entity/86'},
        {'id': params['wien_id'],
         'label': 'Wien',
         'url': 'http://local.host/api/0.2/entity/85'}]}

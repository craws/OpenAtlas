class NodeEntities:
    @staticmethod
    def get_test_node_entities(params):
        return {'nodes': [{
            'id': params['austria_id'],
            'label': 'Austria',
            'url': f'http://local.host/api/0.3/entity/{params["austria_id"]}'}, {
            'id': params['czech_republic_id'],
            'label': 'Czech Republic',
            'url': f'http://local.host/api/0.3/entity/{params["czech_republic_id"]}'}, {
            'id': params['germany_id'],
            'label': 'Germany',
            'url': f'http://local.host/api/0.3/entity/{params["germany_id"]}'}, {
            'id': params['italy_id'],
            'label': 'Italy',
            'url': f'http://local.host/api/0.3/entity/{params["italy_id"]}'}, {
            'id': params['slovakia_id'],
            'label': 'Slovakia',
            'url': f'http://local.host/api/0.3/entity/{params["slovakia_id"]}'}, {
            'id': params['slovenia_id'],
            'label': 'Slovenia',
            'url': f'http://local.host/api/0.3/entity/{params["slovenia_id"]}'}]}

    @staticmethod
    def get_test_node_entities_all(params):
        return {'nodes': [
            {'id': params['austria_id'],
             'label': 'Austria',
             'url': f'http://local.host/api/0.3/entity/{params["austria_id"]}'},
            {'id': params['czech_republic_id'],
             'label': 'Czech Republic',
             'url': f'http://local.host/api/0.3/entity/{params["czech_republic_id"]}'},
            {'id': params['germany_id'],
             'label': 'Germany',
             'url': f'http://local.host/api/0.3/entity/{params["germany_id"]}'},
            {'id': params['italy_id'],
             'label': 'Italy',
             'url': f'http://local.host/api/0.3/entity/{params["italy_id"]}'},
            {'id': params['slovakia_id'],
             'label': 'Slovakia',
             'url': f'http://local.host/api/0.3/entity/{params["slovakia_id"]}'},
            {'id': params['slovenia_id'],
             'label': 'Slovenia',
             'url': f'http://local.host/api/0.3/entity/{params["slovenia_id"]}'},
            {'id': params['niederösterreich_id'],
             'label': 'Niederösterreich',
             'url': f'http://local.host/api/0.3/entity/{params["niederösterreich_id"]}'},
            {'id': params['wien_id'],
             'label': 'Wien',
             'url': f'http://local.host/api/0.3/entity/{params["wien_id"]}'}]}

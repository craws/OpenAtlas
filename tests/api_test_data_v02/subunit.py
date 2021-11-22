class Subunits:
    @staticmethod
    def get_test_subunit(params):
        return {
            'nodes': [{
            'id': params["home_id"], 'label': 'Home of Baggins',
            'url': f'http://local.host/api/0.2/entity/{params["home_id"]}'}]}

    @staticmethod
    def get_test_subunit_hierarchy(params):
        return {
            'nodes': [{
                'id': params["home_id"], 'label': 'Home of Baggins',
            'url': f'http://local.host/api/0.2/entity/{params["home_id"]}'}, {
            'id': params["kitchen_id"], 'label': 'Kitchen',
            'url': f'http://local.host/api/0.2/entity/{params["kitchen_id"]}'}]}

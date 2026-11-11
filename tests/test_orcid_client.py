import unittest
from unittest.mock import Mock, patch

import requests

from openatlas.api.external import orcid


def response(data, status=200):
    result = Mock(status_code=status)
    result.json.return_value = data
    if status >= 400:
        result.raise_for_status.side_effect = requests.HTTPError()
    return result


class TestORCIDClient(unittest.TestCase):

    def setUp(self):
        orcid._token = None
        orcid._expires = 0
        orcid._credentials = None
        self.config = patch.dict(orcid.app.config, {
            'ORCID_CLIENT_ID': 'client',
            'ORCID_CLIENT_SECRET': 'secret',
            'USER_AGENT': {},
            'PROXIES': {}})
        self.config.start()
        self.addCleanup(self.config.stop)

    @patch.object(orcid.requests, 'get')
    @patch.object(orcid.requests, 'post')
    def test_search_cache_and_cleaning(self, post, get):
        post.return_value = response({'access_token': 'token'})
        get.return_value = response({'expanded-result': [{
            'orcid-id': '0000-0001-7608-7446',
            'given-names': 'Alice', 'family-names': 'Smith',
            'institution-name': ['One', 'Two', 'Three']}]})
        expected = [{'id': '0000-0001-7608-7446', 'label': 'Alice Smith (One, Two)',
                     'info': '', 'detail': ''}]
        self.assertEqual(orcid.search('  Ali:ce\t Smith*  '), expected)
        self.assertEqual(orcid.search('Alice'), expected)
        self.assertEqual(post.call_count, 1)
        self.assertEqual(get.call_args_list[0].args[0],
                         'https://pub.orcid.org/v3.0/expanded-search/')
        self.assertEqual(get.call_args_list[0].kwargs['params'], {
            'q': '(given-names:Alice* OR family-names:Alice* OR credit-name:Alice*) AND '
                 '(given-names:Smith* OR family-names:Smith* OR credit-name:Smith*)',
            'rows': 15})

    @patch.object(orcid.requests, 'get')
    @patch.object(orcid.requests, 'post')
    def test_search_configuration_and_request_failures(self, post, get):
        orcid.app.config['ORCID_CLIENT_ID'] = ''
        self.assertEqual(orcid.search('Alice'), [])
        post.assert_not_called()
        orcid.app.config['ORCID_CLIENT_ID'] = 'client'
        post.side_effect = requests.RequestException('token error')
        self.assertEqual(orcid.search('Alice'), [])
        post.side_effect = None
        post.return_value = response({'access_token': 'token'})
        get.side_effect = requests.RequestException('search error')
        self.assertEqual(orcid.search('Alice'), [])

    @patch.object(orcid.requests, 'get')
    @patch.object(orcid.requests, 'post')
    def test_unauthorized_refreshes_once(self, post, get):
        post.side_effect = [response({'access_token': 'old', 'expires_in': 3600}),
                            response({'access_token': 'new', 'expires_in': 3600})]
        get.side_effect = [response({}, 401), response({'expanded-result': None})]
        self.assertEqual(orcid.search('Alice'), [])
        self.assertEqual(post.call_count, 2)
        self.assertEqual(get.call_args_list[1].kwargs['headers']['Authorization'],
                         'Bearer new')

    @patch.object(orcid, '_request')
    def test_info_and_empty_search(self, request):
        self.assertEqual(orcid.search(' :* '), [])
        request.assert_not_called()
        request.return_value = {'name': {'given-names': {'value': 'Alice'},
                                         'family-name': {'value': 'Smith'}}}
        result = orcid.ORCID.get_info('0000-0001-7608-7446', None)
        self.assertEqual(result['title'], 'Alice Smith')
        self.assertIn('https://orcid.org/0000-0001-7608-7446', result['ORCID ID'])
        self.assertEqual(orcid.ORCID.get_info('../bad', None), {})


if __name__ == '__main__':
    unittest.main()
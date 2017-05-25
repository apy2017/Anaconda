from technobot import TechnoBot
from technobot import api
import config
import unittest
import json
from unittest.mock import patch, Mock
import requests


class FakeResponse:
    def __init__(self, code, return_json=None):
        self.code = code
        self.return_json = return_json

    @property
    def status_code(self):
        return self.code

    def json(self):
        return json.loads(self.return_json)


class TechBotTest(unittest.TestCase):
    def setUp(self):
        self.bot = TechnoBot(config.token)
        self.host = 'localhost'
        self.url = 'http://{0}'.format(self.host)
        pass

    @patch('requests.get', Mock(return_value=FakeResponse(153,'{"description" : "test"}')))
    def testApi(self):
        self.assertRaises(api.TelegramApiException, api._make_request, config.token, 'getMe')

    @patch('requests.get', Mock(return_value=FakeResponse(200, '{"ok": false, '
                                                               '"error_code" : 123, '
                                                               '"description" : 12, '
                                                               '"result" : {}}')))
    def testOk(self):
        self.assertRaises(api.TelegramApiException, api._make_request, config.token, 'getMe')

    def get_url(self, tail):
        return '{base}/api/v0/{tail}'.format(base=self.url, tail=tail)

    def testPolls(self):
        requests_url = self.get_url('polls/12345678/')
        response = requests.get(requests_url)
        self.assertEqual(response.status_code, 200)

    def testCode(self):
        requests_url = self.get_url('polls/1278/')
        response = requests.get(requests_url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TechBotTest)
    unittest.TextTestRunner().run(suite)
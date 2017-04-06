from technobot import TechnoBot
from technobot import api
import config
import unittest
import json
from unittest.mock import patch, Mock


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
        pass

    @patch('requests.get', Mock(return_value=FakeResponse(153)))
    def testApi(self):
        self.assertRaises(api.TelegramApiException, api._make_request, config.token, 'getMe')

    @patch('requests.get', Mock(return_value=FakeResponse(200, '{"ok": false, '
                                                               '"error_code" : 123, '
                                                               '"description" : 12, '
                                                               '"result" : {}}')))
    def testOk(self):
        self.assertRaises(api.TelegramApiException, api._make_request, config.token, 'getMe')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TechBotTest)
    unittest.TextTestRunner().run(suite)
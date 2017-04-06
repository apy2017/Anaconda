import requests


class TelegramApiException(BaseException):
    pass

BASE_URL = 'https://api.telegram.org/bot{token}/{method_name}'


def _make_request(token, method_name, params=None):
    request_url = BASE_URL.format(token=token, method_name=method_name)
    request_result = requests.get(request_url, params=params)
    return _parse_response(request_result)


def _parse_response(request_result):
    if request_result.status_code != 200:
        message = 'Server returns code: {code}'
        raise TelegramApiException(message.format(code=request_result.status_code))
    try:
        result = request_result.json()
    except:
        message = 'Invalid JSON returned from server:\n{request_text}'
        raise TelegramApiException(message.format(request_text=request_result.text()))

    if not result['ok']:
        message = 'Telegram Error {code} : {description}'
        raise TelegramApiException(message.format(code=result['error_code'], description=result['description']))

    return result['result']


def get_me(token):
    return _make_request(token, 'getMe')


def send_message(token, chat_id, text, *args):
    parsed_params = {'chat_id': chat_id, 'text': text}
    return _make_request(token, 'sendMessage', parsed_params)


def get_updates(token, offset=None, limit=None, timeout=None, allowed_updates=None):
    return _make_request(token, 'getUpdates')
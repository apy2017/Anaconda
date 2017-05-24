import requests
try:
    from requests.packages.urllib3 import fields
except ImportError:
    fields = None


class TelegramApiException(BaseException):
    pass

BASE_URL = 'https://api.telegram.org/bot{token}/{method_name}'


def _make_request(token, method_name, params=None, files=None):
    if files and fields:
        fields.format_header_param = _no_encode(fields.format_header_param)
    request_url = BASE_URL.format(token=token, method_name=method_name)
    request_result = requests.get(request_url, params=params, files=files)
    return _parse_response(request_result)


def _parse_response(request_result):
    if request_result.status_code != 200:
        message = 'Server returns code: {code} {description}'
        raise TelegramApiException(message.format(code=request_result.status_code, description=request_result.json()['description']))
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


def send_message(token, chat_id, text, **kwargs):
    parsed_params = {'chat_id': chat_id, 'text': text}
    if 'reply_markup' in kwargs:
        parsed_params['reply_markup'] = kwargs['reply_markup'].json
    return _make_request(token, 'sendMessage', parsed_params)


def get_updates(token, offset=None, limit=None, timeout=None, allowed_updates=None):
    parsed_params = {}
    if offset is not None:
        parsed_params['offset'] = offset
    return _make_request(token, 'getUpdates', parsed_params)


def set_webhook(token, url=None, certificate=None, max_connections=None, allowed_updates=None):
    payload = {
        'url': url if url else "",
    }
    files = None
    if certificate:
        files = {'certificate': certificate}

    return _make_request(token, 'setWebhook', params=payload, files=files)


def delete_webhook(token):
    return _make_request(token, 'deleteWebhook')


def _no_encode(func):
    def wrapper(key, val):
        if key == 'filename':
            return '{0}={1}'.format(key, val)
        else:
            return func(key, val)
    return wrapper
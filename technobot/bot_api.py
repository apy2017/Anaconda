import requests


class TechbotApiException(BaseException):
    pass


BASE_URL = 'http://localhost/api/v0/{tail}'


def _make_request(tail, type='GET', params=None, data=None):
    request_url = BASE_URL.format(tail=tail)
    if type == 'GET':
        request_result = requests.get(request_url, params=params)
        return _parse_response(request_result)
    elif type == 'POST':
        request_result = requests.post(request_url, data=data)
        return _parse_response(request_result)


def _parse_response(request_result):
    if request_result.status_code != 200:
        message = 'Server returns code: {code}'
        raise TechbotApiException(message.format(code=request_result.status_code))
    try:
        result = request_result.json()
    except:
        message = 'Invalid JSON returned from server:\n{request_text}'
        # raise TechbotApiException(message.format(request_text=request_result.text()))
        return 0

    return result


def get_poll_by_code(code):
    tail = 'polls/{code}/'.format(code=code)
    try:
        return _make_request(tail=tail)
    except TechbotApiException:
        return 0


def add_answer_container(code, telegram_username):
    tail = 'questions/addAnswerContainer/'
    data = {'poll_code': code, 'telegram_username': telegram_username}
    try:
        return _make_request(tail=tail, type='POST', data=data)
    except TechbotApiException:
        return 0


def send_answer(question_id, answer_container_pk, caption):
    tail = 'questions/{question_id}/addAnswer/'.format(question_id=question_id)
    data = {'answer_container_pk': answer_container_pk, 'caption': caption}
    try:
        return _make_request(tail=tail, type='POST', data=data)
    except TechbotApiException:
        return 0

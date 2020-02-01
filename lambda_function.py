from app import eval_math
import json
from json import JSONDecodeError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def convert_to_http_response(status_code, data=None):
    return {
        'statusCode': status_code,
        'body': data,
    }


def parseJSON(s):
    try:
        return json.loads(s)
    except JSONDecodeError:
        return None


def handler(event, context):
    try:
        request = parseJSON(event['body'])
        if not request:
            raise ValueError('Failed to parseJSON: `' + event['body'] + '`')
        result = eval_math(request)
        return convert_to_http_response(200, result)
    except ValueError as e:
        return convert_to_http_response(400, {'errors': e.args})
    except Exception as e:
        logger.error('Failed with unknown exception: %s', e.args)
        return convert_to_http_response(500, {'errors': e.args})


# print(handler({'body': '{"func":"eval","expr":"(lambda: (((9+10), N((9+10))) if S((9+10)).is_rational else ((9+10), N((9+10)), cancel((9+10)), factor((9+10)), radsimp((9+10)))))()"}'}, {}))

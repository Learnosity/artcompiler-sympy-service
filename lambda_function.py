from app import eval_math
import json
from json import JSONDecodeError
import logging

FUNC_KEY = 'func'
EXPR_KEY = 'expr'
QUERY_PARAMS_KEY = 'queryStringParameters'

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
    except Exception:
        return None


def handler(event, context):
    try:
        body = parseJSON(event['body'])
        if not body:
            body = {}
        queryParams = {}
        if QUERY_PARAMS_KEY in event and event[QUERY_PARAMS_KEY]:
            queryParams = event[QUERY_PARAMS_KEY]

        if FUNC_KEY in body and body[FUNC_KEY]:
            func = body[FUNC_KEY]
        elif FUNC_KEY in queryParams and queryParams[FUNC_KEY]:
            func = queryParams[FUNC_KEY]
        else:
            func = None

        if EXPR_KEY in body and body[EXPR_KEY]:
            expr = body[EXPR_KEY]
        elif EXPR_KEY in queryParams and queryParams[EXPR_KEY]:
            expr = queryParams[EXPR_KEY]
        else:
            expr = None

        logger.info({FUNC_KEY: func, EXPR_KEY: expr})
        result = eval_math({FUNC_KEY: func, EXPR_KEY: expr})
        logger.info(result)
        return convert_to_http_response(200, result)
    except ValueError as e:
        return convert_to_http_response(400, {'errors': e.args})
    except Exception as e:
        logger.error('Failed with unknown exception: %s', e.args)
        return convert_to_http_response(500, {'errors': e.args})


# print(handler({'body': '{"func":"eval","expr":"1+2"}'}, {}))

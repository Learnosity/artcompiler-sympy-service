import json
import logging
from sympy import latex
from sympy import sympify

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def eval_math(obj):
    logger.debug(str(obj))
    func = obj['func']
    expr = obj['expr']
    if func == 'eval':
        kwargs = {'ln_notation': 'True', 'inv_trig_style': 'power'}
        return latex(eval(expr), **kwargs)
    elif func == 'latex':
        return latex(sympify(expr, evaluate=False))
    elif func == 'literal':
        return expr
    return 'error'


def convert_to_http_response(status_code, data=None):
    return {
        'statusCode': status_code,
        'body': json.dumps(data),
    }


def handler(event, context):
    try:
        # if event['httpMethod'] != 'POST':
        #     return convert_to_http_response(404)
        request = json.loads(event['body'])
        result = eval_math(request)
        return convert_to_http_response(200, result)
    except Exception as ex:
        logger.info(ex)
        return convert_to_http_response(500)

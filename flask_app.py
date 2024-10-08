# Copyright (c) 2019, Art Compiler LLC

#!flask/bin/python

import time
import logging
from multiprocessing import Process, Pipe
from app import eval_math
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

FUNC_KEY = 'func'
EXPR_KEY = 'expr'
TIMEOUT_KEY = 'timeout'

app = Flask(__name__, static_url_path="")

# Set up Gunicorn logging
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.errorhandler(Exception)
def handle_exception(error):
    # Most likely something wrong with the SymPy code.
    app.logger.error('ERROR: ' + str(error))
    return make_response(jsonify({'error': str(error)}), 500)

@app.errorhandler(400)
def handle_bad_request(error):
    return make_response(jsonify({'error': error}), 400)

@app.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def convert_to_http_response(status_code, data=None):
    return {
        'statusCode': status_code,
        'body': json.dumps(data),
    }

def call_async(func, expr, conn):
    try:
        result = eval_math({FUNC_KEY: func, EXPR_KEY: expr})
        conn.send({'error': None, 'data': result})
    except Exception as e:
        conn.send({'error': e})

def eval_math_async(func, expr, timeout):
    parent_conn, child_conn = Pipe(False)
    t0 = time.time()
    p = Process(target=call_async, name="Math", args=(func, expr, child_conn))
    p.start()
    result = parent_conn.recv()
    p.join(timeout)  # Abort process after timeout seconds.
    t1 = time.time()
    if t1 - t0 > timeout:
        app.logger.error('timeout ' + str(timeout) + ' reached')
        result = {'error': 'Timeout for sympy-service of ' + str(timeout) + ' seconds exceeded.'}
    p.kill()
    return result

@app.route('/api/v1/eval', methods=['GET'])
def get_eval():
    try:
        func = request.args.get(FUNC_KEY)
        if not func and FUNC_KEY in request.json:
            func = request.json[FUNC_KEY]
        expr = request.args.get(EXPR_KEY)
        if not expr and EXPR_KEY in request.json:
            expr = request.json[EXPR_KEY]
        timeout = request.args.get(TIMEOUT_KEY)
        if not timeout and TIMEOUT_KEY in request.json:
            timeout = request.json[TIMEOUT_KEY]
        if not timeout:
            timeout = 30  # Default timeout is 30 seconds.
        result = eval_math_async(func, expr, timeout)
        if result['error']:
            return handle_bad_request(str(result['error']))
        else:
            return jsonify(str(result['data']))
    except ValueError as e:
        return handle_bad_request(e.args)
    except Exception as e:
        app.logger.error('Failed with unknown exception: ' + str(e.args))
        return handle_exception(e.args)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

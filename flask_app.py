# Copyright (c) 2019, Art Compiler LLC

#!flask/bin/python

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


@app.errorhandler(Exception)
def handle_exception(error):
    # Most likely something wrong with the SymPy code.
    print('ERROR: ' + str(error))
    return make_response(jsonify({'error': str(error)}), 500)

@app.errorhandler(400)
def handle_bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def call_async(func, expr, conn):
    result = eval_math({FUNC_KEY: func, EXPR_KEY: expr})
    conn.send(result)

def eval_math_async(func, expr, timeout):
    parent_conn, child_conn = Pipe(False)
    p = Process(target=call_async, name="Math", args=(func, expr, child_conn))
    p.start()
    result = parent_conn.recv()
    p.join(timeout)  # Abort process after timeout seconds.
    p.kill()
    return result

@app.route('/api/v1/eval', methods=['GET'])
def get_eval():
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
    if result == None:
        return handle_exception(f'Timeout of {timeout} seconds exceeded in SymPy.')
    else:
        return jsonify(str(result))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

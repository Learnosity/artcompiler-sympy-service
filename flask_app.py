# Copyright (c) 2019, Art Compiler LLC

#!flask/bin/python

from app import eval_math
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
FUNC_KEY = 'func'
EXPR_KEY = 'expr'

app = Flask(__name__, static_url_path="")


@app.errorhandler(Exception)
def handle_exception(error):
    # Most likely something wrong with the SymPy code.
    print('ERROR: ' + str(error))
    return make_response(jsonify({'error': str(error)}), 400)

@app.errorhandler(400)
def handle_bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1/eval', methods=['GET'])
def get_eval():
    func = request.args.get(FUNC_KEY)
    if not func and FUNC_KEY in request.json:
        func = request.json[FUNC_KEY]
    expr = request.args.get(EXPR_KEY)
    if not expr and EXPR_KEY in request.json:
        expr = request.json[EXPR_KEY]
    return jsonify(str(eval_math({FUNC_KEY: func, EXPR_KEY: expr})))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

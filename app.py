# Copyright (c) 2019, Art Compiler LLC

#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for
from sympy import *
from sympy.simplify.fu import *
import sys

app = Flask(__name__, static_url_path = "")

import platform
print(platform.python_version())

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def eval_math(obj):
    print(str(obj))
    func = obj["func"]
    expr = obj["expr"]
    if func == "eval":
        kwargs = {"ln_notation": "True", "inv_trig_style": "power"}
        return latex(eval(expr), **kwargs)
    elif func == "latex":
        return latex(sympify(expr, evaluate=False))
    elif func == "literal":
        return expr
    return "error"

@app.route('/api/v1/eval', methods = ['GET'])
def get_eval():
    return jsonify(str(eval_math(request.json)))

if __name__ == '__main__':
    app.run(debug = True)

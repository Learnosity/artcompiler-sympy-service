#!flask/bin/python

from __future__ import print_function # In python 2.7
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from sympy import *
from sympy.abc import x, y
import sys

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'art':
#         return 'compiler'
#     return None

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
#     # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def eval_math(obj):
    func = obj["func"]
    expr = obj["expr"]
    if func == "eval":
        return latex(eval(expr))
    elif func == "latex":
        return latex(sympify(expr, evaluate=False))
    elif func == "literal":
        return expr
    return "error";

@app.route('/api/v1/eval', methods = ['GET'])
def get_eval():
    return jsonify(str(eval_math(request.json)))

if __name__ == '__main__':
    app.run(debug = True)

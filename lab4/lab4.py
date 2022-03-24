from crypt import methods
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route("/add", methods = ['GET'])
def getSum():
    num1, num2 = int(request.args.get('num1')), int(request.args.get('num2'))
    sum = num1+num2
    response = {"answer": sum}
    resp = Response(json.dumps(response), mimetype='application/json')
    return resp

@app.route("/sub", methods = ['POST'])
def getDiff():
    num1, num2 = int(request.form.get('num1')), int(request.form.get('num2'))
    diff = num1-num2
    response = {"answer": diff }
    resp = Response(json.dumps(response), mimetype='application/json')
    return resp

@app.route("/mult", methods = ['POST'])
def getMult():
    form = request.get_json()
    num1, num2 = int(form['num1']), int(form['num2'])
    mult = num1*num2
    response = {"answer": mult}
    resp = Response(json.dumps(response), mimetype='application/json')
    return resp

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
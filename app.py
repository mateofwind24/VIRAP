import math
from flask import Flask, request, url_for, render_template, redirect, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World!"


@app.route('/module4')
def module4():
    totalnum = 1
    data = [[0 for j in range(5)] for i in range(5)]
    '''
    list param
    henry's constant: DHvs, Rc, Tsk, Tr, Hc, R, Ts
    inputdata[i]['']
    '''
    inputdata = request.get_json()
    for i in range(totalnum):
        data[i][0] = ((math.exp(-(inputdata[i]['DHvs']/inputdata[i]['Rc'])*((1/inputdata[i]['Tsk'])-(1/inputdata[i]['Tr']))))*inputdata[i]['Hr'])/(inputdata[i]['R']*inputdata[i]['Ts'])    # henry's constant calculate
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
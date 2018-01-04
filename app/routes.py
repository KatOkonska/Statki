from flask import render_template, request, redirect, Response
import json
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Josif'}
    return render_template('index.html', user=user)

@app.route('/kasia')
def niech_zyje():
    return render_template('kasia.html')

@app.route('/hiszpanska')
def hiszpanska():
    return render_template('hiszpanska.html')

@app.route('/gameManager',methods = ['POST'])
def gameManager():
    if request.method == 'POST':
        print("Data recieved: ", request.get_json())
        requestData = request.get_json()
        for key, value in requestData.items():
            print(key," ", value)
        responseData = {'kaczka': 'kwa kwa', 'pies': 'hau hau'}
        return json.dumps(responseData)
        #return request.data
    else:
        return ("Bad method")
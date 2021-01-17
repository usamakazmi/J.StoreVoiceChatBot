from flask import Flask, render_template, json, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from wit import Wit
import pyttsx3
import speech_recognition as sr
import os
import random
from random import seed
from random import randint
import smtplib
import sys
import cgi


access_token = "WKU2TPW45UZ47NY6FXVU7WBRQGCNSP4I"

client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    
    entity = None
    value = None
    confidence = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
        #confidence = resp['entities'][entity][0]['confidence']
    except:
        pass
    return (entity,value)
#message_text = "I want to buy something"



#now = datetime.now() dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['output']
        cur = mysql.connection.cursor()
        now = datetime.now() 
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        abc = 'User'
        abc2 = 'Bot'
        response = None

        message_text = wit_response(task_content)
        demo = (None, None)
        #return jsonify({'text' : message_text})      
        
        if message_text == demo:
            #print(message_text)
            response = "Sorry I did not understand, try changing your sentence..."
            cur.execute('''INSERT INTO msg (name, text, time) VALUES (%s,%s,%s)''', (abc, task_content, dt_string))
            cur.execute('''INSERT INTO msg (name, text, time) VALUES (%s,%s,%s)''', (abc2, response, dt_string))
            mysql.connection.commit()
            #return 'There was an issue adding your task'
            #return redirect('/')
            return jsonify(response)        
        
        entity, value = wit_response(message_text)
        
        if entity=="tell:tell" and value=="buy something":
            response ="what do you want to buy?"
        if entity=="tell:tell" and value=="something else":
            response ="what do you want to buy?"
        elif entity=="tell:tell" and value!="buy something":
            response = "Here are some {0}".format(str(value))
       
        elif entity=="ask:ask" and value!="on discount" and value!="on sale":
            response = "We do have {0}, do you have a preference?".format(str(value))
        elif entity=="ask:ask" and value=="on discount" and value!="on sale":
            response = "We do have discounted items, here they are"
        elif entity=="ask:ask" and value=="on sale" and value!="on discount":
            response = "We do have items on sale, here they are"
        elif entity=="ask:ask" and value!="on sale" and value!="on discount":
            response = "We do have {0}, do you have a preference?".format(str(value))
       
        elif entity=="greet:greet" and value.casefold()=="Assalam o Alaikum".casefold():
            response = "Waa laekum Assalam, how may I help you"
        elif entity=="greet:greet":
            response = "Hello, how may I help you"
       
        elif entity=="try:try":
            response = "Here you go, take your time, the changing room is on the left"  
        
        elif entity=="get:get":
            response = "Here is the bill thanks for coming"
        
        elif entity=="pack:pack":
            response = "{0} packed and added to your bill".format(str(value))
        

        elif entity=="types:types" and value!="perfume" and value!="shoes" and value!="scarve":
            response = "Here you go, the changing room is on the left"
        elif entity=="types:types" and value=="perfume":
            response = "Here you go"
        elif entity=="types:types":
            response = "Here you go"
        
        if response == None:
            response = "Sorry I did not understand, try changing your sentence..."

        #print(response)
        #speak(response)
        

        cur.execute('''INSERT INTO msg (name, text, time) VALUES (%s,%s,%s)''', (abc, task_content, dt_string))
        cur.execute('''INSERT INTO msg (name, text, time) VALUES (%s,%s,%s)''', (abc2, response, dt_string))
        mysql.connection.commit()
        #return 'There was an issue adding your task'
        #return redirect('/')
        return jsonify(response)
       
       

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM msg")
        fetchdata = cur.fetchall()
        cur.close()
        return render_template('index.html', data=fetchdata)

    


if __name__ == "__main__":
    app.run(debug=True)
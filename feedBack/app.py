from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template,jsonify,request
app = Flask(__name__)

#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.kraft


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/feedback/list', methods=['GET'])
def card_list():
   
    return jsonify({'result': 'success'})



if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
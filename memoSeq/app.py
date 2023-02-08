from pymongo import MongoClient
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from flask import Flask, render_template,jsonify,request
app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
#client = MongoClient('localhost', 27017)
db = client.kraft
db.counters.drop()
db.memoList.drop()
db.counters.insert_one({"seq" : 0})

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo/list', methods=['GET'])
def card_list():
    result = list(db.memoList.find({}))
    return jsonify({'result': 'success', 'list': result})
    


@app.route('/memo/add',methods=['POST'])
def add_card():
    title = request.form['title']
    text = request.form['text']
    seq = db.counters.find({})[0]['seq']
    doc = {
        '_id' : seq,
        'title' : title,
        'text' : text,
    
    }
    db.memoList.insert_one(doc)
    db.counters.update_one({'seq': seq},{'$set':{'seq' : (seq+1)}})
    

    return jsonify({'result' : 'success'})


@app.route('/memo/update', methods=['POST'])
def update_list():
    _id = request.form['id']
    title = request.form['title']
    text = request.form['text']
    db.memoList.update_one({'_id' :int(_id)} ,{'$set':{ 'title': title, 'text' : text}})

    return jsonify({'result': 'success'})


@app.route('/memo/delete', methods=['POST'])
def delete_list():

    _id = request.form['id']
    db.memoList.delete_one({'_id' : int(_id)})

    return jsonify({'result': 'success'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template,jsonify,request
from datetime import datetime
app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
#client = MongoClient('localhost', 27017)
db = client.kraft
db.commentList.drop()
db.counters.drop()
db.counters.insert_one({"seq" : 0})

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/feedback/list', methods=['GET'])
def card_list():
    result = list(db.commentList.find({}))
    return jsonify({'result': 'success', 'list' : result})


@app.route('/feedback/list/add', methods=['POST'])
def card_add():
    name = request.form['name']
    pw = request.form['pw']
    contents = request.form['contents']
    date = datetime.today().strftime("%Y-%m-%d")

    seq = db.counters.find({})[0]['seq']
    doc = {
        '_id' : seq,
        'name' : name,
        'pw' : pw,
        'contents' : contents,
        'date' : date,
    
    }
    db.commentList.insert_one(doc)
    db.counters.update_one({'seq': seq},{'$set':{'seq' : (seq+1)}})

    
    return jsonify({'result': 'success'})


@app.route('/feedback/list/delete', methods=['POST'])
def card_delete():

    id = request.form['id']
    db.commentList.delete_one({'_id' : int(id)})
   

    
    return jsonify({'result': 'success'})



if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
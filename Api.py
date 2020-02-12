from flask import Flask,jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo
from requests import request
import json
import ast
app = Flask(__name__)
app.config['MONGO_DBNAME']='test'
app.config['MONGO_URI']='mongodb+srv://Alejandro:Prueba1@proyectodi-sn0fh.mongodb.net/test?retryWrites=true&w=majority'
mongo=PyMongo(app)
api = Api(app)

@app.route('/allusers', methods=['GET'])
def get_all_users():
  usr = mongo.db.user
  output = []
  for s in usr.find():
    output.append({'username' : s['username'], 'password' : s['password']})
  return jsonify({'result' : output})

@app.route('/user/<name>', methods=['GET'])
def get_one_user(name):
  usr = mongo.db.user
  s = usr.find_one({'username' : name})
  if s:
    output = {'username' : s['username'],'password':s['password']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/postuser<datos>', methods=['POST'])
def add_user(datos):
  print('entra')
  usr = mongo.db.user
  content = datos
  print(content)
  realm = content['realm']
  name = content['username']
  email = content['email']
  password = request.form.get('password')
  user_id = usr.insert(content)
  new_user = usr.find_one({'id': user_id })
  output = {'username' : new_user['username'], 'password' : new_user['password'],'mail':new_user['email'],'realm':new_user['realm'],'emailVerified':new_user['emailVerified']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
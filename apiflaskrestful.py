from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
app = Flask(__name__)
app.config['MONGO_DBNAME']='test'
app.config['MONGO_URI']='mongodb+srv://Alejandro:Prueba1@proyectodi-sn0fh.mongodb.net/test?retryWrites=true&w=majority'
mongo=PyMongo(app)
api = Api(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class Users(Resource):
    def get(self):
        usr = mongo.db.user
        output=[]
        for s in usr.find():
            output.append({'username':s['username'],'email':s['email'],'emailVerified':s['emailVerified']})
        return jsonify({'result':output})
    def post(self):
        usr=mongo.db.user
        name= request.json['username']
        email=request.json['email']
        realm=request.json['realm']
        password=request.json['password']
        usr.insert_one({'realm':realm,'username':name,'password':password,'email':email,'emailVerified':'true'})
        return{'status':'Nuevo Usuario Añadido'}
    def put(self):  
        usr=mongo.db.user
        #TODO
        return{'status':'usuario modificado'}

class Noticias(Resource): 
    def get(self):
        usr=mongo.db.noticia
        output=[]
        for s in usr.find():
            di = JSONEncoder().encode(s['_id']).replace('"','')
            output.append({'id':di,'titulo':s['titulo'],'img':s['img'],'subtitulo':s['subtitulo'],'cuerpo':s['cuerpo']})
        return output

    def post(self):
        usr=mongo.db.noticia
        title=request.json['titulo']
        subtitle=request.json['subtitulo']
        categoria = request.json['categoria']
        img=request.json['img']
        body=request.json['cuerpo']
        comments=request.json['comentarios']
        usr.insert_one({'titulo':title,'subtitulo':subtitle,'categoria':categoria,'img':img,'cuerpo':body,'comentarios':comments})
        return{'status':'Nueva noticia añadida'}

    def put(self):
        usr=mongo.db.noticia
        di = request.json['_id']
        title=request.json['titulo']
        subtitle=request.json['subtitulo']
        img=request.json['img']
        body=request.json['cuerpo']
        comments=request.json['comentarios']
        usr.update_one({'_id':ObjectId(di)},{'$set':{'titulo':title,'subtitulo':subtitle,'img':img,'cuerpo':body,'comentarios':comments}})
        return{'status':'noticia actualizada correctamente'}
class NoticiasId(Resource):
        def get(self):  
            usr=mongo.db.noticia
            di = request.args['_id']
            print(di)
            for s in usr.find({'_id':ObjectId(di)}): 
                di = s['_id']
                categoria = s['categoria']
                titulo = s['titulo']
                subtitulo = s['subtitulo']
                img = s['img']
                cuerpo = s['cuerpo']
                comArr = []
                for c in s['comentarios']: 
                    objid = c['id']
                    comArr.append({
                    'id':JSONEncoder().encode(objid).replace('"',''),
                    'nick' : c['nick'],
                    'cuerpo' : c['cuerpo'],
                    'icono' : c['icono']
                    })

                noticia = {
                    'id':JSONEncoder().encode(di).replace('"',''),
                    'titulo':titulo,
                    'categoria':categoria,
                    'subtitulo':subtitulo,
                    'img':img,
                    'cuerpo':cuerpo,
                    'comentarios':comArr
                }
                print('NOTISIO',noticia['comentarios'])
            return jsonify(noticia)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
api.add_resource(Users,'/users')
api.add_resource(Noticias,'/noticias')
api.add_resource(NoticiasId,'/noticiasId')

if __name__ =='__main__':
    app.run(port='5000')

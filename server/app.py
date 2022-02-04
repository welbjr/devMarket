from email.policy import default
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from mongoengine import *
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

SERVER_URL = 'http://localhost:5000'
MONGO_URL = os.environ['MONGO_URL']
UPLOAD_FOLDER = './static/produtos'

# ----------------MONGODB--------------
connect(host=MONGO_URL)

class Produto(Document):
   nome     = StringField(max_length=25, required=True)
   preco    = DecimalField(min_value=0.0, max_value=5999.99, required=True)
   img_path = StringField(size=(150, 280, True), required=True)
   

# ----------------MONGODB--------------

# ----------------ROTAS----------------

@app.route("/")
def hello():
   Produto.objects.first().delete()
   return jsonify({"foo": "bar"})

@app.route("/produtos", methods=["GET", "POST"])
def produtos():
   if request.method == 'GET':
      try:
         produtos_json = Produto.objects.to_json()
         return produtos_json
      except:
         return jsonify({"status": "error", "msg": "Algo deu errado"})

   elif request.method == 'POST':
      try:
         data = request.form
         nome = data["nome"]
         preco = (data["preco"])
         img_path = f'{SERVER_URL}/{UPLOAD_FOLDER}/{nome}.png'
         request.files['file'].save(os.path.join(UPLOAD_FOLDER, f"{nome}.png"))
         novo_produto = Produto(nome=nome, preco=preco, img_path=img_path).save()
         return novo_produto.to_json()
      except (DoesNotExist, KeyError):
         return jsonify({"status":"error", "msg": "Preencha os campos obrigatórios"})
      except:
         return jsonify({"status": "error", "msg": "Algo deu errado"})


@app.route("/produtos/<id>", methods=["GET","DELETE"])
def produto(id):
   if request.method == 'GET':
      try:
         return Produto.objects(pk=id).to_json()
      except ValidationError:
         return jsonify({"status": "error", "msg": "Produto não encontrado"})
      except:
         return jsonify({"status": "error", "msg": "Algo deu errado"})

   if request.method == 'DELETE':
      try:
         Produto.objects(nome=id).delete()
         return jsonify({"status": "sucesso"})
      except ValidationError:
         return jsonify({"status": "error", "msg": "Produto não encontrado"})
      except:
         return jsonify({"status": "error", "msg": "Algo deu errado"})

# ----------------ROTAS----------------


app.run(host='0.0.0.0', debug=True)
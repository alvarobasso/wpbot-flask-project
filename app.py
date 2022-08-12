from flask import Flask, request
from src.resources.bot.bot import bot_resource
from flask_restx import Api
from pymongo import MongoClient

from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

# NAMESPACES = [
#     botNameSpace
# ]

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://us3r_MDBadmin:ADnTWxnQlunfnaFB@basso.sbxsm.mongodb.net/devolada?retryWrites=true&w=majority'

# client = MongoClient('mongodb+srv://us3r_MDBadmin:ADnTWxnQlunfnaFB@basso.sbxsm.mongodb.net/?retryWrites=true&w=majority')
# db = client.flask_db
# db_name = db.devolada

mongo = PyMongo(app)
app.config['data_to_pass'] = mongo
#print(mongo)
# id = mongo.db.users.insert_one(
#              {'username': 'a', 'email': 'a', 'password': 'a'})

app.register_blueprint(bot_resource)

api = Api(
    app=app,
    doc='/docs',
    version='1.0.0',
    title='FLASK-BOT-WP',
    description='DEVOLON BOT WP',
)

# api.namespaces.pop(0)
# for namespace in NAMESPACES:
#     api.add_namespace(namespace)

# botNameSpace.add_resource(BotResponse, '/')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)

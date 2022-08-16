import os
from dotenv import load_dotenv
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, request
from flask_restx import Api
from flask_pymongo import PyMongo
from src.resources.bot.bot import bot_resource

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)
app.config['mongo_connection'] = mongo

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

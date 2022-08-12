from flask import jsonify, request, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from src.utils.db import db_connection
from flask_pymongo import PyMongo
from bson import json_util


def get_location_by_phone(phone_number):
    mongo = current_app.config['data_to_pass']
    try:
        if phone_number:
            data = mongo.db.locations.find_one( {'phone': int(phone_number)} )
            if data:
                return data
        else:
            return jsonify({'message': 'Phone is required'})
    except Exception as e:
        return jsonify({'message': 'Error'})
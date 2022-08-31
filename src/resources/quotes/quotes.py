from flask import jsonify, current_app
from bson.objectid import ObjectId

def save_quote(quote_data:object) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        save = mongo.db.quotes.insert_one(quote_data)
        return {'message': 'Quote saved successfully', 'status': 'ok'}
    except Exception as e:
        return {'message': e, 'status': 'error'}

def update_quote(quote_data:object) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        update = mongo.db.quotes.find_one_and_update( {'phone': quote_data['phone'], 'status':True, 'quote_status':{'$in':['pending','quoted']}}, {'$set': quote_data} )
        return {'message': 'Quote updated successfully', 'status': 'ok', 'id':update['_id']}
    except Exception as e:
        return {'message': e, 'status': 'error'}

def get_quote_by_phone(quote_phone:str) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        if quote_phone:
            data = mongo.db.quotes.find_one( {'phone': quote_phone, 'status':True, 'quote_status':{'$in':['pending','quoted']}} )
            if data:
                data.pop('status')
                data['status'] = 'ok'
                return data
            else:
                return {'message': 'Quote not found', 'status': 'error'}
        else:
            return {'message': 'Phone is required', 'status': 'error'}
    except Exception as e:
        return {'message': e, 'status': 'error'}

def get_quote_by_id(quote_id:str) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        if quote_id:
            data = mongo.db.quotes.find_one( {'_id': ObjectId(quote_id), 'status':False, 'quote_status':'confirmed'} )
            if data:
                data.pop('status')
                data['status'] = 'ok'
                return data
            else:
                return {'message': 'Quote not found', 'status': 'error'}
        else:
            return {'message': 'Phone is required', 'status': 'error'}
    except Exception as e:
        return {'message': e, 'status': 'error'}
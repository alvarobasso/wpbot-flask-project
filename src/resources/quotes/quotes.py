from flask import jsonify, current_app

def post_quote(quote_data:object) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        save = mongo.db.quotes.insert_one(quote_data)
        return jsonify({'message': 'Quote saved successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'message': e, 'status': 'error'})

def get_quote_by_phone(quote_phone:str) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        if quote_phone:
            data = mongo.db.quotes.find_one( {'phone': int(quote_phone), 'status':True} )
            if data:
                data.pop('status')
                data['status'] = 'ok'
                return data
            else:
                return {'message': 'Quote not found', 'status': 'error'}
        else:
            return jsonify({'message': 'Phone is required', 'status': 'error'})
    except Exception as e:
        return jsonify({'message': e, 'status': 'error'})
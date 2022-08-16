from flask import jsonify, current_app

def get_location_by_phone(phone_number:str) -> object:
    mongo = current_app.config['mongo_connection']
    try:
        if phone_number:
            data = mongo.db.locations.find_one( {'phone': int(phone_number), 'status':True} )
            if data:
                return data
        else:
            return jsonify({'message': 'Phone is required', 'status': 'error'})
    except Exception as e:
        return jsonify({'message': e, 'status': 'error'})
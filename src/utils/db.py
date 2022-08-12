from pymongo import MongoClient

client = MongoClient('mongodb+srv://us3r_MDBadmin:ADnTWxnQlunfnaFB@basso.sbxsm.mongodb.net/devolada?retryWrites=true&w=majority' )
db = client.devolada
db_connection = client.users


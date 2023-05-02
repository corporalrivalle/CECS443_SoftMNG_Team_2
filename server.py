from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import yaml

app = Flask(__name__)
config = yaml.safe_load(open('database.yaml'))
client = MongoClient(config['uri'])
db = client['ParkingGarage']
CORS(app, resources={r"*":{"origins":"*"}})

@app.route('/')
@cross_origin(origins="*")
def index():
    return render_template('ParkingFrontEnd\src\app\homepage\homepage.component.html')

@app.route('/', methods=['POST','GET'])
@cross_origin(origins="*")
#method for creating new users
def createUser():
    if request.method == 'POST':
        body = request.json
        username = body['username']
        password = body['password']
        email = body['email']
        balance = body['balance']
        car_plate = body['car_plate']
        print(username,password,email,balance,car_plate)
        db['userData'].insert_one({
            "username":username,
            "password":password,
            "email":email,
            "balance":balance,
            "car_plate":car_plate
        })
        response = jsonify({
            "status":"Data posted to MongoDB!",
            "username":username,
            "password":password,
            "email":email,
            "balance":0,
            "car_plate":""
        })
        return response
    if request.method=='GET':
        allData = db['userData'].find()
        dataJson=[]
        for data in allData:
            fetch_id = data['_id']
            fetch_user = data['username']
            fetch_pass = data['password']
            fetch_email = data['email']
            dataDict={
                'id': str(fetch_id),
                'username': fetch_user,
                'password': fetch_pass,
                'email':fetch_email
            }
            dataJson.append(dataDict)
        print("CreateUser GET:",dataJson)
        response = jsonify(dataJson)
        return response

@app.route('/user',method=['PUT','GET','DELETE'])
@cross_origin(origins="*")
def getUser(id):
    if request.method=='GET':
        data = db['userData'].find_one({'_id':ObjectId(id)})
        fetch_username=data['username']
        fetch_id=data['_id']
        fetch_email=data['email']
        fetch_balance = data['balance']
        fetch_car_plate = data['car_plate']
        fetch_password=data['password']
        dataDict={
            'id':str(fetch_id),
            'username':fetch_username,
            'email':fetch_email,
            'balance':fetch_balance,
            'car_plate':fetch_car_plate,
            'password':fetch_password
        }
        print("GetUser GET:",dataDict)
        response = jsonify(dataDict)
        return response
    if request.method == 'PUT':
        body = request.json
        username = body['username']
        email = body['email']
        password = body['password']

        db['userData'].update_one({
            {'_id': ObjectId(id)},
            {
                "$set":{
                    'username':username,
                    'password':password,
                    'email': email
                }
            }
        })

        print("Update Successful!")
        response = jsonify({'status':'Data id: '+id+' is updated!'})
        response.headers.add('Access-Control-Allow-Origin','*')
        return response
    
    if request.method == "DELETE":
        db['userData'].delete_many({'_id': ObjectId(id)})
        print("Deletion successful!")
        response = jsonify({'status': 'Data id: ' + id + ' is deleted!'})
        response.headers.add('Access-Control-Allow-Origin','*')
        return response


if __name__ == '__main__':
    app.run()
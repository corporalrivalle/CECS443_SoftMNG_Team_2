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

# @app.route('/')
# @cross_origin(origins="*")
# def index():
#     return render_template('home.html')

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
        print("Running getAllData")
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

@app.route('/user',methods=['PUT','GET','DELETE'])
@cross_origin(origins="*")
def getAllData():
    if request.method=='GET':
        print("Running getAllData")
        allData = db['userData'].find()
        dataJson=[]
        for data in allData:
            fetch_id = data['_id']
            fetch_user = data['username']
            fetch_pass = data['password']
            fetch_email = data['email']
            fetch_balance = data['balance']
            fetch_car_plate = data['car_plate']
            dataDict={
                'id': str(fetch_id),
                'username': fetch_user,
                'password': fetch_pass,
                'email':fetch_email,
                'balance':fetch_balance,
                'car_plate':fetch_car_plate
            }
            dataJson.append(dataDict)
        print("CreateUser GET:",dataJson)
        response = jsonify(dataJson)
        return response



if __name__ == '__main__':
    app.run()
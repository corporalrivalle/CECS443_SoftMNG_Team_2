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

@app.route('/', methods=['POST'])
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



if __name__ == '__main__':
    app.run()
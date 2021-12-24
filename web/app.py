from flask import Flask, jsonify, request
from flask_restful import Api
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)



app.run(debug=True, host='0.0.0.0', port="3000")
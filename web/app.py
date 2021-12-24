from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, spacy
from validators import user_exists, verify_password, token_balance


# Flask
app = Flask(__name__)
api = Api(app)


# MongoDB
client = MongoClient("mongodb://db:27017")
db = client["PlagiarismDB"]
users = db["Users"]


# Resources
class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]

        if user_exists(username):
            return jsonify({
                "message": "User already registered"
            })
        hashed_pw = bcrypt.hashed_pw(password.encode("utf-8"), bcrypt.gensalt())


        new_user = {
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 8
        }
        users.insert_one({
            "Message": "User registered successfully",
            "User": new_user,

        })


class Detect(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]
        tokens = posted_data["tokens"]

        # Documents to check against
        text1 = posted_data["text1"]
        text2 = posted_data["text2"]


        correct_pw = verify_password(username, password)
        tokens = token_balance(username)

        if not user_exists(username):
            return jsonify({"message": "Invalid username!"})

        
        if not correct_pw:
            return jsonify({"message": "Invalid password!"})

        if tokens <= 0:
            return jsonify({"message": "Insufficient tokens to complete the request"})

        # Calculate
        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        # int (0-1) closer to 1 indicates similarity
        ratio = text1.similarity(text2)

        return_json = {"message": "Success", "similarity": ratio}
        current_tokens = token_balance(username)

        users.update_one(
            {"Username": username},
             {"$set":{
                 "Tokens": current_tokens-1
             }})
        return jsonify(return_json)
         

# Run to docker set port
app.run(debug=True, host='0.0.0.0', port="3000")
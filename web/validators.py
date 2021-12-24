from app import users
import bcrypt


def user_exists(username):
    if users.find_one({"Username": username}).count() == 0:
        return False
    else:
        return True


def correct_pw(username, password):
    hashed_pw = users.find_one({"Username": username})[0]["Password"]

    if not user_exists(username):
        return False
    
    if bcrypt.checkpw(hashed_pw, password.encode("utf-8")):
        return True
    else:
        return False


def token_balance(username):
    return users.find_one({"Username": username})[0]["Tokens"]

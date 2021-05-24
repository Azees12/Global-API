from datetime import datetime, timedelta
import json
import os
from flask import jsonify
import uuid
import mongoengine as db
import bcrypt
import jwt
from Models.MyVault.Vault import Vault
from mongoengine.fields import ListField


secret_key = os.urandom(12).hex()

class User(db.Document):
    user_id = db.UUIDField(
        db_field="user_id", unique=True, default=uuid.uuid4())
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    vault = ListField(db.ReferenceField(Vault)) 
    date_created = db.DateTimeField(default=datetime.utcnow)
    
    def json(self):
            user_dict = {
                "user_id": self.user,
                "username": self.username,
                "password": self.password,
                "date_created": self.date_created
            }
            return json.dumps(user_dict)

    meta = {
            "indexes": [],
            "ordering": ["date_created"]
        }

    def user_token(self, name):
            session_token = jwt.encode({
                'username': name,
                'exp': datetime.now() + timedelta(minutes=45)},
                secret_key
            )
            return {'session_token': session_token.decode('UTF-8')}


    def signIn(self, payload):
        try:
            check_user = User.objects(username = payload.get("username")).get()
            try:
                bcrypt.checkpw(payload.get("password").encode('utf-8'), check_user.password.encode('utf-8'))
                print("hello")
                return jsonify({"status": "True", 
                                    
                                        "username": check_user.username,
                                        "user_id": check_user.user_id,
                                        "vaults": check_user.vault,
                                        "token": self.user_token(check_user.username)}
                                     )
            except:
                return jsonify({"error": "Invaild username or password", "status": "False"})
        
        except:
            return jsonify({"error": "Invaild username or password", "status": "False"})


    def signOut():
            return({"success": True, "message": "User Signed Out"})


    def confirmPass(self, payload):
        try:
            check_user = User.objects(username = payload.get("username")).get()
            try:
                bcrypt.checkpw(payload.get("password").encode('utf-8'), check_user.password.encode('utf-8'))
                return jsonify({"status": "True", "message":"Password matches"})
            except:
                return jsonify({"error": "Password does not match", "status": "False"})
        except:
             return jsonify({"error": "User not found", "status": "False"})





    def signUp(self, payload):

            hashed_pass = bcrypt.hashpw(payload.get("password").encode('utf-8'), bcrypt.gensalt())
            print(hashed_pass)
            try:
                user = User(
                    username=payload.get("username"),
                    password=hashed_pass
                )
                print("I am here")
                user.save()
                return jsonify({"status": "True", "message": "User Created"})
            except:
                print("im in here")
                return jsonify({"error": "Unexpected error please try again", "status": "False"})

    def addVault(self,payload):
        try: 
            user = User.objects(user_id = payload.get("user_id")).get()
            print(user.username)
            try:
                new_vault = Vault(
                name = payload.get("name"),
                )
                new_vault.save()
                user.vault.append(new_vault)
                user.save()

                return jsonify({"status": "True", "message": "Vault "+ new_vault.name + " Created"})
            except:
                return jsonify({"error": "Could not be created", "status": "False"})
        except: 
            return jsonify({"error": "User not be found", "status": "False"})

    def getVault(self, payload):
        try:
            user = User.objects(user_id = payload.get("user_id")).get()

            print(user.username, user.vault[0].name)
            return jsonify({"status": "True", "Vault": user.vault})
        except:
            return jsonify({"error": "User not be found", "status": "False"})
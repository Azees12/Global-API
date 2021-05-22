from Models.MyVault.Credential import Credential
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
from Routes.vaults_routes import secret_key


class User(db.Document):
    user_id = db.UUIDField(
        db_field="user_id", unique=True, default=uuid.uuid4())
    username = db.StringField(unique=True, required=True)
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


    def user_details(self, name):

            check_user = User.objects(username=name).first()
            if check_user:
                return jsonify({
                    "status": "True",
                    "userData":
                    {
                        "username": check_user.username,
                    }
                })
            else:
                return jsonify({"error": "User not found", "status": "False"})


    def signIn(self, input1, input2):
            print(input1)
            check_user = User.objects(username=input1).first()
            if check_user:
                if bcrypt.checkpw(input2.encode('utf-8'), check_user.password.encode('utf-8')):
                    return jsonify({"status": "True", "userData":
                                    {
                                        "username": check_user.username,
                                    }, "token": self.user_token(check_user.username)})
                else:
                    return jsonify({"error": "Password does not match", "status": "False"})
            else:
                return jsonify({"error": "User not found", "status": "False"})

    def signOut():
            return({"success": True, "message": "User Signed Out"})


    def confirmPass(self, payload):
            check_user = User.objects(username=payload.get("username")).first()
            if check_user:
                    if bcrypt.checkpw(payload.get("password").encode('utf-8'), check_user.password.encode('utf-8')):
                        return jsonify({"status": "True", "message":"Password matches"})
                    else:
                        return jsonify({"error": "Password does not match", "status": "False"})
            else:
                 return jsonify({"error": "User not found", "status": "False"})



    def signUp(self, input1, input2):

            print(input1, input2, self)

            hashed_pass = bcrypt.hashpw(input2.encode('utf-8'), bcrypt.gensalt())
            print(hashed_pass)
            try:

                user = User(
                    username=input1,
                    password=hashed_pass
                )
                print("I am here")
                user.save()

                return jsonify({"status": "True", "message": "User Created"})
            except:
                print("im in here")
                return jsonify({"error": "Username already exists", "status": "False"})
            finally:
                print("Last phase")

    def addVault(self,payload):
        try: 
            user = User.objects(username = payload.get("username")).get()
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
            user = User.objects(username = payload.get("username")).get()

            print(user.username, user.vault[0].name)
            return jsonify({"status": "True", "Vault": user.vault})
        except:
            return jsonify({"error": "User not be found", "status": "False"})




            
        
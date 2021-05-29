
from enum import unique
from os import name
from Models.MyVault.Credential import Credential
from Models.MyVault.Image import Image
from Models.MyVault.Audio import Audio
import json
import uuid
from datetime import date, datetime
import mongoengine as db
from flask import jsonify
from mongoengine.fields import EmbeddedDocumentField, ListField


class Vault(db.Document):
    vault_id=db.UUIDField(db_field="vault_id", unique=True, default=uuid.uuid4())
    name = db.StringField(Required = True)
    images = ListField(EmbeddedDocumentField(Image))
    audio = ListField(EmbeddedDocumentField(Audio))
    credentials = ListField(EmbeddedDocumentField(Credential))
    date_created = db.DateTimeField(default=datetime.utcnow)
    user = db.StringField(Required=True)

    def json(self):
        vault_dict = {
            "vault_id": self.vault_id,
            "name": self.name,
            "images": self.images,
            "audio": self.audio,
            "credentials" : self.credentials,
            "user": self.user
        }
        return json.dumps(vault_dict)

    meta = {
        "indexes": [],
    }

    def addImage(self, payload):
        try:  
            new_image = Image(
                filename = payload.filename,
                payload = payload.data
            )
            Vault.update(add_to_set_images=new_image)
            return jsonify({"status": "True", "message": new_image.filename + "added"})
        except:
            return jsonify({"status": "False", "message": "Image failled to be added"})
        
    
        
    def addAudio(self, payload):
        try:  
            new_audio = Audio(
                filename = payload.filename,
                payload = payload.data
            )
            Vault.update(add_to_set_audio=new_audio)
            return jsonify({"status": "True", "message": new_audio.filename + "added"})
        except:
            return jsonify({"status": "False", "message": "Audio failled to be added"})

    def addCredentials(self,payload): 
        try:
            vault = Vault.objects(vault_id = payload.get("vault_id")).first()
            try:  
                new_cred = Credential(
                    cred_name = payload.get("cred_name"),
                    username = payload.get("username"),
                    password = payload.get("password"),
                    website = payload.get("website")
                )

                print(new_cred.cred_id)
                vault.credentials.append(new_cred)
                vault.save()
                return jsonify({"status": "True", "message": new_cred.cred_name + " added"})
            except:
                return jsonify({"status": "False", "message": "Credentials failed to be added"})
        except:
            return jsonify({"status": "False", "message": "Vault not found"})
    
    def removeCredentials(self, payload):
        try:  
            
            vault = Vault.objects(vault_id = payload.get("vault_id")).first()
            try: 
                print(payload.get("cred_id"))
                print(vault.credentials[0].cred_id)
                vault.update(pull__credentials__cred_id = payload.get("cred_id"))
                return jsonify({"status": "True", "message":  "Credential Removed"})
            except:
                return jsonify({"status": "False", "message": "Could not be removed"})
        except:
            return jsonify({"status": "False", "message": "Vault not found"})
    
    def getVault(self, payload):
        try:
           
            user = Vault.objects(vault_id = payload.get("vault_id")).get()

            return jsonify({"status": "True", "Vault": user})
        except:
            return jsonify({"error": "Vault not be found", "status": "False"})
    
    def getVaultNames(self, payload):
        try:
            print(payload.get("user_id"))
            vaults= Vault.objects(user = payload.get("user_id")).only('name','vault_id')
        
                            
            return jsonify({"status": "True", "Vaults": vaults})
        except:
            return jsonify({"error": "Vault not be found", "status": "False"})

    
    
    def addVault(self,payload):

            try:
                new_vault = Vault(
                name = payload.get("name"),
                user = payload.get("user_id")
                )
                print(new_vault.name)
                Vault.objects().insert(new_vault)

                return jsonify({"status": "True", "message": "Vault "+ new_vault.name + " Created"})
            except:
                return jsonify({"error": "Could not be created", "status": "False"})

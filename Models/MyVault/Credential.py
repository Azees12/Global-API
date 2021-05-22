from datetime import datetime, timedelta
import json
import uuid
import mongoengine as db




class Credential(db.EmbeddedDocument):
    cred_id = db.UUIDField(db_field="cred_id", unqiue=True, default=uuid.uuid4())
    cred_name= db.StringField(required = True)
    username = db.StringField(required=True)
    password = db.StringField(required = True)
    website = db.StringField(required = True)
    date_uploaded = db.DateTimeField(default=datetime.utcnow)

    def json(self):
        user_dict = {
            "cred_id": self.cred_id,
            "cred_name" : self.cred_name,
            "username": self.username,
            "password": self.password,
            "website": self.website,
            "date_upload": self.date_uploaded
        }
        return json.dumps(user_dict)

    meta = { 
        "indexes": [],
        "ordering": ["date_uploaded"]
    }
from datetime import datetime, timedelta
import json
import uuid
import mongoengine as db
from mongoengine.fields import DateTimeField, UUIDField



class Image(db.EmbeddedDocument):
    img_id = db.UUIDField(db_field="audio", unqiue=True, default=uuid.uuid4())
    filename= db.StringField(required = True)
    date_upload = db.DateTimeField(default=datetime.utcnow)
    payload = db.ImageField(required = True, thumbnail_size=(100,100, False))

    def json(self):
        user_dict = {
            "image_id": self.img_id,
            "filename" : self.filename,
            "date_uploaded": self.date_upload,
            "payload": self.payload,
        }
        return json.dumps(user_dict)

    meta = { 
        "indexes": [],
        "ordering": ["date_uploaded"]
    }
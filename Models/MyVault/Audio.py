import json
import uuid
import mongoengine as db
from datetime import datetime, timedelta




class Audio(db.EmbeddedDocument):
    audio_id = db.UUIDField(db_field="audio", unqiue=True, default=uuid.uuid4())
    filename= db.StringField(required = True)
    date_upload = db.DateTimeField(default=datetime.utcnow)
    payload = db.FileField(required = True)

    def json(self):
        user_dict = {
            "audio_id": self.audio_id,
            "filename" : self.filename,
            "date_uploaded": self.date_upload,
            "payload": self.payload,
        }
        return json.dumps(user_dict)

    meta = { 
        "indexes": [],
        "ordering": ["date_uploaded"]
    }
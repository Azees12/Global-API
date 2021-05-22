import json
import os
from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from flask_mongoengine import MongoEngine
from flask_mongoengine.sessions import MongoEngineSessionInterface
from config import Config
from Routes.vaults_routes import MyVaults
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.register_blueprint(MyVaults, url_prefix="/MyVaults")
app.config['MONGODB_SETTINGS'] = {
    "db": "MyVaults",
}
app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']
toolbar = DebugToolbarExtension(app)


db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



if __name__ == "__main__":
    app.run(debug=True)

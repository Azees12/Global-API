import os
import jwt
from Models.MyVault.Vault import Vault
from Models.MyVault.vaults_user import User
from flask import  jsonify, request, Blueprint
from functools import wraps

MyVaults = Blueprint("MyVaults",__name__)

secret_key = os.urandom(12).hex()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'session_token' in request.headers:
            token = request.headers['session_token']

        if not token:
            return jsonify({'message': 'Token is missing'}),

        try:
            data = jwt.decode({token, secret_key})
            current_user = User.objects(username=data['username']).first()

        except:
            return jsonify({'message': 'Token is Invaild'})

        return f(current_user, *args, **kwargs)

    return decorated


@MyVaults.route('/signin', methods=['POST'])
def signIn():

    user = request.get_json()
    username = user.get('username')
    password = user.get('password')

    return User().signIn(username, password)

@MyVaults.route('/signup', methods=['POST'])
def signUp():

    user = request.get_json()
    name = user.get("username")
    password = user.get("password")

    return User().signUp(name, password)

@MyVaults.route('/addVault', methods = ['POST'])
def addVault():
     payload = request.get_json()

     print(payload.get("username"))
     return User().addVault(payload)

@MyVaults.route('/addCred', methods = ['POST'])
def addCred():
     payload = request.get_json()

     return Vault().addCredentials(payload)

@MyVaults.route('/remCred', methods = ['POST'])
def remCred():
     payload = request.get_json()

     return Vault().removeCredentials(payload)

@MyVaults.route('/getVaults', methods = ['POST'])
def getVault():
     payload = request.get_json()

     return User().getVault(payload)
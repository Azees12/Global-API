import os
import jwt
from Models.MyVault.Vault import *
from Models.MyVault.vaults_user import User, secret_key
from flask import  jsonify, request, Blueprint
from functools import wraps

MyVaults = Blueprint("MyVaults",__name__)



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

    payload = request.get_json()

    return User().signIn(payload)

@MyVaults.route('/signup', methods=['POST'])
def signUp():

    payload = request.get_json()

    return User().signUp(payload)

@MyVaults.route('/addVault', methods = ['POST'])
def addVault():
     payload = request.get_json()

     
     return Vault().addVault(payload)

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

     return Vault().getVault(payload)


@MyVaults.route('/getVaultsNames', methods = ['POST'])
def getVaultNames():
     payload = request.get_json()

     return Vault().getVaultNames(payload)
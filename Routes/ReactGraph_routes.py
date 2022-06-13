import os
import jwt
from Models.ReactGraphsDemo.PythonGraph import *
from flask import  jsonify, request, Blueprint
from functools import wraps

PythonGraph = Blueprint("PythonGraph",__name__)

@PythonGraph.route('/food_sales', methods=['POST'])
def getsales():
    return getFood_Sales()
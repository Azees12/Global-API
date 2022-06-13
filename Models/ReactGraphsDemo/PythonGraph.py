import os
from pickle import TRUE
from textwrap import indent
import jwt
from functools import wraps
import json
from flask import jsonify
from openpyxl import load_workbook
import datetime


def datetimeconvert(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def getFood_Sales():
    try:
        book = load_workbook('Excels/Food.xlsx',data_only=True)
        ws = book.active
        for row in ws.iter_rows(min_row=1, min_col=1,values_only = TRUE):
            
            food_sales = {
                "date": row[0],
                "region": row[1],
                "city": row[2],
                "category": row[3],
                "product": row[4],
                "quantity": row[5],
                "unit_price": row[6],
                "total_price": row[7]
            }
        sales = json.dumps(food_sales, indent=3, default=datetimeconvert)
        return jsonify ({"status": True, "Data": sales})
    except:
        return jsonify({"status": False, "error": "data could not be retrieved"})

 
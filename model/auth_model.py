import mysql.connector
import json
import jwt
from flask import make_response,request
from functools import wraps
import re
from config.dbconfig import dbconfig
class auth_model():

    def __init__(self):

        try:
            self.con=mysql.connector.connect(host=dbconfig["hostname"], user=dbconfig["root"], password=dbconfig["Akash@2000"],database=dbconfig["flask"])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")

    def token_auth(self,endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                try:

                    authorization = request.headers.get("Authorization")
                    if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                        token = authorization.split(" ")[1]

                        try:
                            jwt_decoded = jwt.decode(token,"Akash", algorithms="HS256")
                        except Exception as e:
                            return make_response({"ERROR":str(e)}, 401)

                        role_id = jwt_decoded["payload"]["role_id"]
                        self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint = '{endpoint}'")
                        result = self.cur.fetchall()
                        if len(result)>0:
                            allowed_roles=json.loads(result[0]['roles'])
                            if role_id in allowed_roles:
                                return func(*args)
                            else:
                                return make_response({"ERROR":"INVALID_ROLE"},404)
                        else:
                            return make_response({"ERROR":"UNKNOWN_ENDPOINT"},404)
                    else:
                        return make_response({"ERROR":"INVALID TOKEN"},401)
                except Exception as e:
                    return make_response({"ERROR":str(e)}, 401)
            return inner2
        return inner1
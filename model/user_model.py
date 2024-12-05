import mysql.connector
import json
from datetime import datetime, timedelta
import jwt
from flask import make_response
from config.dbconfig import dbconfig
class user_model():

    def __init__(self):

        try:
            self.con=mysql.connector.connect(host=dbconfig["hostname"], user=dbconfig["root"], password=dbconfig["Akash@2000"],database=dbconfig["flask"])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")
    
    def user_getall_model(self):

        self.cur.execute("Select * From users")
        result=self.cur.fetchall()
        if len(result)>0:
                res = make_response({"Payload":result})
                res.headers['Access-control-Allow-Origin']='*'
                return res
        else:
             return make_response({"Message":"No Data Found"}, 204)
             
    def user_addone_model(self,data):

        self.cur.execute(f"INSERT INTO users(name,email,phone,role_id,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role_id']}','{data['password']}')")
        
        return make_response({"Message":"User added successfully"},201)
    
    def user_update_model(self,data):
            
        self.cur.execute(f"UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role_id']}',password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"Message":"User Updated successfully"},201)
        else:
            return make_response({"Message":"Nothing to Update"},202)
        
    def user_delete_model(self,id):
            
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"Message":"User Deleted successfully"},200)
        else:
            return make_response({"Message":"Nothing to Delete"},202)
        
    def user_patch_model(self,data,id):
        qry = "UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id={id}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"Message":"User Updated successfully"},201)
        else:
            return make_response({"Message":"Nothing to Update"},202)

    def user_pagination_model(self,limit,page):
        limit=int(limit)
        page=int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start},{limit}"
        self.cur.execute(qry)
        result=self.cur.fetchall()
        if len(result)>0:
                res = make_response({"Payload":result})
                #res.headers['Access-control-Allow-Origin']='*'
                return res
        else:
             return make_response({"Message":"No Data Found"}, 204)


    def user_upload_avatar_model(self,uid,finalFilePath):
        self.cur.execute("UPDATE users SET avatar=%s WHERE id=%s", (finalFilePath, uid))

        if self.cur.rowcount>0:
            return make_response({"Message":"User Uploaded successfully"},201)
        else:
            return make_response({"Message":"Nothing to Update"},202)
    
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id,name,phone,avatar,role_id FROM users WHERE email='{data['email']}' and password='{data['password']}' ")
        result=self.cur.fetchall()
        userdata=result[0]
        exp_time = datetime.now() + timedelta(minutes=150)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload" : userdata,
            "exp" : exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "Akash", algorithm="HS256")
        return make_response({"token":jwtoken}, 200)
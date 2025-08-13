from flask_restful import Resource,reqparse
from flask import jsonify
import json
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class CheckUser(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=int,required=True,help="rollno cannot be left blank!")
        data=parser.parse_args()
        return query(f"""SELECT * FROM webapp.userslogin WHERE rollno like '{data["rollno"]}' """)

class GetUserEvents(Resource):
    @jwt_required
    def post(self): 
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=int,required=True,help="rollno cannot be left blank!")
        parser.add_argument('getpost',type=str,required=True,help=" getpost be left blank!")
        data=parser.parse_args()
        if data["getpost"] == "get":
            value =query(f"""SELECT e.eventname,e.eventdesc,e.clubname,e.eventincharge,e.contact,e.lastregdate,e.startdate,e.enddate FROM webapp.eventsregistered e where e.eventname NOT IN (SELECT s.eventname FROM webapp.studentsregistered s WHERE s.rollno = '{data["rollno"]}')""",False)
            result= {"events":value }
            print(result)
        else:
            value =query(f"""SELECT e.eventname,e.eventdesc,e.clubname,e.eventincharge,e.contact,e.lastregdate,e.startdate,e.enddate FROM webapp.eventsregistered e NATURAL JOIN webapp.studentsregistered s  WHERE s.rollno = '{data["rollno"]}' """,False)
            print(type(value))
            result= {"events":value }
            print(type(result))
        return jsonify(result)
class Enroll(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=int,required=True,help="rollno cannot be left blank!")
        parser.add_argument('name',type=str,required=True,help="name cannot be left blank!")
        parser.add_argument('emailid',type=str,required=True,help="emailid cannot be left blank!")
        
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        parser.add_argument('contactno',type=int,required=True,help="contactno cannot be left blank!")
        parser.add_argument('year',type=int,required=True,help="year cannot be left blank!")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left blank!")
        parser.add_argument('section',type=int,required=True,help="section cannot be left blank!")
        data=parser.parse_args()
        query(f"""INSERT INTO webapp.studentsregistered values('{data["rollno"]}','{data["name"]}', '{data["emailid"]}','{data["eventname"]}' ,'{data["contactno"]}', '{data["year"]}', '{data["branch"]}','{data["section"]}' ) """)
        return  jsonify({"message":"Successfully enrolled event!"})

class Unroll(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=int,required=True,help="rollno cannot be left blank!")
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        data=parser.parse_args()
        query(f"""DELETE FROM webapp.studentsregistered WHERE rollno ='{data["rollno"]}' AND  eventname LIKE '{data["eventname"]}' """)
        return  jsonify({"message":"Successfully unrolled event!"})

class User(): 
    def __init__(self,rollno,pwd):
        self.rollno=rollno
        self.pwd=pwd



    @classmethod
    def getUserById(cls,rollno):
        result=query(f"""SELECT rollno,pwd FROM webapp.userslogin WHERE rollno ='{rollno}'""",return_json=False)
        if len(result)>0: return User(result[0]['rollno'],result[0]['pwd'])
        return None

class UserLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=str,required=True,help="rollno cannot be left blank!")
        parser.add_argument('pwd',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        user=User.getUserById(data['rollno'])
        print(user,data)
        if user and safe_str_cmp(user.pwd,data['pwd']):
            access_token=create_access_token(identity=user.rollno,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

class UserSignUp(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=int,required=True,help="rollno cannot be left blank!")
        parser.add_argument('pwd',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        query(f"""INSERT INTO webapp.userslogin VALUES('{data["rollno"]}', '{data["pwd"]}')""")
        return {"message":"Successfully Signed Up!"},201

class ForgotPasswordUser(Resource):
    @jwt_required
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('rollno',type=str,required=True,help="rollno cannot be left blank!")
            parser.add_argument('pwd',type=str,required=True,help="pwd cannot be left blank!")
            data=parser.parse_args()
            query(f"""UPDATE webapp.userslogin set pwd ='{data["pwd"]}'  WHERE rollno LIKE '{data["rollno"]}' """)
            return  jsonify({"message":"Successfully reset password!"})
        except:
            return  jsonify({"message":"Error Reseting password!"})
    ''''def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=str,required=True,help="rollno cannot be left blank!")
        data=parser.parse_args()
        result =query(f"""SELECT emailid FROM webapp.userslogin WHERE rollno LIKE '{data["rollno"]}' """,return_json=False)
        emailid=result[0]['emailid']
        rollno = data["rollno"]
        expires = datetime.timedelta(minutes=3)
        access_token=create_access_token(identity=rollno,expires_delta=expires)
        
        msg = MIMEMultipart()
        password =  "lablab1234"
        msg['From'] = "iotlab1234@gmail.com"
        msg['To'] = emailid
        msg['Subject'] = "Reset Password"
        message = """<a href='http://127.0.0.1:8000/home/resetconf'>Reset Password</a>"""
        msg.attach(MIMEText(message, 'html'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
 
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()
        
        print("successfully sent email to %s:" % (msg['To']))

        
        #print("Error: unable to send email")
        return {'access_token':access_token},200'''

class VerifyUser(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=str,required=True,help="rollnocannot be left blank!")
        data=parser.parse_args()
        return query(f"""SELECT pwd FROM webapp.userlogin WHERE rollno like '{data["rollno"]}' """)
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=str,required=True,help="rollno cannot be left blank!")
        parser.add_argument('pwd',type=str,required=True,help="pwd cannot be left blank!")
        data=parser.parse_args()
        try: 
            query(f"""UPDATE webapp.userslogin SET pwd = '{data["pwd"]}' WHERE clubname like '{data["rollno"]}' """)
            return  {"message":"Successfully reset password!"}, 200
        except:
            return {"message":"Error Changing password!"}, 200
        




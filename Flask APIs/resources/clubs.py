from flask_restful import Resource,reqparse 
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Check(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        return query(f"""SELECT * FROM webapp.clubsregistered WHERE clubname like '{data["clubname"]}' """)
class GetEventDetails(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        return query(f"""SELECT * FROM webapp.eventsregistered WHERE clubname like '{data["clubname"]}' """)
class AddRemove(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        parser.add_argument('eventdesc',type=str,required=True,help="eventdesc cannot be left blank!")
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('eventincharge',type=str,required=True,help="eventincharge cannot be left blank!")
        parser.add_argument('contact',type=str,required=True,help="contact cannot be left blank!")
        parser.add_argument('lastregdate',type=str,required=True,help="lastregdate cannot be left blank!")
        parser.add_argument('startdate',type=str,required=True,help="startdate cannot be left blank!")
        parser.add_argument('enddate',type=str,required=True,help="enddate cannot be left blank!")
        data=parser.parse_args()
        query(f"""INSERT INTO webapp.eventsregistered values('{data["eventname"]}','{data["eventdesc"]}', '{data["clubname"]}','{data["eventincharge"]}' ,'{data["contact"]}', '{data["lastregdate"]}', '{data["startdate"]}','{data["enddate"]}' ) """)
        return  {"message":"Successfully added event!"}, 200
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        data=parser.parse_args()
        query(f"""DELETE FROM webapp.eventsregistered WHERE eventname LIKE '{data["eventname"]}' """)
        return  {"message":"Successfully deleted event!"}, 200

class Club(): 
    def __init__(self,clubname,clubpwd,status):
        self.clubname=clubname
        self.clubpwd=clubpwd
        self.status=status


    @classmethod
    def getClubById(cls,clubname):
        result=query(f"""SELECT clubname,clubpwd,status FROM webapp.clubsregistered WHERE clubname ='{clubname}'""",return_json=False)
        if len(result)>0: return Club(result[0]['clubname'],result[0]['clubpwd'],result[0]['status'])
        return None

class ClubLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('clubpwd',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        club=Club.getClubById(data['clubname'])
        print(club,data)
        if club and safe_str_cmp(club.clubpwd,data['clubpwd']):
            if club.status==0:
                return {"pendingmessage":"Your registration is still pending!"},201
            else:
                access_token=create_access_token(identity=club.clubname,expires_delta=False)
                return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401


class ClubSignUp(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('clubpwd',type=str,required=True,help="password cannot be left blank!")
        parser.add_argument('clubhead',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('phoneno',type=str,required=True,help="password cannot be left blank!")
        parser.add_argument('emailid',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        query(f"""INSERT INTO webapp.clubsregistered VALUES('{data["clubname"]}', '{data["clubpwd"]}', '{data["clubhead"]}','{data["phoneno"]}' , '{data["emailid"]}',{0})""")
        return {"message":"Registration requested!"},201
        

class ForgotPassword(Resource):
    @jwt_required
    def get(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
            parser.add_argument('clubpwd',type=str,required=True,help="clubpwd cannot be left blank!")
            data=parser.parse_args()
            query(f"""UPDATE webapp.clubsregistered set clubpwd ='{data["clubpwd"]}'  WHERE clubname LIKE '{data["clubname"]}' """)
            return  {"message":"Successfully reset password!"}, 200
        except:
            return  {"message":"Error Reseting password!"}, 200
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        result =query(f"""SELECT emailid FROM webapp.clubsregistered WHERE clubname LIKE '{data["clubname"]}' """,return_json=False)
        emailid=result[0]['emailid']
        clubname = data["clubname"]
        expires = datetime.timedelta(minutes=3)
        access_token=create_access_token(identity=clubname,expires_delta=expires)
        
        msg = MIMEMultipart()
        password =  "lablab1234"
        msg['From'] = "iotlab1234@gmail.com"
        msg['To'] = emailid
        msg['Subject'] = "Reset Password"
        message = """<a href='https://cbit-events.herokuapp.com/home/resetconf'>Reset Password</a>"""
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
        return {'access_token':access_token},200

class Verify(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        return query(f"""SELECT clubpwd FROM webapp.clubsregistered WHERE clubname like '{data["clubname"]}' """)
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('clubpwd',type=str,required=True,help="clubpwd cannot be left blank!")
        data=parser.parse_args()
        try: 
            query(f"""UPDATE webapp.clubsregistered SET clubpwd = '{data["clubpwd"]}' WHERE clubname like '{data["clubname"]}' """)
            return  {"message":"Successfully reset password!"}, 200
        except:
            return {"message":"Error Changing password!"}, 200
   




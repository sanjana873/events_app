from flask_restful import Resource,reqparse 
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
class AdminDeleteEventAndUser(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        data=parser.parse_args()
        query(f"""DELETE FROM webapp.eventsregistered WHERE eventname LIKE '{data["eventname"]}' """)
        return  {"message":"Successfully deleted event!"}, 200
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('rollno',type=str,required=True,help="rollno cannot be left blank!")
        data=parser.parse_args()
        query(f"""DELETE FROM webapp.userslogin WHERE rollno LIKE '{data["rollno"]}' """)   
        return  {"message":"Successfully deleted user!"}, 200

class GetEvents(Resource):
    @jwt_required
    def get(self):
        return query(f"""SELECT * FROM webapp.eventsregistered""")
class GetUsers(Resource):
    @jwt_required
    def get(self):
        return query(f"""SELECT * FROM webapp.userslogin""")
class GetStudentsRegistered(Resource):
    @jwt_required
    def get(self):
        return query(f"""SELECT * FROM webapp.studentsregistered""")

class GetDetails(Resource):
    @jwt_required
    def get(self):
        return query(f"""SELECT * FROM webapp.clubsregistered WHERE status=0""")
    @jwt_required 
    def post(self):
        return query(f"""SELECT * FROM webapp.clubsregistered WHERE status=1""")
class AcceptDeny(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        print(data,data["clubname"])
        return query(f"""UPDATE webapp.clubsregistered SET status=1 WHERE clubname LIKE '{data["clubname"]}' """)
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        return query(f"""DELETE FROM webapp.clubsregistered WHERE clubname LIKE '{data["clubname"]}' """)

class Admin():
    def __init__(self,loginid,loginpwd):
        self.loginid=loginid
        self.loginpwd=loginpwd


    @classmethod
    def getAdminById(cls,loginid):
        result=query(f"""SELECT loginid,loginpwd FROM webapp.adminlogin WHERE loginid ='{loginid}'""",return_json=False)
        if len(result)>0: return Admin(result[0]['loginid'],result[0]['loginpwd'])
        return None

class AdminLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('loginid',type=str,required=True,help="loginid cannot be left blank!")
        parser.add_argument('loginpwd',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        admin=Admin.getAdminById(data['loginid'])
        print(admin,data)
        if admin and safe_str_cmp(admin.loginpwd,data['loginpwd']):
            access_token=create_access_token(identity=admin.loginid,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

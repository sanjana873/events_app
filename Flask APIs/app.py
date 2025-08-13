from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.admin import AdminLogin,GetDetails,AcceptDeny,GetEvents,GetUsers,GetStudentsRegistered,AdminDeleteEventAndUser
from resources.clubs import ClubLogin,GetEventDetails,AddRemove,ClubSignUp,Check,ForgotPassword,Verify
from resources.users import UserLogin,UserSignUp,GetUserEvents,Enroll,Unroll,CheckUser,VerifyUser,ForgotPasswordUser
#from resources.users import Users,UsersLogin


app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='coscskillup'

api = Api(app)
jwt=JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401

api.add_resource(UserLogin,'/userlogin')
api.add_resource(GetUserEvents,'/getuserevents')
api.add_resource(Enroll,'/enroll')
api.add_resource(Unroll,'/unroll')
api.add_resource(UserSignUp,'/usersignup')
api.add_resource(CheckUser,'/checkuser')
api.add_resource(VerifyUser,'/verifyuser')
api.add_resource(ForgotPasswordUser,'/forgotpassword')

api.add_resource(ClubLogin,'/clublogin')
api.add_resource(GetEventDetails,'/geteventdetails')
api.add_resource(AddRemove,'/addremove')
api.add_resource(ClubSignUp,'/clubsignup')
api.add_resource(Check,'/check')
api.add_resource(ForgotPassword,'/resetpassword')
api.add_resource(Verify,'/verify')

api.add_resource(GetDetails,'/getdetails')
api.add_resource(AdminDeleteEventAndUser,'/admindeleteeventanduser')
api.add_resource(AcceptDeny,'/acceptdeny')
api.add_resource(AdminLogin,'/adminlogin')
api.add_resource(GetEvents,'/getevents')
api.add_resource(GetUsers,'/getusers')
api.add_resource(GetStudentsRegistered,'/getstudentsregistered')

if __name__ == "__main__" :
    app.run(debug=True)
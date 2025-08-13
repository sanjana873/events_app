from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import requests

def getpendingclubs():
    global admintoken
    data = requests.get("https://cbitevents.herokuapp.com/getdetails",headers = {'Authorization':'Bearer {}'.format(admintoken)})
    data = data.json()
    print(admintoken)
    print(data)
    context={'data':data}
    return context

def getacceptedclubs():
    global admintoken
    data = requests.post("https://cbitevents.herokuapp.com/getdetails",headers = {'Authorization':'Bearer {}'.format(admintoken)})
    data = data.json()
    print(data)
    context={'data':data}
    return context
def check(clubname):
    data = requests.get("https://cbitevents.herokuapp.com/check",data={'clubname':clubname})
    data = data.json()
    return data
def homepage(request):
    data="club login"
    context={'data':data}
    return render(request,'index.html',context)

admintoken=''
clubtoken= ''
clubname=''
reset_token=''
def adminlogin(request):
    data="Admin Login"
    context={'data':data}
    return render(request,'adminlogin.html',context)
def mainadmin(request):
        
    loginid=request.POST.get('aname','')
    loginpwd=request.POST.get('apass','')
    print(loginid,loginpwd)
    global admintoken
    admintoken = requests.post("https://cbitevents.herokuapp.com/adminlogin",data = {'loginid':loginid,'loginpwd':loginpwd})
    admintoken = admintoken.json()
    if "access_token" in admintoken:
        admintoken = admintoken['access_token']
        print(admintoken)
        context=getpendingclubs()
        return render(request,'pending1.html',context)
    else:
        return HttpResponse(admintoken["message"])
def show_clubs(request):
    context=getacceptedclubs()
    return render(request,'show_clubs.html',context)

def adminhome(request):
    context=getpendingclubs()
    return render(request,'pending1.html',context)
def getevents():
    global admintoken
    data = requests.get("https://cbitevents.herokuapp.com/getevents",headers = {'Authorization':'Bearer {}'.format(admintoken)})
    data = data.json()
    print(data)
    context={'data':data}
    return context
def getallevents(request):
    context = getevents()
    return render(request,'showallevents.html',context) 
def showusers():
    global admintoken
    data = requests.get("https://cbitevents.herokuapp.com/getusers",headers = {'Authorization':'Bearer {}'.format(admintoken)})
    data = data.json()
    print(data)
    context={'data':data}
    return context
def getusers(request):
    context=showusers()
    return render(request,'showusers.html',context) 
def getstudentsregistered(request):
    global admintoken
    data = requests.get("https://cbitevents.herokuapp.com/getstudentsregistered",headers = {'Authorization':'Bearer {}'.format(admintoken)})
    data = data.json()
    print(data)
    context={'data':data}
    return render(request,'showstudentsregistered.html',context) 

def pending_requests(request):

    context=getpendingclubs()
    return render(request,'pending1.html',context)
    #return render(request,'mainadminpage.html')
def acceptdeny(request):
    global admintoken
    if request.method == 'POST':
        print("HI")
        clubname = request.POST.get('clubname')
        value=request.POST.get('status')
        print(clubname,value)
        if value=='1':
            data = requests.get("https://cbitevents.herokuapp.com/acceptdeny",headers = {'Authorization':'Bearer {}'.format(admintoken)},data={'clubname':clubname})
            data = data.json()
            print(data)
            print("accepted ")
            
        if value=='0' or value == '2':
            data = requests.post("https://cbitevents.herokuapp.com/acceptdeny",headers = {'Authorization':'Bearer {}'.format(admintoken)},data={'clubname':clubname})
            data = data.json()
            print(data)
            print("rejected ")

        
        if value == '0' or value == '1':
            context=getpendingclubs()
            return render(request,'pending1.html',context)
        if value == '2':
            context=getacceptedclubs()
            return render(request,'show_clubs.html',context)
def clublogin(request):
    data="club Login"
    context={'data':data}
    return render(request,'clublogin.html',context)
def clubsignup(request):
    data="Club Signup"
    context={'data':data}
    return render(request,'clubsignup.html',context)


def after_registration(request):
    clubname=request.POST.get('clubname')
    clubpwd=request.POST.get('clubpwd')
    clubhead=request.POST.get('clubhead')
    phoneno=request.POST.get('phoneno')
    emailid=request.POST.get('emailid')
    data=check(clubname)
    
    print(data,len(data))
    if(len(data)==1):
        return HttpResponse('ClubName Already exists')
    else:

        data =requests.post("https://cbitevents.herokuapp.com/clubsignup",data={
        "clubname":clubname, 
        "clubpwd":clubpwd, 
        "clubhead":clubhead, 
        "phoneno":phoneno, 
        "emailid":emailid
    
        })
        data = data.json()

        return render(request,'thanks.html')
def after_clublogin(request):
    global clubname
    clubname=request.POST.get('cname','')
    clubpwd=request.POST.get('cpass','')
    
    global clubtoken
    clubtoken = requests.post("https://cbitevents.herokuapp.com/clublogin",data = {'clubname':clubname,'clubpwd':clubpwd})
    clubtoken = clubtoken.json()
    if "access_token" in clubtoken:
        data=check(clubname)
        if data[0]['status']==0:
            return render(request,'thanks.html')
        else:
            print(clubname,clubpwd)
            clubtoken = clubtoken['access_token']
        
            print(clubtoken)
            
            context=show(clubname)
            return render(request,'show_events1.html',context)
    elif "pendingmessage"in clubtoken:
        return render(request,'thanks.html')
    else:
        return HttpResponse(clubtoken["message"])
def clubhome(request):
    
    return render(request,'show_events1.html')
def show(clubname):
    data = requests.get("https://cbitevents.herokuapp.com/geteventdetails",headers = {'Authorization':'Bearer {}'.format(clubtoken)},data={'clubname':clubname})
    data = data.json()
    print(admintoken)
    print(data)
    context={'data':data}
    return context
def show_events(request):
    global clubname
    context=show(clubname)
    return render(request,'show_events1.html',context)
def create_event(request):
    return render(request,'create_event.html')
def after_createevent(request):
    global clubname
    eventname=request.POST.get('eventname')
    eventdesc=request.POST.get('eventdesc')
    eventincharge=request.POST.get('eventincharge')
    contact = request.POST.get('contact')
    lastregdate=request.POST.get('lastregdate')

    startdate= request.POST.get('startdate')

    enddate=request.POST.get('enddate')
    

    print(lastregdate,startdate,enddate)
    data = requests.get("https://cbitevents.herokuapp.com/addremove",headers = {'Authorization':'Bearer {}'.format(clubtoken)},data={
 "eventname":eventname, 
 "eventdesc":eventdesc, 
 "clubname":clubname,"eventincharge":eventincharge, 
 "contact":contact, 
 "lastregdate":lastregdate, 
 "startdate":startdate, 
 "enddate":enddate
})
    data = data.json()
    context=show(clubname)
    return render(request,'show_events.html',context)

def deleteevent(request):
    global clubname
    eventname = request.POST.get('eventname')
    data = requests.post("https://cbitevents.herokuapp.com/addremove",headers = {'Authorization':'Bearer {}'.format(clubtoken)},data={'eventname':eventname})
    data = data.json()
    context=show(clubname)
    return render(request,'show_events.html',context)

def admindeleteeventanduser(request):
    global admintoken
    if request.method == 'POST':
        eventname = request.POST.get('eventname')
        data = requests.get("https://cbitevents.herokuapp.com/admindeleteeventanduser",headers = {'Authorization':'Bearer {}'.format(admintoken)},data={'eventname':eventname})
        data = data.json()
        context=getevents()
        return render(request,'showallevents.html',context)
    else:
        rollno = request.GET.get('rollno')
        print(rollno)
        print("\n")
        data = requests.post("https://cbitevents.herokuapp.com/admindeleteeventanduser",headers = {'Authorization':'Bearer {}'.format(admintoken)},data={'rollno':rollno})
        data = data.json()
        context=showusers()
        return render(request,'showusers.html',context)
def enterclubnamereset(request):
    return render(request,'resetpassword.html')
def resetpassword(request):
    global clubname
    clubname= request.POST.get('cname')
    global reset_token
    print(clubname)
    reset_token=requests.post("https://cbitevents.herokuapp.com/resetpassword",data = {'clubname':clubname})
    
    reset_token=reset_token.json()["access_token"]
    print(reset_token)
    return HttpResponse("mail sent")

def resetconf(request):
    return render(request,'reset.html')
def reset(request): 
    global clubname
    global reset_token
    clubpwd= request.POST.get('cpwd')
    confclubpwd = request.POST.get('confcpwd')
    print(clubpwd,confclubpwd)
    if (clubpwd==confclubpwd):
        result=requests.get("https://cbitevents.herokuapp.com/resetpassword",headers = {'Authorization':'Bearer {}'.format(reset_token)},data = {'clubname':clubname,'clubpwd':clubpwd})
        result= result.json()["message"]
        return HttpResponse(result)
    else:
        return HttpResponse("Password didnt match")
def profile(request):
    global clubname

    data = requests.get("https://cbitevents.herokuapp.com/check",data={'clubname':clubname})
    data = data.json()
    context={"data":data}
    return render(request,'profile.html',context)

def changeform(request):
    return render(request,'changepassword.html')

def changepassword(request):
    global clubname
    global clubtoken
    newpwd=request.POST.get("newpwd")
    confnewpwd=request.POST.get("confnewpwd")
    if newpwd == confnewpwd:
        data = requests.get("https://cbitevents.herokuapp.com/verify",headers = {'Authorization':'Bearer {}'.format(clubtoken)},data={'clubname':clubname})
        cpwd=request.POST.get("cpwd")
        print(data)
        clubpwd = data.json()[0]["clubpwd"]
        if(cpwd==clubpwd):
            data = requests.post("https://cbitevents.herokuapp.com/verify",headers = {'Authorization':'Bearer {}'.format(clubtoken)},data={'clubname':clubname,'clubpwd':newpwd})
            data = data.json()["message"]
            return HttpResponse(data)
        else:
            return HttpResponse("Old Passwords didnt match")
    else:
        return HttpResponse("New Passwords didnt match")
def getstarted(request):
    return render(request,'letsgetstarted.html')



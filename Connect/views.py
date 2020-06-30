from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate

from django.http import HttpResponse
from .forms import *
from django.db.models import Q
from .models import *

from SocialMedia.tasks import SendEmail


from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

headers = {"X-Api-Key": "d82016f839e13cd0a79afc0ef5b288b3", "X-Auth-Token": "3827881f669c11e8dad8a023fd1108c2"}

'''  Payment gateway Integration 
send_request > decide redirect url >post request(instamojo Server) > store unique id > redirect on long url > after redirect on url where we will
open unique id > send get request with unique id (Instamojo Server)
> accept response > check the status of payment 


'''
import requests
import json
def SendPaymentRequest(request, u_id):

    Buyer =UserDatabase.objects.get(id=u_id)

    payload = {
        'purpose': 'donate amt',
        'amount': '2500',
        'buyer_name': 'Buyer.name',
        'email': 'Buyer.email',
        'phone': 'Buyer.number',
        'redirect_url': 'http://127.0.0.1:8000/paycheck/',
        'send_email': 'True',
        'send_sms': 'True',

    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
    op= response.text
    data=json.loads(op)
    Pay_Id= data["payment_request"]["id"]
    PayId.objects.create(PaymentId=Pay_Id)
    Longurl =data["payment_request"]["longurl"]

    return redirect("longUrl")
    #return  HttpResponse("you want to donate 100 rs"+str(u_id))







def SendEmail(email,msg):

    from_email=settings.EMAIL_HOST_USER
    to_email = [email]
    #html =get_template("mail.html").render("msg":msg)
    html="<h1>Email</h1>"
    sub ="Techblog -New Like"
    send_mail(sub,msg,from_email, to_email,html_message=html)



def PaymentCheck(request):
    PaymentI= PayId.objects.all().order_by("-id")[0]
    PayI= PaymentI.PaymentId

    response = requests.get(
        "https://www.instamojo.com/api/1.1/payment-requests/{}/",format(PayI),
        headers=headers)
    #print(PayI)

    op = response.text
    data = json.loads(op)
    print(data)
    status= data["payment_request"]["payments"][0]["status"]
    print(status)
    if status =='Failed':
        return HttpResponse("try again")
    else:
        HttpResponse("u paid")
    #return HttpResponse("hello")





def SendSms(number,msg):
    import urllib
    import urllib.request as urllib2

    authkey = "some reference no from msg91"
    mobiles = number
    sender = "TCsim"
    msg = msg
    route = '4'
    # for transaction sms
    Dict = {
        "authkey": authkey,
        "mobiles": mobiles,
        "msg": msg,
        "route": route,
        "sender": sender

    }

    url = "http://api.msg91.com/api/sendhttp.php"
    # where we send request
    postData = urllib.parse.urlencode(Dict)
    # change data into posturl
    postData = postData.encode("ascii")
    req = urllib2.Request(url, postData)
    resp = urllib2.urlopen(req)

    op = resp.read()
    print("send msg",msg)



def login1(request):
    if request.user.is_authenticated:
        return redirect("UserProfile", request.user.username)
    form= AddUser_Form()
    error=False
    if request.method == 'POST':
        un= request.POST['un']
        ps = request.POST['ps']
        usr=authenticate(username = un,password =  ps)
        if usr != None:
            login(request, usr)
            return redirect("UserProfile", usr.username)
        error=True

    Dict ={
            "error":error,"form":form
        }
    return render(request,"login_register.html", Dict)

def register(request):
    if request.method=="POST":
        form = AddUser_Form(request.POST, request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            un = request.POST["un"]
            ps = request.POST["ps"]
            email = data.email

            usr = User.objects.create_user(un,ps,email)
            data.usr = usr
            data.save()
            return redirect("login")

    return HttpResponse("reister yourself")




def UserProfile1(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    usr=User.objects.filter(username=Username)
    if not usr:
        logged_in_username=request.user.username
        return redirect("UserProfile",logged_in_username)
    connection=None
    if request.user.username != Username:
        user1 = User.objects.get(username=Username)
        user2 = User.objects.get(username=request.user.username)
        UserData1 = UserDatabase.objects.get(usr=user1)
        UserData2 = UserDatabase.objects.get(usr=user2)
        connection = Connections.objects.filter(Q(sender=UserData1, Receiver=UserData2) | Q(sender=UserData2, Receiver=UserData1))
        if connection:
            connection = connection[0]
        # print(connection)
        # print("you are not logged")
    Usr = usr[0]
    User_Detail = UserDatabase.objects.get(usr=Usr)
    blog_form=UserBlog_Form()

    all_posts = Blogs_Model.objects.filter(usr=Usr).order_by("-date")
    like_by_me_Ids=[]
    all_like_by_me=BlogLikes.objects.filter(usr= request.user)
    for i in all_like_by_me:
        like_by_me_Ids.append(i.blog.id)
    Dict = {
        "Profile": User_Detail, "connection": connection,
        "form":blog_form,"all_posts":all_posts,
        "like_by_me_Ids":like_by_me_Ids
    }


    return render(request,"user_detail.html",Dict)

def logout1(request):
    logout(request)
    return redirect("login")

def Update_User_Details(request, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    logged_in_username = request.user.username
    if Username != logged_in_username:
        return redirect("UserProfile",logged_in_username)
    usr = User.objects.filter(username=Username)
    Usr=usr[0]
    User_Detail = UserDatabase.objects.get(usr=Usr)

    form=Edit_User_Details(request.POST or None, request.FILES or None, instance=User_Detail)

    if form.is_valid():
        form.save()
        return redirect("UserProfile",logged_in_username)

    Dict = {
        "Profile": User_Detail,"form":form
    }
    return render(request, "Update_User_Details.html", Dict)




def Manage_your_connections(request,action, u_id):

    if not request.user.is_authenticated:
        return redirect("login")

    if action == "Send_Request":
        senderUser = User.objects.get(username=request.user.username)
        sender = UserDatabase.objects.get(usr=senderUser)
        receiver=UserDatabase.objects.get(id=u_id)
        Connections.objects.create(sender=sender,Receiver=receiver)
        return redirect("UserProfile",receiver.usr.username)
    if action=="Accept_Request" or action=="Reject_Request":
        ReceiverUser = User.objects.get(username=request.user.username)
        receiver = UserDatabase.objects.get(usr=ReceiverUser)
        sender = UserDatabase.objects.get(id=u_id)
        connection =Connections.objects.filter(sender=sender, Receiver=receiver)
        if connection:
            for c in connection:
                if action=="Accept_Request":
                    c.status="Friend"
                    c.save()
                if action=="Reject_Request":
                    c.status="rejected"
                    c.save()

        return redirect("professional",  "all")

    return HttpResponse("you want " + str(action) + "For User" + str(u_id))

def All_Profession(request,what):
    if not request.user.is_authenticated:
        return redirect("login")
    logged_in_user =User.objects.get(username=request.user.username)
    me =UserDatabase.objects.get(usr=logged_in_user)

    #######count request section
    con_request = Connections.objects.filter(Receiver=me, status="Sent")
    con_sent = Connections.objects.filter(sender=me, status="Sent")
    con_friend = Connections.objects.filter(Q(sender=me, status="friend") | Q(Receiver=me, status="friend")).order_by(
        "-date")
    #### Count Request Section End ######


    data=""

    if what=="all":
        data=UserDatabase.objects.all()
    if what=="myreceived":
        connection=Connections.objects.filter(Receiver=me, status="Sent")
        user_data=[]
        for c in connection:
            ud=UserDatabase.objects.get(id=c.sender.id)
            user_data.append(ud)
        data=user_data
    if what=="Sent":
        connection=Connections.objects.filter(sender=me, status="Sent")
        user_data = []
        for c in connection:
            ud = UserDatabase.objects.get(id=c.Receiver.id)
            user_data.append(ud)
        data=user_data
    if what=="Friends":
        connection =Connections.objects.filter(Q(sender=me, status="friend") | Q(Receiver=me, status="friend")).order_by("-date")
        data = []
        for c in connection:
            ud=UserDatabase.objects.get(id=c.sender.id)
            if ud.id != me.id:
                data.append(ud)
            ud = UserDatabase.objects.get(id=c.receiver.id)
            if ud.id != me.id:
                data.append(ud)

    Dict={
        "all_users":data,"what":what,"con_request":con_request, "con_sent":con_sent, "con_friend":con_friend
    }
    return render(request, "professionals.html", Dict)


def All_professional_Html(request, what):
    if not request.user.is_authenticated:
        return redirect("login")
    data = ""
    logged_in_user = User.objects.get(username=request.user.username)
    me = UserDatabase.objects.get(usr=logged_in_user)
    #######count request section
    con_request = Connections.objects.filter(Receiver=me, status="Sent")
    con_sent = Connections.objects.filter(sender=me, status="Sent")
    con_friend = Connections.objects.filter(Q(sender=me, status="friend") | Q(Receiver=me, status="friend")).order_by(
        "-date")
    #### Count Request Section End ######
    if what =="all":
        data= UserDatabase.objects.all()
    myData = me.connections_set.all()
    Dict = {
        "all_users": data, "what": what, "con_request": con_request, "con_sent": con_sent, "con_friend": con_friend,"me":me
    }

    return render(request, "professionals_html.html", Dict)


def Add_Company(request):
    if not request.user.is_authenticated:
        return redirect("login")

    form = StartCompany_Form()

    if request.method == "POST":
        form=StartCompany_Form(request.POST , request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            Map=data.map_embad
            if 'width="600"' in Map:
                Map =Map.split('"width="600"')
                Map.insert(1, 'width="100%')
                Map=" ".join(Map)
                data.map_embad=Map
            data.usr = request.user
            data.save()
            return redirect("login")


            data.usr =request.user
            data.save()
            return redirect("login")
    Dict={"form":form}

    return render(request,"add_company.html",Dict)

def CompanyDetails(request):
    if not request.user.is_authenticated:
        return redirect("login")

    usr=request.user
    company= Company_Model.objects.filter(usr=usr)

    if not company:
        return redirect("login")

    Dict={
        "company":company.first()
    }
    return render(request,"companies_detail.html",Dict )


def NewPost(request):
    if request.method == "POST":
        form=UserBlog_Form(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.usr=request.user
            data.save()
            print("blog submitted")
    return redirect("login")

def Like_By_Me(request,b_id, Username):
    if not request.user.is_authenticated:
        return redirect("login")
    BlogLikes.objects.create(usr=request.user, blog=blog)
    msg="hii"
    blog =Blogs_Model.objects.get(id=b_id)
    user= User.objects.get(username =blog.usr.username)
    Ud= UserDatabase.objects.get(usr =user)
    name=Ud.name.split()[0]
    email =Ud.email
    number=Ud.number
    n_likes=len(BlogLikes.objects.filter(blog=blog))
    msg="hi, {name}! you got new like and {likes} no of likes ".format(name=name,likes=n_likes)
    #SendSms(number,msg)
    SendEmail(email, msg)
    return redirect("UserProfile", Username)






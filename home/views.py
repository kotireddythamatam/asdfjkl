from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from .models import User_Registration_Model,Profile,Comments,Chatting,Comment_Reply
from .forms import User_Registration_Form,User_Login_Form,Profile_Form
import smtplib
from django.conf import settings
import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.


def image_upload(request):
    if request.method == "POST":
        form = Profile_Form(request.POST or request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('image saved')
        return HttpResponse('form is invalid')
    else:
        form = Profile_Form()
        return render(request,'reg.html',{'form':form})



def user_registration_view(request):
	"""Registration form for new users"""
	form = User_Registration_Form(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			data = form.save()
			data.set_password(data.password)
			data.save()
			return HttpResponse('data saved')
		return HttpResponse('form is invalid')
	return render(request,'signup.html',{'form':form})


def login(request):
	"""Login form for registred users"""
	form = User_Login_Form(request.POST or None)
	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = auth.authenticate(username=email,password=password)
		if user:
			auth.login(request,user)
			return HttpResponseRedirect('/project/home/')
		return HttpResponse('login failed')
	return render(request,'home/login.html',{'form':form})


def home(request):
	# if request.session.has_key('email_id'):
    reply_comment=Comment_Reply.objects.all()
    comment_obj = Comments.objects.all()
    chatting_obj= Chatting.objects.filter(user_id=request.user.id).all()
    return render(request,'home/home.html',{'comments':comment_obj,'chatting':chatting_obj,'reply_comment':reply_comment})
    # return HttpResponseRedirect('/localhost/login')


def python(request):
    return render(request,'python/python.html')
    

def django(request):
	return render(request,'home/django.html')
    

def restapi(request):
	return render(request,'home/restapi.html')


def html(request):
	return render(request,'home/html.html')
    

def css(request):
	return render(request,'home/css.html')
   

def js(request):
	return render(request,'home/js.html')


def bootstrap(request):
	return render(request,'home/bootstrap.html')
 

def mysql(request):
	return render(request,'home/mysql.html')


def mongodb(request):
    # if request.session.has_key('email_id'):
    return render(request,'home/mongodb.html')
    # return HttpResponseRedirect('/localhost/login')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/project/login')


em = ""
obj_id = 0
def to_mail(request):
    if request.method == "GET":
        return render(request,'home/to_mail.html')
    elif request.method == "POST":
        global em
        em = request.POST.get('e')
        model_obj = User.objects.get(email_id = em)
        global obj_id
        obj_id = model_obj.id
        if model_obj:
            return render(request,'home/links.html')
        return HttpResponse('send proper mail')


def otp_to_mail(request):
    if request.method == "GET":
        otp = random.randrange(100000,999999)
        mail = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        subject = 'from django'
        message = 'otp:'+str(otp)
        To = [em,]
        send_mail(subject,message,settings.EMAIL_HOST_USER,To,fail_silently=True)
        response = render(request,'home/otp.html')
        response.set_cookie('otp',otp)
        return response
    elif request.method == "POST":
        user_otp = request.POST['otp']
        if request.COOKIES['otp'] == user_otp:
            return HttpResponseRedirect('/localhost/change_password')
        return HttpResponse('otp not matched')


def change_password(request):
    if request.method == "GET":
        return render(request,'home/change_password.html')
    elif request.method == "POST":
        p1 = request.POST['p1']
        p2 = request.POST.get('p2')
        if p1 == p2:
            model_obj = User.objects.get(id=obj_id)
            model_obj.password = p1
            model_obj.conform_password = p2
            model_obj.save()
            return HttpResponse('password changed')
        else:
            return HttpResponse('two fields must be same')


def link_to_mail(request):
    if request.method == "GET":
        mail = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        subject = 'from smtp'
        message = "Link : " + "http://127.0.0.1:8080/localhost/change_password"
        To = [em,]
        send_mail(subject,message,settings.EMAIL_HOST_USER,To,fail_silently=True)
        return HttpResponse('plese click on link')


def profile1(request,id=12):
    if request.method == "GET":
        model_data = User.objects.get(id=id)
        # form = Registration_Form(instance=model_data.id)
        return render(request,'home/profile.html',{"form":model_data})
    elif request.method == "POST" or request.method == "FILES":
        p = None
        four = None
        try:
            p = request.FILES.get('photo')
            one = request.POST['coursename']
            two = request.POST['collegename']
            three = request.POST['percentage']
            four = request.POST['passedoutyear']
        except:
            pass
        if p != None:
            print('p: ',p)
            model_obj = Profile(image=p)
            model_obj.save()
            return HttpResponseRedirect('/localhost/profile')
        elif four != None:
            model_obj = Student_Education_Details(
            course_name = one,
            college_name = two,
            percentage = three,
            passedout_year = four
            )
            model_obj.save()
        return HttpResponseRedirect('/localhost/profile')


def create_comment(request):
    comment = request.POST.get('ta')
    model_obj = Comments.objects.create(comment=comment,comment_category=1,user_id=request.user.id)
    return HttpResponseRedirect('/project/home')


def comment_like(request):
    like_id = request.GET.get('id')
    comment_obj = Comments.objects.get(id=int(like_id))
    comment_obj.like += 1
    comment_obj.save()
    data={'id':like_id}
    return HttpResponse(data)


def comment_dislike(request):
    dislike_id = request.GET.get('id')
    comment_obj = Comments.objects.get(id=int(dislike_id))
    comment_obj.dislike += 1
    comment_obj.save()
    data={'id':dislike_id}
    return HttpResponse(data)


def reply_comment(request,id):
    print(request.GET)
    reply_chat = request.GET.get('reply_chat')
    print('reply_chat',reply_chat)
    reply_comment_obj = Comment_Reply.objects.create(reply_comment=reply_chat,comment_id=id)
    reply_comment_obj.user.add(request.user)
    return HttpResponseRedirect('/project/home')

def chatting(request):
    chat = request.GET.get('chat',"empty")
    chatting_obj = Chatting.objects.create(user_id=request.user.id,chat=chat)
    return HttpResponseRedirect('/project/home')



























































































    # def signup_view(request):
#     if request.method == "GET":
#         form = Registration_Form()
#         return render(request,'home/signup.html',{'form':form})
#     elif request.method == "POST":
#         form = Registration_Form(request.POST)
#         if form.is_valid():
#             model_obj = User(
#             first_name = form.cleaned_data['First_name'],
#             last_name = form.cleaned_data['Last_name'],
#             email = form.cleaned_data['Email_id'],
#             # phone_number = form.cleaned_data['Phone_number'],
#             password = form.cleaned_data['Password'],
#             conform_password = form.cleaned_data['Conform_password'],
#             gender = form.cleaned_data.get('Gender'),
#             age = form.cleaned_data.get('Age'),
#             date_of_birth = form.cleaned_data.get('Date_of_birth'),
#             qualification = form.cleaned_data.get('Qualification'),
#             username = form.cleaned_data.get('username')
#             )
#             model_obj.save()
#             # return HttpResponse('Your registration is successfull')
#             return HttpResponseRedirect('/localhost/home')
#         # return HttpResponse('form invalid')
#         return render(request,'home/signup.html',{'form':form})

# def login_view(request):
#     if request.method == "GET":
#         return render(request,'home/login.html')
#     elif request.method == "POST":
#         print(request.POST)
#         un = request.POST.get('email')
#         pw = request.POST.get('password')
#         user = auth.authenticate(username=un,password=pw)
#         print(user)
#         if user:
#             auth.login(request,user)
#             request.session['email_id'] = model_obj.status
#             return HttpResponseRedirect('/localhost/home')
#         return HttpResponse('credentials are invalid')


# def login_view1(request):
#     if request.method == "GET":
#         return render(request,'home/login.html')
#     elif request.method == "POST":
#         un = request.POST.get('email')
#         pw = request.POST.get('password')
#         user = User.objects.get(email_id=un)
#         print('user: ',user)
#         print('request.user: ',request.user)
#         print('user.last_name: ',user.last_name)
#         if user.password == pw:
#             request.session['email_id'] = user.status
#             return HttpResponseRedirect('/localhost/home')
#         return HttpResponse('credentials are invalid')
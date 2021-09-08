from django.shortcuts import render,redirect
from django.http import HttpResponse, response
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

from rest_framework import serializers
from rest_framework.decorators import api_view
from work_app.serializers import JobSerializer
from work_app.models import jobs

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth 
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def home(request):
    # return render(request,'index.html')
    user = request.user
    job_list = jobs.objects.all()
    return render(request,'index.html', context={'job_list' : job_list})
    # if request.user.is_authenticated:
    #     user = request.user
    #     todos = TODO.objects.filter(user = user).order_by('priority')
        
    #     # form = TODOForm()
    #     # return render(request , 'index.html' , context={'form' : form , 'todos' : todos})
        
    #     form = TodoSerializer()
        # return render(request , 'index.html' , context={'serializer' : form , 'todos' : todos})

def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )

def signup(request):
    print(request.POST)
    form = UserCreationForm(request.POST)  
    context = {
        "form" : form
    }
    if form.is_valid():
        user = form.save()
        print(user)
        if user is not None:
            return redirect('login')
    else:
        return render(request , 'signup.html' , context=context)

def signout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def job_add(request):
    serializers = JobSerializer()
    return render(request , 'job_add.html' , context={'serializer' : serializers})
  

@login_required(login_url='login')
@api_view(["POST"])
def confirm_add(request):
    #this is a POST
    if request.user.is_authenticated:
        user = request.user
        print(user)
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return redirect("home")
        else: 
            return render(request , 'job_add.html' , context={'serializer' : serializer})


from django.core.mail import send_mail,BadHeaderError
def email_job(request, id):

    job = jobs.objects.get(pk=id)
    return render(request , 'email_send.html' , context={'job' : job})

def email_send(request,id):
    job = jobs.objects.get(pk=id)
    subject = "Job Inquiry " + job.position 
    body = request.POST['body']

    if(len(body)==0):
        messages.error(request, 'Empty Body')
    else:
        send_mail(subject, body, 'job.listing.eric@gmail.com', [job.contact_email], fail_silently=False) 
        messages.success(request, 'Email sent')
        return render(request , 'email_send.html' , context={'job' : job })

def delete_job(request, id):

    job = jobs.objects.get(pk=id)
    if(request.user == job.user):
        jobs.objects.get(pk = id).delete()
        messages.success(request,"Jobs Deleted")
    else:
        messages.error(request,"Cannot Delete the Job Poster that are not posted by you")
    return redirect('home')
    
    # return redirect('home')


def show_profile(request):
    user = request.user

    return render(request , 'profile.html') 

def update_profile(request):
    user = request.user
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    flag=0
    print("EMAIL:",email)
    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already used')
        return redirect('profile')
    else:
        messages.success(request, 'Email updated')
        if(len(email)):
            user.email = email
            flag=1
        elif len(password) and password==password2:
            user.password = password
            flag=1

        if(flag):
            user.save()
     
    return render(request , 'profile.html') 

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

def password_reset_request(request):

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})




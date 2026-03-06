from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')



from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register_api(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {"message": "User created successfully"},
        status=status.HTTP_201_CREATED
    )    



from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EmailOTP
from .utils import generate_otp



@api_view(['POST'])
def send_otp(request):

    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=400)

    otp = generate_otp()

    EmailOTP.objects.create(
        email=email,
        otp=otp
    )

    send_mail(
        "Email Verification OTP",
        f"Your OTP is {otp}",
        settings.EMAIL_HOST_USER,
        [email]
    )

    return Response({"message": "OTP sent successfully"})






from django.contrib.auth.models import User

@api_view(['POST'])
def verify_otp(request):

    email = request.data.get("email")
    otp = request.data.get("otp")
    password = request.data.get("password")

    record = EmailOTP.objects.filter(email=email, otp=otp).order_by('-created_at').first()

    if not record:
        return Response({"error": "Invalid OTP"}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )

    record.delete()

    return Response({"message": "Account created successfully"})
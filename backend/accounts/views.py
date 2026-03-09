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

# @api_view(['POST'])
# def register_api(request):
#     username = request.data.get("username")
#     email = request.data.get("email")
#     password = request.data.get("password")

#     if User.objects.filter(username=username).exists():
#         return Response(
#             {"error": "Username already exists"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password
#     )

#     return Response(
#         {"message": "User created successfully"},
#         status=status.HTTP_201_CREATED
#     )    



from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EmailOTP
from .utils import generate_otp


from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
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
        f"""Your One-Time Password (OTP) for AI Resume Analyzer is {otp}.This code is valid for 5 minutes.For security reasons, do not share this code with anyone.""",
        settings.EMAIL_HOST_USER,
        [email]
    )

    return Response({"message": "OTP sent successfully"})






from django.contrib.auth.models import User
from .models import UserProfile

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):

    email = request.data.get("email")
    otp = request.data.get("otp")
    password = request.data.get("password")

    record = EmailOTP.objects.filter(email=email, otp=otp).order_by('-created_at').first()

    from django.utils import timezone
    from datetime import timedelta
    

    if not record:
        return Response({"error": "Invalid OTP"}, status=400)

    if timezone.now() - record.created_at > timedelta(minutes=5):
        record.delete()
        return Response({"error": "OTP expired"}, status=400)


    username = request.data.get("username")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)
    

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    UserProfile.objects.create(
        user=user,
        profile_name=username
    )
    
    record.delete()

    return Response({"message": "Account created successfully"})




from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):

    identifier = request.data.get("identifier")
    password = request.data.get("password")

    # Check if identifier is email
    if "@" in identifier:
        try:
            user = User.objects.get(email=identifier)
            username = user.username
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)
    else:
        username = identifier

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    })   


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):

    email = request.data.get("email")

    if not User.objects.filter(email=email).exists():
        return Response({"error": "Email not registered"}, status=400)

    otp = generate_otp()

    EmailOTP.objects.create(
        email=email,
        otp=otp
    )

    send_mail(
        "Password Reset OTP",
        f"""Your One-Time Password (OTP) for AI Resume Analyzer is {otp}.This code is valid for 5 minutes.For security reasons, do not share this code with anyone.""",
        settings.EMAIL_HOST_USER,
        [email]
    )

    return Response({"message": "OTP sent"})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    email = request.data.get("email")
    otp = request.data.get("otp")
    password = request.data.get("password")

    record = EmailOTP.objects.filter(email=email, otp=otp).order_by('-created_at').first()

    if not record:
        return Response({"error": "Invalid OTP"}, status=400)

    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    record.delete()

    return Response({"message": "Password reset successful"})





from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):

    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    return Response({
        "username": user.username,
        "email": user.email,
        "profile_name": profile.profile_name
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):

    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    username = request.data.get("username")
    profile_name = request.data.get("profile_name")

    if username:
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            return Response({"error": "Username already taken"}, status=400)
        user.username = username
        user.save()

    if profile_name:
        profile.profile_name = profile_name
        profile.save()

    return Response({"message": "Profile updated successfully"})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user

    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    if not user.check_password(current_password):
        return Response({"error": "Current password incorrect"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_interview_email(request):
    """
    Send interview invitation emails to a list of candidates.
    """
    emails = request.data.get("emails") or []
    subject = request.data.get("subject")
    message = request.data.get("message")

    if not isinstance(emails, list):
        return Response({"error": "emails must be a list"}, status=400)

    if not subject or not message:
        return Response(
            {"error": "subject and message are required"},
            status=400,
        )

    for email in emails:
        if not email:
            continue
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

    return Response({"message": "Emails sent successfully"})


views.py

from django.shortcuts import render, redirect  # Removed duplicate import
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.conf import settings
from django.core.mail import send_mail
import random

def signup(request):
    if request.method == "POST":  # Fixed syntax error
        username = request.POST["username"]  # Fixed syntax error
        email = request.POST["email"]  # Fixed syntax error
        password = request.POST["password"] 
        #checking username already exist
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken. Please choose a different one."})

        # Corrected the order and fixed syntax error
        user = User.objects.create_user(username=username, password=password, email=email)  # Fixed indentation
        login(request, user)  # Fixed syntax error
        
    #otp generation
        otp = random.randint(100000,999999)
        request.session['otp'] = otp  # Store OTP in session

        subject = 'Welcome to my World'  # Fixed syntax error
        message = f'Hi {user.username}, thank you for registering in my app , here is one time password :{otp}.'  # Fixed syntax error and typo
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        send_mail(subject, message, email_from, recipient_list)
        print("success")
        return redirect("/verify_otp/")
    return render(request, "signup.html") # Fixed indentation

def dashboard_view(request):
    return render(request,"dashboard.html")

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        if 'otp' in request.session:
            otp = request.session['otp']
            if str(otp) == user_otp:
                del request.session['otp']  # Remove OTP from session after successful verification
                return redirect("/dashboard/")
            else:
                return render(request, "verify_otp.html", {"error": "Invalid OTP. Please try again."})
    return render(request, "verify_otp.html")


urls.py
from django.contrib import admin
from django.urls import path
from email_app.views import signup ,dashboard_view,verify_otp

urlpatterns = [
    path('',signup),
    path('signup/', signup, name='signup'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
]

templates
signup.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup Form</title>
</head>
<body>
    {% if error %}
    <div style="color: red;">{{ error }}</div>
    {% endif %}
    <form action="/signup/" method="POST">
        {% csrf_token %}
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <input type="submit" value="Signup">
    </form>
</body>
</html>


dashboard.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .welcome-container {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <h1>Welcome to My World</h1>
        <p>Thank you for visiting our site. We're glad to have you here!</p>
    </div>
</body>
</html>

verify_otp.html
<!DOCTYPE html>
<html>
<head>
    <title>Verify OTP</title>
</head>
<body>
    <h2>Verify OTP</h2>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        {% csrf_token %}
        <label for="otp">Enter OTP:</label>
        <input type="text" id="otp" name="otp" required>
        <button type="submit">Verify</button>
    </form>
</body>
</html>

settings.py
STATIC_URL = '/static/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your email id@gmail.com'
EMAIL_HOST_PASSWORD = 'app password'

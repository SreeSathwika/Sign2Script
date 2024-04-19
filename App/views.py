from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.db import IntegrityError
from django.contrib.auth import login as auth_login  # Rename to avoid conflicts
from scripts.inference_classifier import GestureClassifier
from . forms import CreateUserForm, LoginForm
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
import cv2
import pyttsx3
from django.contrib.messages import get_messages

gesture_classifier = GestureClassifier()
camera = cv2.VideoCapture(0)



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            return redirect('index')
        else:
            messages.error(request, "Invalid Credentials!")

    # Pass the messages to the template
    stored_messages = get_messages(request)
    return render(request, 'login.html', {'messages': stored_messages})

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered! Please use another email.")
        elif len(username) > 15:
            messages.error(request, "Username should be less than or equal to 15 characters.")
        elif password != confirmPassword:
            messages.error(request, 'Passwords do not match!')
        elif not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
        else:
            try:
                myuser = User.objects.create_user(username, email, password)
                myuser.save()

                # Automatically log in the user after successful registration
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    request.session['user_id'] = user.id

                return redirect('index')
            except IntegrityError:
                messages.error(request, "An error occurred during registration. Please try again later.")

    stored_messages = get_messages(request)
    return render(request, 'login.html', {'messages': stored_messages})





def index(request):
    if request.user.is_authenticated:
     user = request.user
     context = {
        'user': user
     }
     return render(request, 'index.html',context)
    else:
       return redirect('login')
   
    
def text_to_speech(text):
    # Initialize the Text-to-Speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    # Convert text to speech and play it
    engine.say(text)
    engine.runAndWait()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Perform gesture classification using your GestureClassifier
        predicted_text, frame = gesture_classifier.predict(frame)

        ''' Convert text to speech
        if predicted_text is not None:
            text_to_speech(predicted_text)'''

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode(".jpg", frame)
        frame_bytes = jpeg.tobytes()

        # Yield the frame for streaming
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n"
        )

def video_feed(request):
    return StreamingHttpResponse(
        generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame"
    )


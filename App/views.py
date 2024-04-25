from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.db import IntegrityError
from django.contrib.auth import login as auth_login  # Rename to avoid conflicts
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from .models import Transcript

from scripts.inference_classifier import GestureClassifier
import cv2
import pyttsx3
from django.contrib.messages import get_messages

record_transcript = False
transcript = ""

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
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
                    return redirect('home')
            except IntegrityError:
                messages.error(request, "An error occurred during registration. Please try again later.")

    stored_messages = get_messages(request)
    return render(request, 'login.html', {'messages': stored_messages})

@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'home.html',context)
    else:
       return redirect('login')

@login_required  
def logout_user(request):
    logout(request)
    request.session.flush()  # Clear session data
    return redirect('login')
   
@login_required
def view_profile(request):
    # Get the current user
    user = request.user
    # Assuming you have additional profile data associated with the user
    profile_data = {
        'username': user.username,
        'email': user.email,
    }

    # Render the profile.html template with the profile data
    return render(request, 'profile.html', {'profile_data': profile_data})

@login_required
def learn(request):
    return render(request, 'learn.html')

@login_required
def transcripts(request):
    user_transcripts = Transcript.objects.filter(user=request.user)
    context = {
        'user_transcripts': user_transcripts
    }
    return render(request, 'transcripts.html', context)

def text_to_speech(text):
    # Initialize the Text-to-Speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    # Convert text to speech and play it
    engine.say(text)
    engine.runAndWait()

def generate_frames(request):
    global transcript
    gesture_classifier = GestureClassifier()
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break

        if not request.path == '/video_feed/':
            camera.release()
            break

        # Perform gesture classification using your GestureClassifier
        add, predicted_text, frame = gesture_classifier.predict(frame)

        if not predicted_text == "None" and record_transcript is True and add is True:
            transcript += predicted_text
            transcript += ' ' 

        #Convert text to speech
        #if predicted_text is not None:
            #text_to_speech(predicted_text)

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode(".jpg", frame)
        frame_bytes = jpeg.tobytes()

        # Yield the frame for streaming
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n"
        )
    

def video_feed(request):
    # Generate the streaming video frames
    streaming_content = generate_frames(request)
    return StreamingHttpResponse(streaming_content, content_type="multipart/x-mixed-replace; boundary=frame")

def interpreter(request):
    global record_transcript, transcript
    if request.method == 'POST':
        post_data = request.POST
        if 'start_button' in post_data:
            record_transcript = True
        elif 'stop_button' in post_data:
            record_transcript = False
            if not transcript == "":
                transcripts_len = len(Transcript.objects.filter(user=request.user))
                title = "Transcript" + str(transcripts_len + 1)
                transcript_object = Transcript.objects.create(user=request.user, title = title, transcript = transcript )
                transcript = ""
    print(record_transcript)
    # Call the video_feed view to get the streaming video feed
    streaming_content = video_feed(request)
    # Render the 'interpreter.html' template and pass the streaming content
    return render(request, 'interpreter.html', {'streaming_content': streaming_content})



    
from django.shortcuts import render
from django.http import StreamingHttpResponse
from scripts.inference_classifier import GestureClassifier
import cv2
import pyttsx3

gesture_classifier = GestureClassifier()
camera = cv2.VideoCapture(0)

def index(request):
    return render(request, 'index.html')\
    
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


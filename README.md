
## Sign2Script - An American Sign Language Interpreter

Sign2Script  seamlessly translates ASL gestures captured through a camera into text or speech, facilitating meaningful interactions between deaf or hard-of-hearing individuals and their hearing counterparts.

With Sign2Script, communication barriers are broken down, promoting inclusivity and accessibility in the digital age.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Navigating through the project](#navigating-through-the-project)
- [Authors](#authors)

## Requirements
- Python 3.x
- OpenCV (cv2)
- NumPy
- Mediapipe
- Scikit-learn
- Django
## Installation
- Clone the repository.

__Install Python:__
If you don't already have Python installed on your system, you can download it from the official Python website:
- [Python offical Website](https://www.python.org/downloads/)

__Install Project Dependencies:__
- Open your terminal or command prompt.
- Navigate to the project directory using the cd command.
- Run the following command to install the required Python libraries from the provided ```requirements.txt``` file:
```
pip install -r requirements.txt
```
__Setup Database:__
- Run the following commands to apply migrations and create the database:
```
python manage.py makemigrations
python manage.py migrate
```
__Run the Deployment Server:__

- Start the Django development server using the following command:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your web browser to access the extension locally.
## Project Structure
- ```App/views.py```: Main Django application script.
- ```App/templates```:HTML templates for rendering the web page.
- ```inference_classifier.py```: Module containing the GestureClassifier class for performing gesture recognition.

## Navigating through the project

 __```scripts/01_collect_imgs.py```__

This script allows you to collect real-time image data from your webcam with specified labels. It creates a dataset for each label by capturing images and storing them in separate directories within a specified data directory.

 __Usage__:
- Run the script.
- Enter the labels you want to create when prompted. Enter -1 to stop adding labels.
- Once labels are entered, the webcam will activate.
- Press Q to start capturing images for each label.
- Images will be stored in the specified data directory under separate folders for each label.

__Parameters:__

- `DATA_DIR`: Directory to store the collected data. Default is `./data`.
- `dataset_size`: Number of images to collect for each label. Default is `300`.

__Notes:__

- Ensure proper lighting and background for accurate image collection.
- Press Q to start capturing images after each label prompt.

__```scripts/02_create_dataset.py```__

This script captures images from a specified directory, detects hand landmarks using the MediaPipe library, and saves the landmark data along with corresponding labels into a pickle file.

__Usage__:

- Place your image data in the specified data directory (```./data``` by default).
- Run the script.
- The script will process each image, extract hand landmarks, and save the data along with labels into a pickle file named `data.pickle`.

__Parameters__

- `DATA_DIR`: Directory containing the image data. Default is `./data`.

__Notes__

- Ensure your images have sufficient resolution and quality for accurate hand landmark detection.
- The script assumes that each subdirectory in the data directory represents a different label/class.
- Hand landmark data is saved as a list of coordinates relative to the top-left corner of the bounding box of the detected hand.
- The pickle file `data.pickle` contains a dictionary with keys 'data' and 'labels', where 'data' is a list of hand landmark data and 'labels' is a list of corresponding labels.

__```scripts/03_train_classifier.py```__

This script trains a Random Forest classifier for gesture recognition using hand landmarks data. It also evaluates the model's performance using cross-validation and saves the trained model for future use.

__Usage__

- Ensure you have hand landmarks data saved as `data.pickle` in the project directory.
- Run the script.
- The script will load the hand landmarks data, preprocess it, train a Random Forest classifier, and evaluate its performance.

 __Notes__

- Hand landmarks data should be saved as a dictionary containing 'data' (list of hand landmark data) and 'labels' (list of corresponding labels).
- The script pads each hand landmark sequence with zeros to ensure all sequences have the same length, necessary for training the classifier.
- The classifier is trained using stratified train-test split and evaluated using cross-validation for robustness.
- The trained model is saved as `model.p` using the pickle module for future use.
- Adjust the model parameters and preprocessing steps as needed for improved performance.

__```scripts/04_inference_classifier.py```__

This script performs real-time gesture recognition using hand landmarks detected by the MediaPipe library. It loads a pre-trained gesture classification model and overlays the predicted gesture label on the input video stream.

__Usage__

- Ensure you have a trained gesture classification model saved as `model.p` in the project directory.
- Run the script.
- The script will activate your webcam and overlay the predicted gesture label on the detected hand landmarks in real-time.

__Notes__

- The gesture classification model is assumed to be trained externally and saved using the pickle module.
- Hand landmarks are detected using the MediaPipe library, providing a robust representation of hand gestures.
- The script draws bounding boxes around detected hands and overlays the predicted gesture label on the video stream.
- Adjust the `min_detection_confidence` parameter of the Hands class for controlling the confidence threshold of hand landmark detection.
- Ensure proper lighting and background for accurate hand landmark detection and gesture recognition.

__```App/views.py```__

This Django-based web application streams real-time video from your webcam and performs gesture recognition using a pre-trained model. The predicted gesture labels are overlaid on the video stream and displayed on a web page.

__Usage__

- Ensure you have your pre-trained gesture classification model saved and inference code ready.
- Run the django application.
- Open your web browser and navigate to http://127.0.0.1:8000/.
- You should see the real-time video stream with predicted gesture labels overlaid.

__Notes__

- The GestureClassifier class is assumed to be implemented in `inference_classifier.py`.
- The Django application captures frames from the webcam using OpenCV, performs gesture recognition using the GestureClassifier class, and streams the processed frames to the web page.
- Ensure proper permissions for accessing the webcam.
- Adjust the URL (http://127.0.0.1:8000/) according to your Django application settings.

## Authors
- [Sathwika](https://github.com/SreeSathwika)
- [Siya](https://github.com/arorasiya008)
- [Satya](https://github.com/kuval-2004)
- [Ritika](https://github.com/ritzz912)
- [Geethika](https://github.com/GeethikaVangapandu)
- [Tamanna](https://github.com/TamannaRao)
- [Najma](https://github.com/najma-mousavi)

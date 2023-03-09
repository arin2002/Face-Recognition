from flask import Flask, render_template, Response
import cv2 
import os
import numpy as np
import face_recognition

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        ret, frame = camera.read()
        # Your face detection code here
        # ...
        
        
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

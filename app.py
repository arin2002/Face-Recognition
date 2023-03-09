from flask import Flask, render_template, Response
import cv2
import os
import numpy as np
import face_recognition

app = Flask(__name__)

# create a path for images where we stored
path = 'images'
# create a list for images
image_list = []
name = []
myList = os.listdir(path)

# now getting image name from photo name
for img in myList:
    # for loading images used
    temp = cv2.imread(f'{path}/{img}')
    # images stored in this
    image_list.append(temp)
    # names also storing
    string = os.path.splitext(img)[0]
    # remove digits from string
    res = ''.join([i for i in string if not i.isdigit()])
    name.append(res)

# now generate face encodings


def encodings(images):
    encode = []
    for img in images:
        # convert to colored images
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # a variable for storing all encodings
        temp = face_recognition.face_encodings(img)[0]
        encode.append(temp)

    return encode


encodeList = encodings(image_list)
print("ALL encodings are done")

# camera part for detecting faces
camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        # read camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # resizing
            face = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            # again convert to rgb bcz cv2 we are reading images
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            # now we need to find face locations and encodings
            current_frame = face_recognition.face_locations(face)
            encode_frame = face_recognition.face_encodings(face, current_frame)

            # now using this we wil do matching
            for encodeL, faceLoc in zip(encode_frame, current_frame):
                matching = face_recognition.compare_faces(encodeList, encodeL)
                faceDisMatching = face_recognition.face_distance(
                    encodeList, encodeL)

                # we will find minimun distance if distance face matched but if more not matched
                # this give index value of min
                matching_index = np.argmin(faceDisMatching)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2-25), (x2, y2),
                              (0, 255, 0), cv2.FILLED)

                if matching[matching_index]:
                    personName = name[matching_index].upper()
                    cv2.putText(frame, personName, (x1+6, y2-5),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Unknown face", (x1+6, y2-6),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

            # encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Flask route to home page
@app.route('/')
def home():
    return render_template('index.html')

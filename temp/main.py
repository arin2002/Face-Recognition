# we will import modules
# cv2 for displaying images and mainly for testing
# os is used because while training we need to specify path of images and looping so os used
# face recognition library help in recognizing face with many additional features
import cv2 
import os
import numpy as np
import face_recognition

# create a path for images where we stored
path = 'images'
# create a list for images
image_list = []
name = []
myList = os.listdir(path)
print(myList)
# now getting image name from photo name
for img in myList:
    # for loading images used 
    # cv2.imread() is a function in the OpenCV library used for reading an image from a file. It takes the path to the image file as input and returns a NumPy array representing the image pixel values.
    temp = cv2.imread(f'{path}/{img}')
    # images stored in this
    image_list.append(temp)
    # names also storing
    string = os.path.splitext(img)[0]
    # name.append(os.path.splitext(img)[0])
    res = ''.join([i for i in string if not i.isdigit()])
    name.append(res)


# testing 
# print(image_list)
print(name)

# now we will generate face encodings
# face encodings are basically way to represent the face using a set of 128 computer-generated measurements
# function made bcz for n images

# hog algorithm is used in this face recognition
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

# now camera paert for detecting and all
# id 0 set for camera of labtop
camera = cv2.VideoCapture(0)

# detecting faces and all code

while True:
    # camera frame is read
    ret,frame = camera.read()
    # resizing
    face = cv2.resize(frame,(0,0),None,0.25,0.25)
    # again convert to rgb bcz cv2 we are reading images
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)    
    # now we need to find face locations and encodings
    current_frame = face_recognition.face_locations(face)
    encode_frame = face_recognition.face_encodings(face,current_frame) 
    # now using this we wil do matching
    
    for encodeL,faceLoc in zip(encode_frame,current_frame):
        matching = face_recognition.compare_faces(encodeList,encodeL)
        
        faceDisMatching = face_recognition.face_distance(encodeList,encodeL)
        
        # we will find minimun distance if distance face matched but if more not matched
        # this give index value of min
        matching_index = np.argmin(faceDisMatching)
        y1,x2,y2,x1 = faceLoc
        y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(frame,(x1,y2-25),(x2,y2),(0,255,0),cv2.FILLED)
        
        if matching[matching_index]:
            personName = name[matching_index].upper()
            # print(personName)
            # now draw rect over detected face
            cv2.putText(frame,personName,(x1+6, y2-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        else:
            cv2.putText(frame,"Unknown face",(x1+6, y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
    cv2.imshow("frame",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()
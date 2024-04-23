import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

databaseURL = os.environ.get("databaseURL")
storageBucket = os.environ.get("storageBucket")


try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred,{
        'databaseURL': databaseURL,
        'storageBucket': storageBucket,
    })
    bucket = storage.bucket()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing mode images into a list
folderModePath = 'Resources/Modes'
nodePathList = os.listdir(folderModePath)
imgModeList = []
for path in nodePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

try:
    # Load the encoding file
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
except Exception as e:
    print(f"Error loading encoding file: {e}")
    exit()

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame ,model="cnn")

    if modeType < 0 or modeType >= len(imgModeList):
        print(f"Error: modeType {modeType} is out of range.")
        modeType = 0  # Set modeType to a default value
        continue  # Skip processing this frame
        
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.6)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            
            matchIndex = np.argmin(faceDis)
            
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0) 
                
                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1

                    # Convert the face region to grayscale
                    face_gray = cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
                    print(face_gray)
                                    
        if counter != 0:
            if counter == 1:
                try:
                    studentsInfo = db.reference(f'Students/{id}').get()
                    print(studentsInfo)
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    dateTimeObject = datetime.strptime(studentsInfo['last_check_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now()-dateTimeObject).total_seconds()

                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentsInfo['total_check'] +=1
                        ref.child('total_check').set(studentsInfo['total_check'])
                        ref.child('last_check_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else: 
                        counter = 0
                except Exception as e:
                    print(f"Error processing student information: {e}")
                    counter = 0
            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    
                if counter <= 10:
                    cv2.putText(imgBackground, str(studentsInfo['total_check']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2 )
                    cv2.putText(imgBackground, str(studentsInfo['id']), (1006, 493), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1 )
                    (w,h), _ = cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX,1 ,2)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentsInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2 )
                    imgBackground[175:175+216, 909:909+216] = imgStudent
                counter+=1
                
                if counter >= 20:
                    modeType = 0
                    counter = 0
                    imgStudent = []
                    studentsInfo = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
         # Set modeType to 4 when no face is detected
        modeType = 4 
        counter = 0   

    cv2.imshow("Face Recognition", imgBackground)
    cv2.waitKey(1)
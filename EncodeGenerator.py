import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from dotenv import load_dotenv

load_dotenv()

databaseURL = os.environ.get("databaseURL")
storageBucket = os.environ.get("storageBucket")


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': databaseURL,
    'storageBucket': storageBucket,
})



# Importing Images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    
    # Add data to database
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
print(studentIds)


# def findEncoding(imagesList):
#     encodeList = []
#     for img in imagesList:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
        
#     return encodeList
# Updated with error handler
def findEncoding(imagesList, imageNames):
    encodeList = []
    for img, name in zip(imagesList, imageNames):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            encode = face_encodings[0]
            encodeList.append(encode)
        else:
            print(f"No face detected in image: {name}")
            # You might want to handle this case differently, like skipping the image

    return encodeList

encodeListKnown = findEncoding(imgList, studentIds)
encodeListKnownWithIds = [encodeListKnown, studentIds]

# Saving file
file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
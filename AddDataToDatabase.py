import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os

load_dotenv()

databaseURL = os.environ.get("databaseURL")
storageBucket = os.environ.get("storageBucket")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': databaseURL
})


ref = db.reference('Students')

data = {
    "321623":
        {
            "id": "cosc201102003",
            "name":"Ahmad Bilal",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":1
        },
    "754478":
        {
            "id": "cosc201102015",
            "name":"Jamal Mustafa",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "868685":
        {
            "id": "cosc201102088",
            "name":"Muhammad Umer",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "973486":
        {
            "id": "cosc201102017",
            "name":"Aqsa Majeed",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "0980978":
        {
            "id": "cosc201102018",
            "name":"Ahsan Roy",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "6776800":
        {
            "id": "cosc201102019",
            "name":"Owais Mazhar",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "7386438":
        {
            "id": "cosc201102034",
            "name":"Muhammad Suleman",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "9689700":
        {
            "id": "cosc201102020",
            "name":"Muhammad Huzaifa",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "9879879":
        {
            "id": "cosc201102021",
            "name":"Abdul Moeed",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "43980798":
        {
            "id": "cosc201102022",
            "name":"Rahman(Not Abdul Rahman)",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "86868578":
        {
            "id": "cosc201102016",
            "name":"Tamoor Wahid",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "87657587":
        {
            "id": "cosc201102077",
            "name":"Muhammad Faizan",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
    "345534534":
        {
            "id": "cosc20110",
            "name":"Muhammad Umair",
            "last_check_time": "2024-03-30 00:54:34",
            "total_check":3
        },
}


for key, value in data.items():
    ref.child(key).set(value)
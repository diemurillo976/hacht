from google.cloud import storage
from firebase import firebase
import pyrebase
import forward
from forward import *
from PIL import Image
from io import BytesIO
import requests

config = {
    "apiKey": "AIzaSyArQxRet5XqKI6v8948A2ZnHZOZsu7vCNY",
    "authDomain": "hacht-7d98d.firebaseapp.com",
    "databaseURL": "https://hacht-7d98d.firebaseio.com",
    "projectId": "hacht-7d98d",
    "storageBucket": "hacht-7d98d.appspot.com",
    "messagingSenderId": "225406534324",
    "appId": "1:225406534324:web:f5317f74d07ced54"
  }

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

#storage.child("Test_Samples/SOB_B_A-14-22549AB-100-022.png").put("C:/Users/Martin/Desktop/Red_CNN/breakhis_subset/SOB_B_A-14-22549AB-100-022.png")


#storage.child("Test_Samples/SOB_B_A-14-22549AB-100-022.png").download("/","C:/Users/Martin/Desktop/Red_CNN/SOB_B_A-14-22549AB-100-022.png")

#url = storage.child("Test_Samples/SOB_B_A-14-22549AB-100-022.png").get_url(None)
#print("Imagen descargada de:  ", url)
for i in range(0,30):
    response = requests.get("https://firebasestorage.googleapis.com/v0/b/hacht-7d98d.appspot.com/o/Test_Samples%2FSOB_B_A-14-22549AB-100-022.png?alt=media")
    img = Image.open(BytesIO(response.content))

    print(forward_single_img(img))
    forward_single_img2("C:/Users/Martin/Desktop/Red_CNN/SOB_B_A-14-22549AB-100-022.png")

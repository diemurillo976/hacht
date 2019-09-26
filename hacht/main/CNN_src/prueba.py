from google.cloud import storage
from firebase import firebase
import pyrebase
import forward
from forward import *
from PIL import Image

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_A-14-22549AB-100-002_0.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 1, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_A-14-22549G-100-009_0.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 2, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_F-14-14134E-100-032_1.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 3, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_F-14-23060CD-100-010_1.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 4, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_PT-14-21998AB-100-015_2.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 5, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_PT-14-21998AB-100-066_2.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 6, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_TA-14-15275-100-013_3.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 7, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

path = "C:/Parma/HACHT/Red_CNN/breakhis/breakhis_subset/SOB_B_TA-14-16184CD-100-018_3.png"
img = Image.open(path)
result = forward_single_img(img)
result2 = forward_single_img2(path)

print("Imagen 8, Resultado: {}, Resultado OpenCV: {} \n".format(result, result2))

#Arreglo de categorías de tumor con que entrenó el modelo.
#Es de suma importancia NO modificar el orden de estas categorías,
#pues los valores de las predicciones del modelo corresponden a los índices de este arreglo
estimation_labels = ["Adenosis", "Fibroadenoma", "Phyllodes Tumour", "Tubular Adenon", "Carcinoma", "Lobular Carcinoma", "Mucinous Carcinoma", "Papillary Carcinoma"]

#Indices del 0 al 3 corresponden a categorías benignas y del 4 al 7 malignas
class_comparison_dict = {
    "Adenosis":0,
    "Fibroadenoma":0,
    "Phyllodes Tumour":0,
    "Tubular Adenon":0,
    "Carcinoma":1,
    "Lobular Carcinoma":1,
    "Mucinous Carcinoma":1,
    "Papillary Carcinoma":1
}

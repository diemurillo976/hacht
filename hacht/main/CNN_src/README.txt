El arhivo "req.txt" posee la lista de librerías que deben instalarse para ejecutar el código satisfactoriamente.
Dicha instalación se realiza ejecutando el siguiente comando desde el terminal (encontrándose en el directorio donde está dicho archivo):

pip install -r req.txt

Para ejecutar el código, se debe ejecutar el archivo "trainv2.py"

por ejemplo:

python trainv2.py --architecture squeezenet --epochs 3 --mag 100 --dataset breakhis --batch_size 18 --lr 0.0001 --classification multi --kfold 0 --preprocessing RGB


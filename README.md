"# hacht"

En este repositorio se encuentra la versión más actualizada del proyecto "HACHT". Esto comprende la aplicación en django, por lo que se tiene tanto el cliente web de la aplicación, como el server que alimenta las peticiones dicho cliente y el cliente móvil.

La estructura del código en el repositorio es la misma que la de un proyecto de django estándar. En la raíz de este, se incluyen archivos txt con las dependencias necesarias para correr el servidor.

En hacht/hacht/main/ se encuentra el código específico de la las funcionalidades del servidor. A continuación se lista con mayor detalle los contenidos de dicho directorio:

<ul>
  <li>Raíz del directorio: Se encuentra los módulos base de django.</li>
  <li>views.py: Módulo base de django con los métodos a procesar según los request hechos a las direcciones en urls.py. Los métodos acá puestos implementan un patrón de diseño factory, con strategy por ducktyping para la flexibilidad de añadir nuevos clientes con sus propias implementaciones de estos métodos.</li>
  <li>urls.py: Módulo base de django con las peticiones válidas a realizar al servidor.</li>
  <li>Clients: directorio que contiene los módulos necesarios para la implementación del patrón de diseño descrito. Acá se incluye el directorio Implementations que guarda las clases específicas de cada implementación de los clientes de la aplicación. Las instrucciones para implementar un nuevo cliente vienen incluidas en comentarios de código y archivos de estos directorios. Básicamente solo hay que crear un nuevo módulo .py para implementar los métodos de views.py y agregarlo al factory, además de un par de detalles más que se especifican en los archivos.</li>
  <li>Analytics: directorio que contiene módulos específicos para calcular y realizar métricas basadas en las predicciones del modelo clasificador.</li>
  <li>CNN_src: directorio que contiene los módulos del modelo clasificador. Acá se encuentra el archivo de pesos del modelo entrenado, además de los métodos utilizados para llamar al modelo y obtener una predicción a partir de una muestra (imagen). También se incluye un directorio con archivos utilizados en el proceso de entrenamiento de la red, además de en el proceso original de investigación, pero que no son necesarios para el funcionamiento de la aplicación.</li>
    <li>templates: directorio con los archivos html del cliente web</li>
    <li>static/index/assets: directorio con todos los assets del cliente web. Entre estos se mencionan las imágenes, avatares, íconos, scripts de javascript y archivos CSS</li>
</ul> 

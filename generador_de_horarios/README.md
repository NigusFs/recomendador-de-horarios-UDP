# recomendador-de-horarios-UDP



#### Instrucciones:

1. Para la ejecución de los programas se necesitan tener instalado Python 3.8 junto con  las siguientes librerias de Python. 
Al inicio de cada libreria, se tiene el comando necesario para instalarlas en Python.

    1. Pandas: [pip install pandas] / Libreria utilizada para leer archivos excel y asi obtener las asignaturas de la malla y las distintas secciones de la oferta academica.

    2. xldr: [pip install xlrd==1.2.0] /Libreria solicitada por Pandas para leer archivos tipo .xlsx. DEBE SER la versión 1.2.0.

    3. numpy: [pip install numpy] /Libreria utilizada para convertir los datos del excel en arreglos de 2 dimensiones y manejar sus datos.

    4. networkx: [pip install networkx] /Libreria más importante ya que permite la creación y manipulación de los grafos, mediante los datos que se tienen en el arreglo de 2-d.

    5. matplotlib: [pip install matplotlib] /Libreria opcional. Se usa en caso de necesitar una visualización gráfica del PERT asociado a la situación del alumno.

2. Para ejecutar el programa, los archivos .py y los archivos Excels, deben estar ubicados en la misma carpeta.

3. Luego, se debe ejecutar el archivo get_clique_max_pond.py e ingresar todos los parametros pedidos en la consola.

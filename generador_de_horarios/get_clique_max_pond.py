import networkx as nx
import matplotlib.pyplot as plt

from extract_data import extract_data

#print(extract_data(1))
G = nx.Graph()
#push del excel de la oferta academica.
#se puede hacer un una sola iteracion -> la momento de extraer los datos se puede agregar al grafo
# los horarios se deben separar para poder se procesados en el grafo

# se asume que todas las catedras y ayudantias son importantes y que el alumno debe asistir a todas las clases -> casi nadie valora las ayudanticas cambiar esto en el futuro.


# ver horario 2020 con los nuevos horarios 17:25
#"catedra":"LU JU 14:00 - 15:20" ||| 05 ->> cat1  "LU 14:00" | cat2 JU 14:00

#no recomienda cfg

#extract_data -> 
#lista_secciones = [
#	{'codigo':"CBF1000_CA05",'nombre':"MECÁNICA", 'seccion':"Sección 5", "horario":["VI 08:30","JU 14:00","MA 14:00"], "profesor": "LAVIN ROBERTO OSVALDO"},
#	{'codigo':"CIT2000_CA07",'nombre':"ESTRUCTURAS DE DATOS", 'seccion':"Sección 10", "horario":["LU 17:25","JU 17:25","VI 17:25"] ,"profesor": "EREMEEV VITALIE"},
#	{'codigo':"CBF1001_CA010",'nombre':"CALOR Y ONDAS", 'seccion':"Sección 7", "horario":["LU 10:00","JU 10:00","VI 10:00"] ,"profesor": "LEON ALEJANDRO"},
#	{'codigo':"CBF1000_CA012",'nombre':"MECÁNICA", 'seccion':"Sección 12", "horario":["MA 10:00","MI 10:00","VI 11:30"] ,"profesor": "GAGIE TRAVIS ALAN"},
#	{'codigo':"CFG_01",'nombre':"CFG", 'seccion':"Sección 0", "horario":["","",] ,"profesor": "CFG"}
#	]

arr_ramos_criticos=["PROGRAMACIÓN","PROBABILIDADES Y ESTADÍSTICAS","ELECTRÓNICA Y ELECTROTECNIA","CFG","CFG","COMUNICACIONES DIGITALES"] #llamar a rutacritica.py
lista_secciones = extract_data(arr_ramos_criticos,'2019-1') #input del año en el que se quiere obtener las secciones disponibles

def get_preferencias(): #se deben agregar mas preguntas para tener una mejor asignacion de pesos
	print("Ingrese sus preferencia")
	print("[nada(1) - poco (2) - da igual(3) - mucho(4) - bastante(5)]")
	
	ramos_830 = int(input("Que tanto te interesa entrar a las 8.30 hrs ?\n"))
	ramos_1725 = int(input("Que tanto te interesa entrar a las 17.30 hrs ?\n"))
	profesores = int(input("Que tanto te interesa tener profesores pedagogico ?\n"))
	ramos_dificiles = int(input("Quieres tener ramos dificiles ?\n"))

	return {"ramos_830":ramos_830+2, "ramos_1725":ramos_1725+2 , "profesores":profesores+2, "ramos_dificiles":ramos_dificiles+2} # se le agrego un +1 porque se esta tabajando con exponencial

def get_profesores_buenos(): # la idea es que se obtengan los datos desde una base de datos externa, en donde se recopile la percepcion de los alumnos
	profesores_buenos = []
	profesores_buenos.append("LEON ALEJANDRO")
	profesores_buenos.append("OLIVARES MARCO ANDRES")
	profesores_buenos.append("POZO JULIO HERMINIO")
	profesores_buenos.append("LOPEZ JULIO CESAR")
	profesores_buenos.append("CAVADA JUAN PABLO")
	profesores_buenos.append("CALCAGNO JAIME ALBERTO")
	profesores_buenos.append("GUTIERREZ MARTIN EDUARDO")
	return profesores_buenos

def get_ramos_dificiles(): # la idea es que se obtengan los datos desde una base de datos externa, en donde se recopile la percepcion de los alumnos
	ramos_dificiles = ["ESTRUCTURAS DE DATOS","INGENIERÍA DE SOFTWARE","ARQUITECTURA DE COMPUTADORES","PROYECTO EN TICS III","ECUACIONES DIFERENCIALES","CÁLCULO III"]
	return ramos_dificiles

#hacer lista de ramos dificiles o profes 
###profesores_buenos = get_profesores_buenos() # se debe obtener esta lista desde otro lugar || desde una pagina que recopile la percepcion de los alumnos sobre los profesores (que tan bueno son para explicar ,rajon ,etc)

# TESTEAR la funcion get_peso !!!!
#-----------------------------------

#definir que significa cada posicion de este arreglo -> ejemplo la posicion 0 es que tanto le gustan los ramos a las 8.30
# [nada(1) - poco (2) - da igual(3) - mucho(4) - bastante(5)]
# [1,2,3,4,5]
#value_encuesta = get_preferencias() # estas variables son las respuestas de la encuesta de las preferencias del alumno
#definir que significa cada numero en la encuesta -> del 1 al 10 - > te gusta tener ramos a las 8 
#																 - > te gusta tener ramos a las 17.25
#																 ->  quieres tener profes buenos
# hacer if para darle importancia a la respuesta de la encuesta
# -> si es mayor a 3 se le dara mas valor si se encuentra el dato que se esta buscando, sino se dara menor importa

# hacer que la importancia (ponderacion) sean valores entre 1 a 10
#s iempre sumar valores, nunca resta -> el peso siempre tiene que ser positivo


## buscar otro operador matematico para denotar la diferencia de importancia entre los parametros !!!!! -> aproach inicial multiplicar o dividir -> usar exponecial 

def get_peso(value_encuesta,node): #pensar bien este sistema

	ponderacion_parametros ={"horarios":7,"profesores":5,"ramos_dificiles":6} # dict para editar mas rapido las ponderaciones | Aqui se define la importancia de los parametros
	
	profesores_buenos = get_profesores_buenos()
	ramos_dificiles = get_ramos_dificiles()

### Condiciones horarias 
	bloque_a = False
	bloque_g = False
	peso_ponderado = 1
	try:
		for elem in node["horario"]:	
			if  elem[4] == str(8):
				bloque_a=True
			if  elem[3] == str(1) and elem[4] == str(7):
				bloque_g=True
	except:
		pass

	### SECCIONES EN BLOQUE 8.30 ->> #pasar esto a una funcion 
	if value_encuesta["ramos_830"] == 3*2: #se coloco un por 2 porque las respuestas estan multiplicadas por 2
		peso_ponderado +=  value_encuesta["ramos_830"]**5
	elif value_encuesta["ramos_830"] > 3*2: #arreglar lo de adentro, se puede mejorar colcoando un arreglo que esten seteados las ponderaciones -> 3 linas buscar forma
		if 	bloque_a:
			peso_ponderado += value_encuesta["ramos_830"]**ponderacion_parametros["horarios"] #este es la importancia que le damos a este parametro  # importanacia horario
		else:
			peso_ponderado += (-value_encuesta["ramos_830"])**-ponderacion_parametros["horarios"]
	else:
		if 	bloque_a == True:
			peso_ponderado += value_encuesta["ramos_830"]**-ponderacion_parametros["horarios"]
		else:
			peso_ponderado += (value_encuesta["ramos_830"])**ponderacion_parametros["horarios"]

	print(node," ",peso_ponderado)
	### SECCIONES EN BLOQUE 17.25
	
	if value_encuesta["ramos_1725"] == 3*2: #arreglar lo de adentro, se puede mejorar colcoando un arreglo que esten seteados las ponderaciones -> 3 linas buscar forma
		peso_ponderado += value_encuesta["ramos_1725"]**5 # si la respuesta de la encuesta es 3 se le asigna una importancia estandar
	elif value_encuesta["ramos_1725"] > 3*2: #si al alumno le importa este valor, si se pilla la condicion se le da mas importancia al nodo si no se le quita.
		if 	bloque_g:
			peso_ponderado += value_encuesta["ramos_1725"]**ponderacion_parametros["horarios"] 
		else:
			peso_ponderado += (value_encuesta["ramos_1725"])**-ponderacion_parametros["horarios"]
	else:
		if 	bloque_g:
			peso_ponderado += value_encuesta["ramos_1725"]** -ponderacion_parametros["horarios"] #complemento de 10 al no encontrar la preferencia estipulada.
		else:
			peso_ponderado += (value_encuesta["ramos_1725"])** ponderacion_parametros["horarios"]

	print(node," ",peso_ponderado)
### ENCUESTA PROFESORES
	if  value_encuesta["profesores"] == 3*2:
		peso_ponderado += value_encuesta["profesores"]**5 
	elif value_encuesta["profesores"] > 3*2:
		if node["profesor"] in profesores_buenos:
			peso_ponderado += value_encuesta["profesores"] ** ponderacion_parametros["profesores"]
		else:
			peso_ponderado += value_encuesta["profesores"] ** -ponderacion_parametros["profesores"] # complemento del valor ingresado ?	
	else:
		if node["profesor"] in profesores_buenos:
			peso_ponderado += value_encuesta["profesores"] ** -ponderacion_parametros["profesores"] #if (4-10)>0 else 1 #definir como se determinara este valor || restar 5 a la importancia asignada ?
		else:
			peso_ponderado += value_encuesta["profesores"] ** ponderacion_parametros["profesores"]	
	print(node," ",peso_ponderado)
### ENCUESTA RAMOS DIFICILES
	if  value_encuesta["ramos_dificiles"] == 3*2:
		peso_ponderado += value_encuesta["ramos_dificiles"]**5 
	elif value_encuesta["ramos_dificiles"] > 3:
		if node["profesor"] in profesores_buenos:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** ponderacion_parametros["ramos_dificiles"]
		else:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** -ponderacion_parametros["ramos_dificiles"] # verificar si el complemento funciona	
	else:
		if node["ramos_dificiles"] in profesores_buenos:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** -ponderacion_parametros["ramos_dificiles"] #if (4-10)>0 else 1 #definir como se determinara este valor || restar 5 a la importancia asignada ?
		else:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** ponderacion_parametros["ramos_dificiles"]		

	print(node," ",peso_ponderado)
	return peso_ponderado


def get_clique_max_pond():

	value_encuesta = get_preferencias()
	
	for elem in lista_secciones:
		peso = round(get_peso(value_encuesta,elem))
		G.add_nodes_from([elem["codigo"]], nombre = elem["nombre"],seccion= elem["seccion"],horario=elem["horario"],profesor=elem["profesor"],peso=peso )

	# verificar por nombre de ramo, dos secciones del mismo ramo no pueden ser adyacente (no deben estar conectados)
	# verificar por horario de catedra y ayudantia

	# se asume que la informacion del excel es certera -> un nodo por seccion y no se repiten los nodos. -> no era asi se tuvo que colocar un if mas linea 47 de extract_data
	# se asume que los bloques de horarios son fijos, es decir todos parte a la misma hora dependiendo del bloque-> una clase de las 14 siempre terminara a las 15.20

	list_node = list(G.nodes.items()) # es buena practica hcacer esto o los defino en los for ?
	lenth_graph = len(list_node) 

	for i  in range (lenth_graph): 
		if (i+1) < lenth_graph:
			for j in range (i+1,lenth_graph):
				if (list_node[i][1]["nombre"] != list_node[j][1]["nombre"]): #verificando que no se tomen dos secciones del mismo ramo
					tope=0
					for k in range (len(list_node[i][1]["horario"])): #sera mejor colocar varios if ?
						for x in range(len(list_node[j][1]["horario"])): 
							if (list_node[i][1]["horario"][k] == list_node[j][1]["horario"][x]): #verificando que no topen los horarios
								tope+=1
								break										
					if tope == 0:
						G.add_edge(list_node[i][0], list_node[j][0])

	#for elem in list_node: # imprime todos los nodos agregados en el grafo G
	#	print(elem,"\n")

	max_clique_pond= nx.max_weight_clique(G, weight="peso") # se obtiene el maximo clique ponderado segun el peso asignado

	for elem in  max_clique_pond[0]:
		print(G.nodes[elem]["nombre"],G.nodes[elem]["seccion"],G.nodes[elem]["horario"])

	print(max_clique_pond) #se muestra los elementos del clique maximo

	nx.draw(G, with_labels=True, font_weight='bold') #se dibuja el grafo generado
	plt.show()
	
	#return max_clique_pond #se coloca por si se quiere utilizar mas adelante, de momento se deja el print

def main():
	get_clique_max_pond()

if __name__ == "__main__":
    main()
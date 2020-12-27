import networkx as nx
import matplotlib.pyplot as plt
from extract_data import extract_data

G = nx.Graph()

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

	### SECCIONES EN BLOQUE 8.30 -
	if value_encuesta["ramos_830"] == 3*2: #se coloco un por 2 porque las respuestas estan multiplicadas por 2
		peso_ponderado +=  value_encuesta["ramos_830"]**5
	elif value_encuesta["ramos_830"] > 3*2: 
		if 	bloque_a:
			peso_ponderado += value_encuesta["ramos_830"]**ponderacion_parametros["horarios"] #este es la importancia que le damos a este parametro  # importanacia horario
		else:
			peso_ponderado += (-value_encuesta["ramos_830"])**-ponderacion_parametros["horarios"]
	else:
		if 	bloque_a == True:
			peso_ponderado += value_encuesta["ramos_830"]**-ponderacion_parametros["horarios"]
		else:
			peso_ponderado += (value_encuesta["ramos_830"])**ponderacion_parametros["horarios"]

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
			peso_ponderado += value_encuesta["ramos_1725"]** -ponderacion_parametros["horarios"]
		else:
			peso_ponderado += (value_encuesta["ramos_1725"])** ponderacion_parametros["horarios"]

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

### ENCUESTA RAMOS DIFICILES
	if  value_encuesta["ramos_dificiles"] == 3*2:
		peso_ponderado += value_encuesta["ramos_dificiles"]**5 
	elif value_encuesta["ramos_dificiles"] > 3:
		if node["profesor"] in profesores_buenos:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** ponderacion_parametros["ramos_dificiles"]
		else:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** -ponderacion_parametros["ramos_dificiles"]	
	else:
		if node["ramos_dificiles"] in profesores_buenos:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** -ponderacion_parametros["ramos_dificiles"]
		else:
			peso_ponderado += value_encuesta["ramos_dificiles"] ** ponderacion_parametros["ramos_dificiles"]		

	return peso_ponderado


def get_clique_max_pond():

	value_encuesta = get_preferencias()
	
	for elem in lista_secciones:
		peso = round(get_peso(value_encuesta,elem))
		G.add_nodes_from([elem["codigo"]], nombre = elem["nombre"],seccion= elem["seccion"],horario=elem["horario"],profesor=elem["profesor"],peso=peso )

	list_node = list(G.nodes.items()) 
	lenth_graph = len(list_node) 

	for i  in range (lenth_graph): 
		if (i+1) < lenth_graph:
			for j in range (i+1,lenth_graph):
				if (list_node[i][1]["nombre"] != list_node[j][1]["nombre"]): #verificando que no se tomen dos secciones del mismo ramo
					tope=0
					for k in range (len(list_node[i][1]["horario"])): 
						for x in range(len(list_node[j][1]["horario"])): 
							if (list_node[i][1]["horario"][k] == list_node[j][1]["horario"][x]): #verificando que no topen los horarios
								tope+=1
								break										
					if tope == 0:
						G.add_edge(list_node[i][0], list_node[j][0])

	#for elem in list_node: # imprime todos los nodos agregados en el grafo G
	#	print(elem,"\n")

	max_clique_pond= nx.max_weight_clique(G, weight="peso") #se obtiene el maximo clique ponderado segun el peso asignado

	for elem in  max_clique_pond[0]:
		print(G.nodes[elem]["nombre"],G.nodes[elem]["seccion"],G.nodes[elem]["horario"])

	print(max_clique_pond) #se muestra los elementos del clique maximo

	#nx.draw(G, with_labels=True, font_weight='bold') #se dibuja el grafo generado
	#plt.show()
	
	#return max_clique_pond #se coloca por si se quiere utilizar mas adelante, de momento se deja el print

def main():
	get_clique_max_pond()

if __name__ == "__main__":
    main()
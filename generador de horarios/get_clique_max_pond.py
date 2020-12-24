import networkx as nx

G = nx.Graph()
#push del excel de la oferta academica.
#se puede hacer un una sola iteracion -> la momento de extraer los datos se puede agregar al grafo
# los horarios se deben separar para poder se procesados en el grafo

# se asume que todas las catedras y ayudantias son importantes y que el alumno debe asistir a todas las clases -> casi nadie valora las ayudanticas cambiar esto en el futuro.


# ver horario 2020 con los nuevos horarios 17:25
#"catedra":"LU JU 14:00 - 15:20" ||| 05 ->> cat1  "LU 14:00" | cat2 JU 14:00
# 
lista_secciones = [
	{'codigo':"CBF1000_CA05",'nombre':"MECÁNICA", 'seccion':"Sección 5", "horario":["VI 08:30","JU 14:00","VI 14:00"], "profesor": "EREMEEV VITALIE"},
	{'codigo':"CBF1000_CA07",'nombre':"ESTRUCTURAS DE DATOS", 'seccion':"Sección 10", "horario":["LU 10:00","JU 10:00","VI 10:00"] ,"profesor": "LEON ALEJANDRO"},
	{'codigo':"CBF1000_CA010",'nombre':"MECÁNICA", 'seccion':"Sección 7", "horario":["LU 17:25","JU 17:25","VI 17:25"] ,"profesor": "LAVIN ROBERTO OSVALDO"}
	]
#hacer lista de ramos dificiles o profes 
profesores_estrictos = ["LAVIN ROBERTO OSVALDO","EREMEEV VITALIE"] # se debe obtener esta lista desde otro lugar || desde una pagina que recopile la percepcion de los alumnos sobre los profesores (que tan bueno son para explicar ,rajon ,etc)
#crear encuesta !!

# TESTEAR la funcion get_peso !!!!
#-----------------------------------

#definir que significa cada posicion de este arreglo -> ejemplo la posicion 0 es que tanto le gustan los ramos a las 8.30
value_encuesta ={"ramos_830":1,"ventanas":3, "ramos_1725": 2, "profesores":3} # estas variables son las respuestas de la encuesta de las preferencias del alumno
def get_peso(value_encuesta,node):
	
	### SECCIONES EN BLOQUE 8.30
	bloque_a = False
	peso_ponderado = 0
	for elem in node["horario"]:
		if  elem[4] == 8:
			bloque_a=True
	if 	bloque_a:
		peso_ponderado += value_encuesta["ramos_830"]*4 #este 4 es la importancia que le damos a este parametro
	else:
		peso_ponderado += (value_encuesta["ramos_830"]-6)*4 #se usa el complemento de 6 al no tener la preferencia descrita.
	

	### SECCIONES EN BLOQUE 17.25
	bloque_g = False
	peso_ponderado = 0
	for elem in node["horario"]:
		if  elem[3] == 1 and elem[4] == 7:
			bloque_g=True
	if 	bloque_g:
		peso_ponderado += value_encuesta["ramos_1725"]*4 #este 4 es la importancia que le damos a este parametro
	else:
		peso_ponderado += (value_encuesta["ramos_1725"]-6)*4 #se usa el complemento de 6 al no tener la preferencia descrita.


	### ENCUESTA PROFESORES
	if node["profesor"] in profesores_estrictos:
		peso_ponderado += value_encuesta["profesores"] * 2
	else:
		peso_ponderado += (value_encuesta["profesores"]-6) * 2 # verificar si el complemento funciona

	
	peso_ponderado += value_encuesta["ramos_830"] *4 + value_encuesta["ventanas"]*3 + value_encuesta["dificil"] * 3 + value_encuesta["profesores"] * 2 
	#esto no esta bien
	return peso_ponderado

#asignar pesos a los nodos

for elem in lista_secciones: #aca se deberia asignar los pesos a los nodos.
	peso = get_peso(value_encuesta,elem)
	G.add_nodes_from([(elem["codigo"],{ "nombre": elem["nombre"],"seccion":elem["seccion"],"horario":elem["horario"],"peso":peso })])

# verificar por nombre de ramo, dos secciones del mismo ramo no pueden ser adyacente (no deben estar conectados)
# verificar por horario de catedra y ayudantia
# este aproach no es eficiente, se puede mejorar
# se asume que la informacion del excel es certera -> un nodo por seccion y no se repiten los nodos.
# se asume que los bloques de horarios son fijos, es decir todos parte a la misma hora dependiendo del bloque-> una clase de las 14 siempre terminara a las 15.20

list_node = list(G.nodes.items()) # es buena practica hcacer esto o los defino en los for ?
lenth_graph = len(list_node) 

for i  in range (lenth_graph): 
	if (i+1) < lenth_graph:
		for j in range (i+1,lenth_graph):
			if (list_node[i][1]["nombre"] != list_node[j][1]["nombre"]): #verificando que no se tomen dos secciones del mismo ramo
				tope=0
				for k in range (len(list_node[i][1]["horario"])): #sera mejor colocar varios if ?
					for x in range(list_node[j][1]["horario"]): #verificar esto, antes era un 3
						if (list_node[i][1]["horario"][k] == list_node[j][1]["horario"][x]): #verificando que no topen los horarios
							print()
							tope+=1
							break					
							
				if tope == 0:
					print(list_node[i][0], "Y",list_node[j][0], "->juntos")	
					#add_edge o como se llame la funcion
					
				else: 
					print(list_node[i][0], "Y",list_node[j][0], "-> no")
					
			else:
				print(list_node[i][0], "Y",list_node[j][0], "-> no")


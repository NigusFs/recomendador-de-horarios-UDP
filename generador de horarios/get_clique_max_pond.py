import networkx as nx

G = nx.Graph()
#push del excel de la oferta academica.
#se puede hacer un una sola iteracion -> la momento de extraer los datos se puede agregar al grafo
# los horarios se deben separar para poder se procesados en el grafo

#"catedra":"LU JU 14:00 - 15:20" ||| 05 ->>
# 
lista_secciones = [
	{'codigo':"CBF1000_CA05",'nombre':"MECÁNICA", 'seccion':"Sección 5", "horario":["LU 14:00","JU 14:00","VI 14:00"], "profesor": "EREMEEV VITALIE"},
	{'codigo':"CBF1000_CA07",'nombre':"MECÁNICA1", 'seccion':"Sección 10", "horario":["LU 10:00","JU 10:00","VI 10:00"] ,"profesor": "LEON ALEJANDRO"},
	{'codigo':"CBF1000_CA010",'nombre':"MECÁNICA", 'seccion':"Sección 7", "horario":["LU 14:00","JU 14:00","VI 14:00"] ,"profesor": "LEON ALEJANDRO"}
	]

for elem in lista_secciones:
	G.add_nodes_from([(elem["codigo"],{"nombre": elem["nombre"],"seccion":elem["seccion"],"horario":elem["horario"]})])

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
				for k in range (3): #sera mejor colocar varios if ?
					for x in range(3):
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

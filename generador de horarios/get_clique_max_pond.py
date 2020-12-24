import networkx as nx

G = nx.Graph()
#push del excel de la oferta academica.
#se puede hacer un una sola iteracion -> la momento de extraer los datos se puede agregar al grafo
lista_secciones = [
    {'codigo':"CBF1000_CA05",'nombre':"MECÁNICA", 'seccion':"Sección 5", "catedra":"LU JU 14:00 - 15:20","ayudantia":"VI 14:00 - 15:20", "profesor": "EREMEEV VITALIE"},
    {'codigo':"CBF1000_CA07",'nombre':"MECÁNICA", 'seccion':"Sección 10", "catedra":"LU JU 14:00 - 15:20","ayudantia":"VI 14:00 - 15:20" ,"profesor": "LEON ALEJANDRO"},
    {'codigo':"CBF1000_CA010",'nombre':"MECÁNICA", 'seccion':"Sección 7", "catedra":"LU JU 14:00 - 15:20","ayudantia":"VI 14:00 - 15:20" ,"profesor": "LEON ALEJANDRO"}
    ]

for elem in lista_secciones:
    G.add_nodes_from([(elem["nombre"],{"catedra":elem["catedra"], "ayudantia":elem["ayudantia"]})])

# verificar por nombre de ramo, dos secciones del mismo ramo no pueden ser adyacente (no deben estar conectados)
# verificar por horario de catedra y ayudantia

for elem1 in list(G.nodes.items()):
    for elem2 in list(G.nodes.items())
    if (elem1[0]["nombre"] != )
        print(elem[0],elem[1]["catedra"])

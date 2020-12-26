import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

PERT = nx.DiGraph()  #Grafo dirigido

excel = pd.read_excel('MallaCurricular.xlsx')

excelArray = np.array(excel)

semestre = int(input('Por favor, indique hasta que semestre tiene aprobado completamente \n'))

ramosNoAprobados = []

for aux in range(1, len(excelArray)):

    if int(excelArray[aux][4]) > semestre:
        ramosNoAprobados.append(excelArray[aux])

asignaturasNoCursadas = np.array(ramosNoAprobados)

#NO BORRAR DESCOMENTAR DESPUES print(asignaturasNoCursadas)

while(True):

    answer = input('¿Corresponden estos ramos a los que aun usted no ha cursado? Responda con yes/no \n')

    if answer == 'no':
        #añadir el if y el while para incluir respuestas incorrectas
        ramos = input('Por favor, ingrese el número de las asignaturas (la primera columna de la matriz entregada previamente) que ya aprobó, separados por comas \n')
        ramos = ramos.split(",")    

        for elem in ramos:
            result = np.where(asignaturasNoCursadas == int(elem))
            asignaturasNoCursadas = np.delete(asignaturasNoCursadas, result[0][0],0)

        print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')    
        #NO BORRAR DESCOMENTAR DESPUES print(asignaturasNoCursadas)
        break

    elif answer == 'yes':
        print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')
        #NO BORRAR DESCOMENTAR DESPUES print(asignaturasNoCursadas)
        break

    else:
        print('Por favor, ingrese una respuesta válida. \n')


#comienzo del proceso de añadir cada elemento de la lista de ramos no cursados, como nodos al grafo que corresponderá al PERT

rows = len(asignaturasNoCursadas)

idRamo = []
ramosAbre = []

for aux in range(rows):

    idRamo.append(asignaturasNoCursadas[aux][0])
    ramosAbre.append(asignaturasNoCursadas[aux][3])

    idAux = idRamo[aux]
    stringAux = ramosAbre[aux]

    if isinstance(stringAux, str):
        stringAux = [int(s) for s in stringAux.split(',')]   #convierte string de numeros a arreglo o lista
    #print(stringAux)
    PERT.add_nodes_from([idAux], abre=stringAux)

rows2 = len(idRamo)

#A continuacion, se crean las aristas que conectan cada nodo, con el respectivo ramo que abren. Estas aristas estan direccionadas.

for aux2 in range(rows2):
    
    idAux2 = idRamo[aux2]
    stringAux2 = ramosAbre[aux2]

    if isinstance(stringAux2, str):
        stringAux2 = [int(s) for s in stringAux2.split(',')]
        rows3 = len(stringAux2)
       
        for elem in range(rows3):
            PERT.add_edge(idAux2, stringAux2[elem])

    elif stringAux2 == 0:
        pass

    else:
        PERT.add_edge(idAux2, stringAux2)

    

#nx.draw_circular(PERT, with_labels=True, font_weight='bold')
#plt.show()

#Comienzan a establecerse los nodos criticos, los que deben cumplir con las 4 condiciones 

for elem in list(PERT.nodes):
    contador = 0
    lista = list(PERT.successors(elem))

    if PERT.out_degree[elem] != 0:
        #print(lista, elem)
        for elem2 in lista:                      #out_degree entrega el numero de aristas que salen del nodo. Si es 0, el nodo no tiene hijos. PRIMERA CONDICIÓN LISTA
            if not list(PERT[elem2]):            #PERT[elem2] indica que ramo abre el nodo, y esto se pasa a lista
                print('hello')    
            else:
                print(elem2)           
    else:
        pass


    


    

#ESTAS CONDICIONES SE DEBEN aAPLICAR PARA CADA ASIGNATURA QUE ABRA EL RAMO EN CUESTION.
#Calculo 1 no cumple con la condicion 4 para contabilidad, pero si la cumple para calculo 2, por lo que es critico.


#condicion 1: sea prerrequisito de un ramo
#condicion 2: que sea parte de una ruta critica que pertenezaca a más de 2 semestres, e.g mecanica no sirve ya que abre calor, el cual no abre más ramos.
#condicion 3: si un ramo requiere 2 o más ramos aprobados para tomarlo, estos serán criticos si, y solo si se pueden inscribir en la misma instancia, al mismo tiempo.
#             e.g calculo 3 y edo abren electro, pero solo serán criticos si se pueden tomar al mismo tiempo.
#condicion 4: el ramo será critico si el ramo que abre esta en el siguiente semestre. e.g calculo 1 abre contabilidad, pero el primero es del primer semestre
#             y conta es del semestre 7, por lo que para el caso de conta, no es critico.  


#condicion futura: tomar en cuenta el semestre actual del alumno y el que debera egresar, por temas de la practica 2.
#condicion futura: ver requisitos de los electivos. Conseguirselos con el profe, para asi establecer de mejor manera las rutas criticas.

#print(PERT.nodes.data())
#print(aux2)
#example = '0, 0, 1, 2, 31, 13, 41, 42'
#print(example)
#t = [int(s) for s in example.split(',')]
#print(t)
#recordar añadir la restricción del causal, para ver si se le deben recomendar 4 o 6 asignaturas para inscribir

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def getRamoCritico(nombreExcel):

    PERT = nx.DiGraph()  #Grafo dirigido

    ramosCriticos = []

    excel = pd.read_excel(nombreExcel)

    excelArray = np.array(excel)

    while(True):

        semestreAprobado = int(input('Por favor, indique hasta que semestre tiene aprobado completamente (número entre 0 y 10)\n'))
        semestreActual = int(input('Por favor, indique el semestre que esta cursando actualmente. (número entre 0 y 10)\n'))
    
        if semestreAprobado >= 0 and semestreAprobado <=10:
            if semestreActual >= 0 and semestreActual <=10:
                break
        else:
            print('Intente nuevamente')


    ramosNoAprobados = []

    for aux in range(1, len(excelArray)):

        if int(excelArray[aux][4]) > semestreAprobado:
            ramosNoAprobados.append(excelArray[aux])

    asignaturasNoCursadas = np.array(ramosNoAprobados)

    print(asignaturasNoCursadas)

    while(True):

        answer = input('¿Corresponden estos ramos a los que aun usted no ha cursado? Responda con yes/no \n')

        if answer == 'no':
        
            ramos = input('Por favor, ingrese el número de las asignaturas (la primera columna de la matriz entregada previamente) que ya aprobó, separados por comas \n')
            ramos = ramos.split(",")    

            for elem in ramos:
                result = np.where(asignaturasNoCursadas == int(elem))
                asignaturasNoCursadas = np.delete(asignaturasNoCursadas, result[0][0], 0)

            print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')    
            print(asignaturasNoCursadas)
            break

        elif answer == 'yes':
            print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')
            print(asignaturasNoCursadas)
            break

        else:
            print('Por favor, ingrese una respuesta válida. \n')


#comienzo del proceso de añadir cada elemento de la lista de ramos no cursados como nodos al grafo que corresponderá al PERT

    rows = len(asignaturasNoCursadas)

    idRamo = []
    ramosAbre = []
    semestreCurso = []
    nombreCurso = []

    for aux in range(rows):

        idRamo.append(asignaturasNoCursadas[aux][0])
        ramosAbre.append(asignaturasNoCursadas[aux][3])
        semestreCurso.append(asignaturasNoCursadas[aux][4])
        nombreCurso.append(asignaturasNoCursadas[aux][2])

        idAux = idRamo[aux]
        stringAux = ramosAbre[aux]
        semestreAux = semestreCurso[aux]
        nombreAux = nombreCurso[aux]

        if isinstance(stringAux, str):
            stringAux = [int(s) for s in stringAux.split(',')]   #convierte string de numeros a arreglo o lista
    
        PERT.add_nodes_from([idAux], abre=stringAux, semestre=semestreAux, nombre=nombreAux)

#print(PERT.nodes.data())

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
    if semestreAprobado < 9:
            apAux = []
            criticosAux = []
            for elem in list(PERT.nodes):
             
            #Si el alumno esta al día, se le entregan solo las asignaturas correspondientes al siguiente semestre.

                if semestreAprobado == semestreActual:             
                    if PERT.nodes[elem]['semestre'] == semestreActual+1:
                        ramosCriticos.append(elem)
                else:   
                    contador = 0
                    lista = list(PERT.successors(elem))

            #condicion 1: que el ramo sea prerrequisito
            #out_degree entrega el numero de aristas que salen del nodo. Si es 0, el nodo no tiene hijos. PRIMERA CONDICIÓN LISTA
            #PERT[elem2] indica que ramo abre el nodo, y esto se pasa a lista

                    if PERT.out_degree[elem] != 0:
                        contador = contador+1
                    else:
                        pass

        #condicion 2: ruta critica de 2 o más nodos criticos
        #single_source_shortest_path_length(grafo, nodo inicial, saltos) retorna un diccionario con la ruta del grafo direccionado

                    diccionario = nx.single_source_shortest_path_length(PERT, elem, 2)

                    if len(diccionario)>2:
                        contador = contador+1
                    else:
                        pass

                #condicion 3:
                #atribute = nx.get_node_attributes(PERT, 'semestre')
        
                    if PERT.out_degree[elem] != 0:
                        pNode = PERT.nodes[elem]['semestre']
                        succs = PERT.successors(elem)
                        for numb in list(succs):
                            nAux = PERT.nodes[numb]['semestre'] - PERT.nodes[elem]['semestre']
                            if nAux < 3:
                                contador = contador+1

                    else:
                        pass
            
        
                    if contador >= 3 and len(ramosCriticos) < 6:
                    #print(contador, elem)
                        criticosAux.append(elem)
                    #print(criticosAux)
                
                        for crit in range(len(criticosAux)):
                        #print(PERT.nodes[criticosAux[crit]]['abre'])
                        #print(type(PERT.nodes[criticosAux[crit]]['abre']))
                        #print('time')
                    
                    
                            if isinstance(PERT.nodes[criticosAux[crit]]['abre'], list):
                                if PERT.nodes[criticosAux[crit]]['abre'] in criticosAux:
                                    pass
                                else:
                            
                                    if criticosAux[crit] in ramosCriticos:
                                        pass                               
                                    else:
                                        ramosCriticos.append(criticosAux[crit])
                                                         
                            elif isinstance(PERT.nodes[criticosAux[crit]]['abre'], int):

                                apAux.append(PERT.nodes[criticosAux[crit]]['abre'])

                            #print(apAux)
                        
                                if criticosAux[crit] in ramosCriticos:                        
                                    pass
                                else:
                                #print(PERT.nodes[criticosAux[crit]]['abre'])
                                    if criticosAux[crit] in ramosCriticos:
                                        pass
                                    else:
                                        ramosCriticos.append(criticosAux[crit])
        
                    rf = ramosCriticos.copy()      
                    for elemento in rf:
                #print(elemento)
                #print(PERT.nodes[elemento]['abre'] )
            
                #elimina de la lista de nodos criticos a los que necesiten aprobar con anterioridad nodos criticos que ya estan en la lista.

                        abre = PERT.nodes[elemento]['abre']
            
                        if isinstance(abre, list):
                            for nums in range(len(abre)):
                                if abre[nums] in ramosCriticos:
                                    ramosCriticos.remove(abre[nums])

                        elif isinstance(abre, int):
                            if abre in ramosCriticos:
                                ramosCriticos.remove(abre)
            
            
        
            if len(ramosCriticos) < 6:
                listaNoCrit = list(PERT.nodes)
                for z in range(len(listaNoCrit)):
                    if len(ramosCriticos) == 6:
                        break
                    else:
                        if listaNoCrit[z] not in ramosCriticos:
                            ramosCriticos.append(listaNoCrit[z])
                        else:
                            pass
            nombreCriticos = []
            for y in ramosCriticos:
                nombreCriticos.append(PERT.nodes[y]['nombre'])
    return nombreCriticos

#print(getRamoCritico('MallaCurricular.xlsx'))

                

        
#ESTAS CONDICIONES SE DEBEN APLICAR PARA CADA ASIGNATURA QUE ABRA EL RAMO EN CUESTION.
#Calculo 1 no cumple con la condicion 4 para contabilidad, pero si la cumple para calculo 2, por lo que es critico.


#condicion 1: sea prerrequisito de un ramo
#condicion 2: que sea parte de una ruta critica que pertenezaca a más de 2 semestres, e.g mecanica no sirve ya que abre calor, el cual no abre más ramos.
#condicion 3: el ramo será critico si el ramo que abre esta en el siguiente semestre. e.g calculo 1 abre contabilidad, pero el primero es del primer semestre
#             y conta es del semestre 7, por lo que para el caso de conta, no es critico.
#


# condicion futura: si un ramo requiere 2 o más ramos aprobados para tomarlo, estos serán criticos, si y solo si, se pueden inscribir en la misma instancia, al mismo tiempo.
#             e.g calculo 3 y edo abren electro, pero solo serán criticos si se pueden tomar al mismo tiempo.  
#condicion futura: tomar en cuenta el semestre actual del alumno y el que debera egresar, por temas de la practica 2.
#condicion futura: ver requisitos de los electivos. Conseguirselos con el profe, para asi establecer de mejor manera las rutas criticas.

#print(PERT.nodes.data())
#print(aux2)
#example = '0, 0, 1, 2, 31, 13, 41, 42'
#print(example)
#t = [int(s) for s in example.split(',')]
#print(t)
#recordar añadir la restricción del causal, para ver si se le deben recomendar 4 o 6 asignaturas para inscribir

import pandas as pd
import numpy as np
import networkx as nx

G = nx.Graph()

excel = pd.read_excel('MallaCurricular.xlsx')

excelArray = np.array(excel)


#print(excel)
#print(excelArray)

semestre = int(input('Por favor, indique hasta que semestre tiene aprobado completamente \n'))

ramosNoAprobados = []

for aux in range(1, len(excelArray)):
    if int(excelArray[aux][4]) > semestre:
        ramosNoAprobados.append(excelArray[aux])

asignaturasNoCursadas = np.array(ramosNoAprobados)

print(asignaturasNoCursadas)

answer = input('¿Corresponden estos ramos a los que aun usted no ha cursado? Responda con yes/no \n')

if answer == 'no':

    ramos = input('Por favor, ingrese el número de las asignaturas (la primera columna de la matriz entregada previamente) que ya aprobó, separados por comas \n')
    ramos = ramos.split(",")
    #print(ramos)
    for elem in ramos:
        result = np.where(asignaturasNoCursadas == int(elem))
        asignaturasNoCursadas = np.delete(asignaturasNoCursadas, result[0][0], 0)
    print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')    
    print(asignaturasNoCursadas)
elif answer == 'yes':
    print('Por lo tanto, las asignaturas que usted aún no cursa corresponden a: \n')
    print(asignaturasNoCursadas)


#recordar añadir la restricción del causal, para ver si se le deben recomendar 4 o 6 asignaturas para inscribir



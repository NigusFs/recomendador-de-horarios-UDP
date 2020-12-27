import pandas as pd
import numpy as np
import networkx as nx

G = nx.Graph()

excel = pd.read_excel('MallaCurricular.xlsx')

excelArray = np.array(excel)


#print(excel)
#print(excelArray)

semestre = int(input('Hasta que semestre tienes aprobado de manera completa? \n'))

ramosNoAprobados = []

for aux in range(1, len(excelArray)):
    if int(excelArray[aux][4]) > semestre:
        ramosNoAprobados.append(excelArray[aux])

asignaturasNoCursadas = np.array(ramosNoAprobados)

print(asignaturasNoCursadas)

answer = input('¿Corresponden estos ramos a los que aun usted no ha cursado? \n')

if answer == 'no':

    ramos = input('Por favor, ingrese el número de las asignaturas que ya aprobó, separados por comas \n')
    ramos = ramos.split(",")
    #print(ramos)
    for elem in ramos:
        result = np.where(asignaturasNoCursadas == int(elem))
        asignaturasNoCursadas = np.delete(asignaturasNoCursadas, result[0][0], 0)

        
print(asignaturasNoCursadas)



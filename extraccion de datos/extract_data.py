#crislo fue parte importante de este codigo. Aceptenlo en la practica. gracias :D Saludos !

# Probado y testeado con la oferta academica 2019-1

import numpy as np
import pandas as pd

excel = pd.read_excel('PROGRAMACION CURSOS 2017-2020.xlsx', sheet_name='2019-1')
excelArray = np.array(excel)

lista_secciones=[]


for elem in excelArray:
	#print(elem)
	if isinstance(elem[5], str):
		if elem[5][0] == "C":
			aux_horario = [] # separar las catedras
			#print(elem[4])
			try:
				if len(elem[7].split()) == 5:
					aux = elem[7].split()[0]+" "+elem[7].split()[2] #if len(elem[7].split()) == 5 else elem[7].split()[0]+" "+elem[7].split()[1]
					aux_horario.append(aux)
					aux = elem[7].split()[1]+" "+elem[7].split()[2]
					aux_horario.append(aux)

			# ['LU JU 08:30 - 09:50']
			# ['LU 08:30', 'JU 08:30',]

			# VI 08:30 - 09:50 -> VI 08:30 

				codigo = elem[4]
				nombre = elem[2]
				seccion = elem[3]
				profesor = elem[9]
			except:
				pass 
			finally:
				continue
		elif elem[5][0] == "A":
			aux = elem[7].split()[0]+" "+elem[7].split()[1]
			aux_horario.append(aux)
		else:
			continue
	else:
		lista_secciones.append({'codigo':codigo,'nombre':nombre, 'seccion':seccion, "horario":aux_horario, "profesor":profesor})
#pushea en un arreglo o dict
		

print(lista_secciones[655])
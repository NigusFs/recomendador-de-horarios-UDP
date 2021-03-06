# Probado con la oferta academica 2019-1

import numpy as np
import pandas as pd

#solo se consideran Catedra y Ayudantias, no Laboratorios

def extract_data(arr_ramos_criticos,sheet_name='2019-1'): 

	count_cfg= arr_ramos_criticos.count("CFG") #cuenta cuantos cfg se deben tomar 
	excel = pd.read_excel('PROGRAMACION CURSOS 2017-2020.xlsx', sheet_name=sheet_name) #se obtiene los datos de la secciones de la oferta academica
	excelArray = np.array(excel)
	lista_secciones=[]

	for i in range (0,len(excelArray)):
		elem=excelArray[i]
		if isinstance(elem[5], str):
			if elem[5][0] == "C": #se verifica que la informacion de la fila sea una Catedra
				aux_horario = [] 
				try:
					if len(elem[7].split()) == 5: #se procesa los datos de los horarios para usarlos posteriormente
						aux = elem[7].split()[0]+" "+elem[7].split()[2] # se guarda el primer modulo de la Catedra ejemplo LU 08.30
						aux_horario.append(aux)
						aux = elem[7].split()[1]+" "+elem[7].split()[2] # se guarda el segundo modulo de la Catedra ejemplo MA 10.00
						aux_horario.append(aux)

					codigo = elem[4] 
					nombre = elem[2]
					seccion = elem[3]
					profesor = elem[9]
				except:
					pass 
				finally:
					continue
			elif elem[5][0] == "A": #se verifica que la informacion de la fila sea una Ayudantia
				aux = elem[7].split()[0]+" "+elem[7].split()[1]  # se guarda el primer modulo de la ayudantia ejemplo VI 17.25
				aux_horario.append(aux)
			else:
				continue
		else:
			if nombre in arr_ramos_criticos : 
				alfa = {'codigo':codigo,'nombre':nombre, 'seccion':seccion, "horario":aux_horario, "profesor":profesor}
				aux_count = 0
				for k in range(0,len(lista_secciones)): 
					if lista_secciones[k]["codigo"] == codigo: # se verifica si ya existe esta seccion en la lista de secciones (se evitan datos repetidos)
						aux_count+=1
				if aux_count == 0:
					lista_secciones.append(alfa)
					
			
	for i in range(0,count_cfg):
		if count_cfg < 10:
			codigo = "CFG_0"+str(i+1)
			lista_secciones.append({'codigo':codigo,'nombre':"CFG-"+str(i+1), 'seccion':"Sección "+str(i+1), "horario":[codigo] ,"profesor": "CFG"})
		else:
			codigo = "CFG_"+str(i+1)
			lista_secciones.append({'codigo':codigo,'nombre':"CFG-"+str(i+1), 'seccion':"Sección "+str(i+1), "horario":[codigo] ,"profesor": "CFG"})

	return lista_secciones





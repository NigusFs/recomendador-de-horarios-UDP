#crislo fue parte importante de este codigo. Aceptenlo en la practica. gracias :D Saludos !

# Probado y testeado con la oferta academica 2019-1

#se asume que el excel tiene la informacion correcta
import numpy as np
import pandas as pd


def extract_data(): #get ramos criticos
	arr_ramos_criticos=["PROGRAMACIÓN","PROBABILIDADES Y ESTADÍSTICAS","ELECTRÓNICA Y ELECTROTECNIA","CFG","CFG","COMUNICACIONES DIGITALES"]
	count_cfg= arr_ramos_criticos.count("CFG")
	print(count_cfg)
	excel = pd.read_excel('PROGRAMACION CURSOS 2017-2020.xlsx', sheet_name='2019-1')
	excelArray = np.array(excel)

	lista_secciones=[]


	for i in range (0,len(excelArray)):
		elem=excelArray[i]
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

					codigo = elem[4] #if isinstance(elem[4], str) == True else elem[1]
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
			#print(elem[2],"->",type(elem[2]))
			if nombre in arr_ramos_criticos :#and isinstance(excelArray[i+1][5], str) == False: # y si fuera un solo espacio ? # el si el utlima fila del excel terminar y fye
				#print(excelArray[i+1][5])
				alfa = {'codigo':codigo,'nombre':nombre, 'seccion':seccion, "horario":aux_horario, "profesor":profesor}
				aux_count = 0
				for k in range(0,len(lista_secciones)):
					if lista_secciones[k]["codigo"] == codigo:
						aux_count+=1
				if aux_count == 0:
					lista_secciones.append(alfa)
					

	#pushea en un arreglo o dict
			
	for i in range(0,count_cfg):
		if count_cfg < 10:
			codigo = "CFG_0"+str(i+1)
			lista_secciones.append({'codigo':codigo,'nombre':"CFG-"+str(i+1), 'seccion':"Sección "+str(i+1), "horario":[codigo] ,"profesor": "CFG"})
		else:
			codigo = "CFG_"+str(i+1)
			lista_secciones.append({'codigo':codigo,'nombre':"CFG-"+str(i+1), 'seccion':"Sección "+str(i+1), "horario":[codigo] ,"profesor": "CFG"})

	return lista_secciones




#print(extract_data(aux,int(count_cfg)))
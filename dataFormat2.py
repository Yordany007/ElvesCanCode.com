#!/usr/bin/env python

# - *- coding: utf - 8 - *-

import os, glob


# Ruta desde donde se ejecuta el script
DIR_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

# ruta de ficheros (/home/precis/files)
PWD = "/home/username/data"

# ficheros a formatear
os.chdir(PWD)
files = glob.glob("*")

# array de intervalo de annos
i = 1
years = []
lines = []


# crear directorio para salida del nuevo fichero formateado
if not os.path.exists(DIR_SCRIPT_PATH + "/filesFormated"):
	os.mkdir(DIR_SCRIPT_PATH + '/filesFormated')


for currentFile in files:
	with open(PWD +"/"+ currentFile, "r") as file:
		
		# lineas del fichero de datos a formatear
		lines = file.readlines()
		
		# seleccionar annos
		for line in lines:
			# limpiar finales de linea y espacios
			line = line.rstrip('\n')
			line = line.split(" ")
			
			if line[2] not in years:
				years.append(line[2])
				

		# salida de fichero formateado
		outputFile = open(DIR_SCRIPT_PATH + "/filesFormated/" + currentFile, "w")
		
		# escribir la cabecera del fichero		
		outputFile.write("Lon Lat")
		
		for year in years:
			outputFile.write(" " + year)
			
		outputFile.write("\n")
		
		# volver a ubicar el puntero al inicio del fichero
		#file.seek(0)
		
		# escribir valores del fichero
		for line in lines:
			# limpiar finales de linea y espacios
			line = line.rstrip('\n')
			line = line.split(" ")
			
			if i == 1:
				outputFile.write(line[0] + " " + line[1] + " " + line[3])
			elif i <= len(years):
				outputFile.write(" " + line[3])
			else:
				i = 0
				outputFile.write("\n")
				
			i += 1
		
		# reiniciar variables para el proximo fichero	
		years = []
		i = 1
		lines = []

#!/usr/bin/env python

# - *- coding: utf - 8 - *-

import os, glob

# ruta de ficheros (/home/precis/files)
PWD = "/home/username/Pictures/guyana/data"

def main():
	# ficheros a formatear
	os.chdir(PWD)
	files = []
	files = glob.glob("*")

	# cabecera del fichero (estaciones)
	headFile = ""
	stations = []
	month_values = [0 for x in range(181)]
	
	# valores missing
	consecutiveMissing = [0 for x in range(181)]
	randomMissing = [0 for x in range(181)]

	# cantidad de lineas fichero original
	i = 0

	# cantidad de lineas fichero formateado
	j = 0

	# iterador de linea
	iteratorLine = 0

	# fecha
	year = ""
	currentYear = ""
	month = ""
	currentMonth = ""

	# matriz para las nuevas lineas formateadas
	formatedLines = []
	
	# crear el primer fichero del rango de annos
	outputFile, currentYear = firstFile(PWD)

	# en caso de existir varios ficheros
	for currentFile in files:
		
		# crear directorio para salida de los nuevos ficheros formateados
		if not os.path.exists(PWD + "/filesFormated"):
			os.mkdir(PWD + '/filesFormated')
		
		# solo los ficheros (saltar los directorios)
		if os.path.isfile(PWD + "/" + currentFile):
		
			with open(PWD +"/"+ currentFile, "r") as file:
				
				lines = file.readlines()
				
				for line in lines:
					if i == 0:						
						# seleccionar estaciones de la cabecera del fichero
						headFile = line
						headFile = headFile.rstrip('\n')
						headFile = headFile.rstrip('\r')
						headFile = headFile.split("\t")
						
						for colunm in headFile:
							if colunm != 'Stations':
								stations.append(colunm)

					elif i > 3:
						# seleccionar lineas del fichero
						line = line.rstrip('\n')
						line = line.rstrip("\r")
						line = line.split("\t")
						year = line[0][0:4]
						month = line[0][4:6]

						if j == 0:
							# escribir la cabecera del fichero formateado
							for station in stations:
								
								if iteratorLine == 0:
									outputFile.write("fecha" + " " + "\"" + station + "\"")
								else:
									outputFile.write(" " + "\"" + station + "\"")
									
								iteratorLine = iteratorLine + 1
						
							outputFile.write("\n")
						iteratorLine = 0
						
						# sumatoria valores mensuales de estaciones
						if month == currentMonth:
							month_values, consecutiveMissing, randomMissing = sumatoriaValues(line, month_values, consecutiveMissing, randomMissing)


						# escribir acumulado de valores mensuales de estaciones
						if month != currentMonth:
							
							if currentMonth != "":
								writeFormatedValues(currentYear, currentMonth, month_values, outputFile)
								
							currentMonth = month							
							
							month_values = [0 for x in range(181)]
							consecutiveMissing = [0 for x in range(181)]
							randomMissing = [0 for x in range(181)]
							
							month_values, consecutiveMissing, randomMissing = sumatoriaValues(line, month_values, consecutiveMissing, randomMissing)
							
						if i == len(lines) - 1:
							# fin de fichero (para el ultimo mes que aparezca en el fichero, que no cambia.)
							month_values, consecutiveMissing, randomMissing = sumatoriaValues(line, month_values, consecutiveMissing, randomMissing)						
							writeFormatedValues(currentYear, currentMonth, month_values, outputFile)

						j = j + 1

						# crear un nuevo fichero por anno
						if year != currentYear:
							
							currentYear = year
							
							j = 0
							
							# salida de fichero formateado
							outputFile = open(PWD + "/filesFormated/" + currentYear, "w")

					i = i + 1
					

# actualizar lista de valores acumulativos de estaciones
def sumatoriaValues(line, month_values, consecutiveMissing, randomMissing):	
	
	iterator = 0
	
	for value in line:
		
		if iterator > 0:
			
			if consecutiveMissing[iterator - 1] < 7 and randomMissing[iterator - 1] < 15:
				
				try:
					value = float(value)
					
					if (value > 0):
						
						consecutiveMissing[iterator - 1] = 0
						
					elif (value < 0):
						
						value = -99
						consecutiveMissing[iterator - 1] += 1
						randomMissing[iterator - 1] += 1
						
				except ValueError:
					
					value = -99
					consecutiveMissing[iterator - 1] += 1
					randomMissing[iterator - 1] += 1


				if consecutiveMissing[iterator - 1] == 7 or randomMissing[iterator - 1] == 15:
					month_values[iterator - 1] = value
				else:
					if value > 0:
						month_values[iterator - 1] += value

			
		iterator = iterator + 1
	
	return month_values, consecutiveMissing, randomMissing
	
	
# escribir lista de valores acumulativos de estaciones en el mes
def writeFormatedValues(year, month, month_values, outputFile):
	date = year +""+ month
	outputFile.write(date)
	
	for value in month_values:
									
		value = str(value)		
		outputFile.write(" " + value)
			
		
	outputFile.write("\n")


# crear el primer fichero del rango de tiempo
def firstFile(PWD):
	i = 0
	year = ""

	# ficheros a formatear
	os.chdir(PWD)
	files = glob.glob("*")
	
	# en caso de existir varios ficheros
	for currentFile in files:
		
		# crear directorio para salida de los nuevos ficheros formateados
		if not os.path.exists(PWD + "/filesFormated"):
			os.mkdir(PWD + '/filesFormated')
		
		# solo los ficheros (saltar los directorios)
		if os.path.isfile(PWD + "/" + currentFile):
		
			with open(PWD +"/"+ currentFile, "r") as file:
				
				lines = file.readlines()
				
				for line in lines:
					if i == 4:
						# seleccionar lineas del fichero
						line = line.rstrip('\n')
						line = line.rstrip("\r")
						line = line.split("\t")
						year = line[0][0:4]
						break
					
					i = i + 1
	
	# salida de fichero formateado
	outputFile = open(PWD + "/filesFormated/" + year, "w")
	return outputFile, year


main()

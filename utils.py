import csv
import sys
from heapq import heappush, heappop
from collections import deque
import math
from grafo import Grafo

CONSTANTE_MAX = 999999


def imprimir_lista(lista):
	string = next(lista)
	for x in lista:
		string = string+" -> "+x
	print(string)
	
def calcular_costo_lista(grafo,lista):
	costo = 0
	for x in range(0,len(lista)-1):
		costo = costo +grafo.obtener_peso(lista[x],lista[x+1])
	return costo

def exportar_csv(dicc,grafo,nombre_archivo):
	cant_vertices = len(grafo.obtener_vertices())
	visitados = {}
	cola = deque()

	f = open(nombre_archivo,'w')
	writer = csv.writer(f)
	writer.writerow([str(cant_vertices)])

	for v in grafo:
		writer.writerow([v,dicc[v][0],dicc[v][1]])
		visitados[v] = False

	writer.writerow([cant_vertices-1])

	vertice_random = grafo.obtener_vertices()[0]
	visitados[vertice_random] = True
	cola.append(vertice_random)

	while cola:
		v = cola.pop()
		for ady in grafo.obtener_adyacentes(v):
			if visitados[ady] == False :
				peso =  grafo.obtener_peso(v,ady)
				writer.writerow([v,ady,str(peso)])
				visitados[ady] = True
				cola.append(ady)
	f.close() #FUNCIONA BIEN

def leer_csv(archivo_csv): #Retorna un grafo y un diccionario con las coordenadas de cada vertice
	dicc = {}
	grafo = Grafo(False	,True)
	with open(archivo_csv) as File:
		reader = csv.reader(File)
		cant_vertices = int((next(reader))[0])
		for i in range(0,cant_vertices): #El archivo me dice cuantos vertices son
			(nombre,coordenada1,coordenada2) = next(reader)
			dicc[nombre] = (coordenada1,coordenada2)
			grafo.agregar_vertice(nombre)

		cant_aristas = int((next(reader))[0])
		for x in range(0,cant_aristas):
			(nombre1,nombre2,peso) =  next(reader)
			peso = int(peso)
			grafo.agregar_arista(nombre1,nombre2,peso)
	File.close()
	return grafo,dicc

def leer_csv_recomendaciones(recomendaciones_csv):
	grafo = Grafo(True,False)
	f = open(recomendaciones_csv)
	reader = csv.reader(f)
	for x in reader:
		a_recorrer = x[0]
		depende = x[1]
		grafo.agregar_vertice(a_recorrer); # Si esta repetido en el csv no pasa nada
		grafo.agregar_vertice(depende)
		grafo.agregar_arista(depende,a_recorrer)
	f.close()
	return grafo


def lista_a_kml(lista,archivo_kml,dicc):
	with open(archivo_kml, "w") as f:
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write('<kml xmlns="http://earth.google.com/kml/2.1">\n')
		f.write("    <Document>\n")
		f.write("        <name>KML de RUSIA</name>\n")
		f.write("        <description>Mostrando el camino en KML.</description>\n")
		for i  in range(len(lista)): #creo los points de todos los vertices
			linea = lista[i]
			coord = dicc[linea]
			f.write("        <Placemark>\n")
			f.write("            <name>"+linea+"</name>\n")
			f.write("            <description>"+linea+"</description>\n")
			f.write("            <Point>\n")
			f.write("                <coordinates>" +coord[0]+", " + coord[1] + "</coordinates>\n")
			f.write("            </Point>\n")
			f.write("        </Placemark>\n")

		tam = len(lista)-1
		for i  in (range(0,tam)): #creo los points de todos los vertices
			linea = lista[i]
			prox_linea = lista[i+1]
			coord = dicc[linea]
			segunda_coord = dicc[prox_linea]
			f.write("        <Placemark>\n")
			f.write("            <LineString>\n")
			f.write("                <coordinates>"+coord[0]+", " + coord[1]+" "+segunda_coord[0]+", "+segunda_coord[1] +"</coordinates>\n")
			f.write("            </LineString>\n")
			f.write("        </Placemark>\n")
		f.write("    </Document>\n")
		f.write("</kml>\n") #FUNCIONA BIEN



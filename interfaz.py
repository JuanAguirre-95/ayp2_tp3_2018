import csv
import sys
from heapq import heappush, heappop
from collections import deque
import math
from grafo import Grafo
from utils import leer_csv, leer_csv_recomendaciones, imprimir_lista, lista_a_kml, exportar_csv, calcular_costo_lista
from biblioteca import camino_minimo, orden_topologico, arbol_tendido_minimo, viaje_aproximado, viajante_optimo

CONSTANTE_MAX = 999999

def imprimir_lista(lista):
	string = next(lista)
	for x in lista:
		string = string+" -> "+x
	print(string)
#=====COMANDOS=====

def ir(dicc,grafo,desde,hasta,nombre_kml): #FUNCIONA BIEN
	lista,distancia = camino_minimo(grafo,desde,hasta)
	reverse = reversed(lista)
	imprimir_lista(reverse)
	print("Costo total:",distancia)
	lista_a_kml(lista,nombre_kml,dicc)




def camino_recomendaciones(dicc,rusia,recomendaciones_csv,nombre_kml):
	grafo = leer_csv_recomendaciones(recomendaciones_csv)
	lista = orden_topologico(grafo)
	itera= iter(lista)
	imprimir_lista(itera)
	costo = calcular_costo_lista(rusia,lista)
	lista_a_kml(lista,nombre_kml,dicc)
	print("Costo total:",costo)


def reducir_caminos(dicc,grafo,nombre_archivo_csv):
	tendido_min,suma = arbol_tendido_minimo(grafo)
	exportar_csv(dicc,tendido_min, nombre_archivo_csv)
	print("Peso total:", suma)





def main():

	if (len(sys.argv) != 3):
		print("Cantidad de parametros erronea")

	lista_argumentos = sys.argv
	ciudades_csv =lista_argumentos[1]
	mapa_kml =lista_argumentos[2]


	rusia,dicc = leer_csv(ciudades_csv)

	for linea in sys.stdin:
		linea = linea.rstrip()
		linea = linea.split(" ")
		if(linea[0] == "ir"):
			temp = linea[1:]
			temp = " ".join(temp)
			temp = temp.split(",")
			desde = temp[0]
			hasta = temp[1].lstrip()
			ir(dicc,rusia,desde,hasta,mapa_kml)

		if(linea[0] == "viaje"):
			if(linea[1] == "aproximado,"):
				temp = linea[2:]
				temp = " ".join(temp)
				temp.lstrip()
				viaje_aproximado(dicc,rusia,temp,mapa_kml)
			if(linea[1] == "optimo,"):
				temp = linea[2:]
				temp = " ".join(temp)
				temp.lstrip()
				viajante_optimo(dicc,rusia,temp,mapa_kml)

		if(linea[0] == "itinerario"):
			camino_recomendaciones(dicc,rusia,linea[1],mapa_kml)
			
		if(linea[0] == "reducir_caminos"):
			reducir_caminos(dicc,rusia,linea[1])


main()

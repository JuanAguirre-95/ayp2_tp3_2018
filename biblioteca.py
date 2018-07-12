import csv
import sys
from heapq import heappush, heappop
from collections import deque
import math
from grafo import Grafo
from utils import imprimir_lista, lista_a_kml

CONSTANTE_MAX = 999999


def orden_topologico(grafo):
	grado_entrada = {}
	ordenado = []

	for vertices in grafo: #Pongo todos grados de entrada en 0
		grado_entrada[vertices] = 0

	for vertices in grafo: #Sumo los grados de entrada
		for ady  in grafo.obtener_adyacentes(vertices):
			grado_entrada[ady] +=1

	cola = deque()

	for vertice in grafo:
		if grado_entrada[vertice] == 0: #Si tiene grado de entrada 0 lo encolo
			cola.append(vertice)

	while cola:
		vertice_aux = cola.pop()
		ordenado.append(vertice_aux)
		for ady in grafo.obtener_adyacentes(vertice_aux):
			grado_entrada[ady] -=1
			if grado_entrada[ady] == 0:
				cola.append(ady)

	if len(ordenado) < len(grafo.obtener_vertices()):
		return None
	return ordenado


def camino_minimo(grafo,desde,hasta):
	padres = {}
	distancia = {}
	heapq = []

	for vertice in grafo:
		padres[vertice] = None
		distancia[vertice] = CONSTANTE_MAX

	distancia[desde]= 0

	principio = (distancia[desde],desde) #encolamos el principio con peso 0
	heappush(heapq,principio)

	while heapq:
		(dist,vert) = heappop(heapq)
		for ady in grafo.obtener_adyacentes(vert):
		   dista_candidato = distancia[vert] +  grafo.obtener_peso(vert,ady)
		   if(distancia[ady] > dista_candidato):
			   distancia[ady] = dista_candidato
			   padres[ady] = vert
			   if(ady == hasta):
				   break
			   encolar = (dista_candidato,ady)
			   heappush(heapq,encolar)

	lista = []
	lista.append(hasta)
	while padres[hasta]:
		nuevo_padre = padres[hasta]
		lista.append(nuevo_padre)
		padres[hasta] = padres[nuevo_padre]
	return lista,distancia[hasta]

def arbol_tendido_minimo(grafo_1):
	heapq = []
	visitados = {}
	grafo_n = Grafo(False,True)
	cant_vertices = len(grafo_1.obtener_vertices())
	peso_total = 0

	for v in grafo_1: #Pongo todos los vertices como no visitados
		visitados[v] = False

	vertice_random = grafo_1.obtener_vertices()[0]
	visitados[vertice_random] = True
	grafo_n.agregar_vertice(vertice_random)

	for ady in grafo_1.obtener_adyacentes(vertice_random): #Encolo los ady de vertice random
		peso = grafo_1.obtener_peso(vertice_random, ady)
		item = (peso,vertice_random,ady)
		heappush(heapq,item)
	contador = 1
	while contador < cant_vertices  and heapq:
		desencolado = heappop(heapq)
		vertice = desencolado[2]
		if visitados[vertice] == False:
			visitados[vertice] = True
			contador+=1
			grafo_n.agregar_vertice(vertice)
			grafo_n.agregar_arista(desencolado[1],vertice,desencolado[0])
			peso_total = peso_total + desencolado[0]
			for adya in grafo_1.obtener_adyacentes(vertice):
				if visitados[adya] == False:
					peso_aris = grafo_1.obtener_peso(vertice,adya)
					item_ady = (peso_aris,vertice,adya)
					heappush(heapq,item_ady)

	return grafo_n,peso_total







def psp_greedy(grafo,origen): #Retorna lista con orden y peso total
	orden_visitado = []
	visitados = {}
	cant_visitado = 0
	cant_vertices = len(grafo.obtener_vertices())
	peso_total = 0

	for v in grafo.obtener_vertices():
		visitados[v] = False

	orden_visitado.append(origen)
	actual = origen

	while cant_visitado < cant_vertices:
		heapq = []
		for ady in grafo.obtener_adyacentes(actual):
			if visitados[ady] ==True:
				continue
			peso = grafo.obtener_peso(actual,ady)
			dato = (peso,ady)
			heappush(heapq,dato)

		ady_min = heappop(heapq)
		peso_total = peso_total+ady_min[0]
		actual = ady_min[1]
		visitados[actual] = True
		cant_visitado+=1
		orden_visitado.append(actual)
	return orden_visitado,peso_total








def tdp_back(grafo, vert_ini, vert_act, actual,peso_recorrido, mejor_costo):

	lista_aux = actual.copy()
	lista_aux.append(vert_act)

	if(len(lista_aux) == len(grafo.obtener_vertices())):
		lista_aux.append(vert_ini)
		actual = lista_aux.copy()
		mejor_costo = peso_recorrido + grafo.obtener_peso(vert_act,vert_ini)		
		return mejor_costo,actual

	if mejor_costo <= peso_recorrido:
		return None,None

	for x in grafo.obtener_vertices():
		if x in lista_aux:
			continue
		peso_recorrido = peso_recorrido + grafo.obtener_peso(vert_act,x)
		costo_temp,aux = tdp_back(grafo,vert_ini,x,lista_aux,peso_recorrido,mejor_costo)
		if(costo_temp != None and  aux !=None):
			if(costo_temp < mejor_costo):
				mejor_costo = costo_temp
				actual = aux
		peso_recorrido = peso_recorrido - grafo.obtener_peso(vert_act,x)
	return mejor_costo,actual


def viaje_aproximado(dicc,grafo,desde,nombre_kml):
	camino,peso_total = psp_greedy(grafo,desde)
	itera = iter(camino)
	imprimir_lista(itera)
	print("Costo total:",peso_total)
	lista_a_kml(camino,nombre_kml,dicc)


def viajante_optimo(dicc,grafo,desde,nombre_kml):
	lista = []
	visited = {}
	mejor_costo =  CONSTANTE_MAX

	peso_recorrido = 0
	costo,lista = tdp_back(grafo,desde,desde,lista,peso_recorrido,mejor_costo)
	itera = iter(lista)
	imprimir_lista(itera)
	lista_a_kml(lista,nombre_kml,dicc)
	print("Costo total:",costo)
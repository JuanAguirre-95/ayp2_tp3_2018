import csv
from heapq import heappush, heappop
from collections import deque
import math
CONSTANTE_MAX = 999999

class Vertice:

	def __init__(self,valor = None):
		self.valor = valor
		self.aristas = {}

	def obtener_aristas(self):
		return self.aristas

	def obtener_valor(self):
		return self.valor
	def __str__(self):
		return self.valor

class Grafo:

	def __init__(self,dirigido = False, pesado = False):
		self.dict_vertices = {}
		self.cant_vertices = 0
		self.es_dirigido = dirigido
		self.es_pesado = pesado

	def __str__(self):
		return list(self.dict_vertices)

	def obtener_vertices(self):
		return list(self.dict_vertices)

	def cantidad_vertices(self):
		return self.cant_vertices

	def agregar_vertice(self,valor):

		if valor in self.dict_vertices:
			return False

		nuevo_vertice = Vertice(valor)

		self.dict_vertices[valor] = nuevo_vertice
		self.cant_vertices+=1
		return True

	def agregar_arista(self, vert1, vert2, peso = None):
		"""
			Si el grafo es dirigido la arista se agrega en vert1 nada mas
		"""
		if vert1 not in self.dict_vertices or vert2 not in self.dict_vertices:
				raise ValueError

		vertice1 = self.dict_vertices[vert1]
		vertice2 = self.dict_vertices[vert2]

		aristas1 = vertice1.obtener_aristas()
		aristas2 = vertice2.obtener_aristas()

		if vert1 in aristas2 or vert2 in aristas1:
			return False

		aristas1[vert2] = peso

		if  not self.es_dirigido : #si no  es dirigido

			aristas2[vert1] = peso
		return True

	def obtener_peso(self,vert1, vert2): #TODO armar raise de excepciones en caso de que no existan los vertices llamados
		"""
			PRE: Recibe el nombre de 2 vertices
			POST: Devuelve el peso de la arista que los une

			Excepciones:
				ValueError si no encuentra alguno de los vertices
		"""
		if not self.es_pesado:
			return None
		vertice = self.dict_vertices[vert1]
		aristas1 = vertice.obtener_aristas()
		return aristas1[vert2]

	def borrar_vertice(self, vertice):
		"""
			PRE: Recibe el nombre de un vertice
			POST: Borra el vertice del grafo (limpia las aristas de ese vertice tambien) y devuelve un booleano
				si esto ocurrio correctamente
		"""
		if vertice not in self.dict_vertices:
			return False
		if self.cant_vertices == 0:
			return True

		for w in self.dict_vertices:
			arist = self.dict_vertices[w].obtener_aristas()
			if vertice in arist:
				arist.pop(vertice)

		self.dict_vertices.pop(vertice)
		self.cant_vertices-=1
		return True

	def obtener_vertice(self,vertice):
		"""
			PRE: Recibe el nombre de un vertice
			POST: Devuelve el objeto Vertice con ese nombre
		"""
		return self.dict_vertices[vertice]

	def existe_arista(self,vert1,vert2):
		"""
			PRE: Recibe dos nombres de vertices
			POST: Devuelve true o false si existe arista

			Excepciones:
				ValueError en caso de que no exista alguno de los vertices
		"""
		if vert1 not in self.dict_vertices or vert2 not in self.dict_vertices:
			raise ValueError

		vertice1 = self.dict_vertices[vert1]
		vertice2 = self.dict_vertices[vert2]
		if vert2 not in vertice1.obtener_aristas():
			return False
		return True

	def obtener_adyacentes(self, vert1): #TODO Manejar excepciones
		"""
			PRE: Recibe un nombre de un vertice
			POST: Devuelve una lista de vertices adyacentes

			Excepciones:
				ValueError en caso de que no exista vertice
		"""
		vertice = self.dict_vertices[vert1]
		return vertice.obtener_aristas()

	def cantidad_vertices(self):
		return self.cantidad_vertices

	def __iter__(self):
		self.indice =0
		return self
	def __next__(self):
		try:
			lista = list(self.dict_vertices)
			result = lista[self.indice]
		except IndexError:
			raise StopIteration
		self.indice += 1
		return result


def arbol_tendido_minimo(grafo_1):
	heapq = []
	visitados = {}
	grafo_n = Grafo(False,True) #no es dirigido ?
	cant_vertices = len(grafo_1.obtener_vertices())

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
			for adya in grafo_1.obtener_adyacentes(vertice):
				if visitados[adya] == False:
					peso_aris = grafo_1.obtener_peso(vertice,adya)
					item_ady = (peso_aris,vertice,adya)
					heappush(heapq,item_ady)

	return grafo_n


def orden_topologico(grafo): #Ver el tema de return NONE si no puede-
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

	#Vuelvo sobre el padre y lo printeo reverseado
	lista = []
	lista.append(hasta)
	while padres[hasta]:
		nuevo_padre = padres[hasta]
		lista.append(nuevo_padre)
		padres[hasta] = padres[nuevo_padre]
	return lista,distancia[hasta]


def psp_greedy(grafo,origen):
	orden_visitado = []
	visitados = {}
	cant_visitado = 0
	cant_vertices = len(grafo.obtener_vertices())

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
		actual = ady_min[1]
		visitados[actual] = True
		cant_visitado+=1
		orden_visitado.append(actual)

	print(orden_visitado)







def leer_csv(archivo_csv): #Retorna un grafo y un diccionario con las coordenadas de cada vertice
	dicc = {}
	grafo = Grafo(True,True)
	with open(archivo_csv) as File:
		reader = csv.reader(File)
		cant_vertices = int((next(reader))[0])
		for i in range(0,cant_vertices): #El archivo me dice cuantos vertices son
			(nombre,coordenada1,coordenada2) = next(reader)
			dicc[nombre] = (coordenada1,coordenada2)
			grafo.agregar_vertice(nombre)

		cant_aristas = int((next(reader))[0])
		for i in range(0,cant_aristas):
			(nombre1,nombre2,peso) =  next(reader)
			peso = int(peso)
			grafo.agregar_arista(nombre1,nombre2,peso)
	File.close()
	return grafo,dicc

# FUNCIONES PARA LA INTERFAZ

def ir(dicc,grafo,desde,hasta): #FUNCIONA BIEN
	lista,distancia = camino_minimo(grafo,desde,hasta)
	reverse = reversed(lista)
	string = next(reverse)

	for x in reverse:
		string = string+" -> "+x

	print(string)
	print("Costo total:",distancia)

	#EXPORTAR MAPA KML














def main():
	#En dicc estan las coordenadas de cada vertice
	print("Pruebas leer csv....\n")
	rusia,dicc = leer_csv("sedes.csv") #Leo csv y armo grafo
	if rusia and dicc:
		print("Se leyo correcamente\n")


	#PROBANDO IR
	ir(dicc,rusia,"Moscu","Sochi")


































main()

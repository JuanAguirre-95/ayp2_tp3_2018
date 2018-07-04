
from heapq import heappush, heappop
from collections import deque

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
			++contador
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
		distancia[vertice] = 100000 # cambiarlo a una constante
	distancia[desde]= 0

	principio = (distancia[desde],desde) #encolamos el principio con peso 0
	vertices_visitados = 0
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
		++vertices_visitados
	#Vuelvo sobre el padre y lo printeo reverseado
	lista = []
	lista.append(hasta)
	while padres[hasta]:
		nuevo_padre = padres[hasta]
		lista.append(nuevo_padre)
		padres[hasta] = padres[nuevo_padre]
	print(lista[::-1])


def main():

		print("==========PRUEBAS TENDIDO MINIMO: PRIM==========")
		print()
		#https://jariasf.files.wordpress.com/2012/04/kruskal20.jpg
		#con arista de 2 a 3 peso 10.

		grafo_n = Grafo(False,True)
		#Vertices
		grafo_n.agregar_vertice('1')
		grafo_n.agregar_vertice('2')
		grafo_n.agregar_vertice('3')
		grafo_n.agregar_vertice('4')
		grafo_n.agregar_vertice('5')
		grafo_n.agregar_vertice('6')
		grafo_n.agregar_vertice('7')
		grafo_n.agregar_vertice('8')
		grafo_n.agregar_vertice('9')
		#Aristas
		grafo_n.agregar_arista("1","2",4)
		grafo_n.agregar_arista("1","8",9)
		grafo_n.agregar_arista("2","3",10)
		grafo_n.agregar_arista("2","8",11)
		grafo_n.agregar_arista("3","9",2)
		grafo_n.agregar_arista("3","4",7)
		grafo_n.agregar_arista("3","6",4)
		grafo_n.agregar_arista("4","5",10)
		grafo_n.agregar_arista("4","6",15)
		grafo_n.agregar_arista("5","6",11)
		grafo_n.agregar_arista("6","7",2)
		grafo_n.agregar_arista("7","8",1)
		grafo_n.agregar_arista("7","9",6)
		grafo_n.agregar_arista("8","9",7)

		#Hago esto para ver el grafo
		lista = []
		for v in grafo_n:
			for ady in grafo_n.obtener_adyacentes(v):
				arista= v+"-"+ady
				lista.append(arista)

		separador = ','
		guardar =  ("%s:%s" % (len(grafo_n.obtener_vertices()),separador.join(lista)))
		print("Link para ver el grafo generado antes de tendido minimo: http://g.ivank.net/#"+guardar)
		print()

		grafo_s = arbol_tendido_minimo(grafo_n) #ARBOL DE TENDIDO MINIMO

		lista = []
		for v in grafo_s:
			for ady in grafo_s.obtener_adyacentes(v):
				arista= v+"-"+ady
				lista.append(arista)

		separador = ','
		guardar =  ("%s:%s" % (len(grafo_n.obtener_vertices()),separador.join(lista)))
		print("Link para ver el grafo generado con tendido minimo: http://g.ivank.net/#"+guardar)
		print()



		print("==========PRUEBAS ORDEN TOPOLOGICO=========") #ORDEN TOPOLOGICO
		grafo_2 = Grafo(True,False)
		#Vertices
		grafo_2.agregar_vertice("Calcetines")
		grafo_2.agregar_vertice("Pantalon")
		grafo_2.agregar_vertice("Camisa")
		grafo_2.agregar_vertice("Zapatos")
		grafo_2.agregar_vertice("Cinturon")
		grafo_2.agregar_vertice("Jersey")

		#Aristas
		grafo_2.agregar_arista("Calcetines", "Zapatos")
		grafo_2.agregar_arista("Pantalon","Zapatos")
		grafo_2.agregar_arista("Pantalon","Cinturon")
		grafo_2.agregar_arista("Camisa","Cinturon")
		grafo_2.agregar_arista("Camisa","Jersey")

		lista = orden_topologico(grafo_2)
		print (lista)
		print()



		print("==========PRUEBAS CAMINO MINIMO=========") #PRUEBA CAMINO MINIMO
		#Use este grafo
		#http://www.myassignmenthelp.net/images/dijkstra-shortest-path-algorithm-output.png


		grafo_d = Grafo(True,True)
		#Vertices
		grafo_d.agregar_vertice('1')
		grafo_d.agregar_vertice('2')
		grafo_d.agregar_vertice('3')
		grafo_d.agregar_vertice('4')
		grafo_d.agregar_vertice('5')
		grafo_d.agregar_vertice('6')

		#Aristas
		grafo_d.agregar_arista("1", "2",2)
		grafo_d.agregar_arista("1", "3",4)
		grafo_d.agregar_arista("2", "4",4)
		grafo_d.agregar_arista("2", "5",2)
		grafo_d.agregar_arista("2", "3",1)
		grafo_d.agregar_arista("3", "5",3)
		grafo_d.agregar_arista("4", "6",2)
		grafo_d.agregar_arista("5", "6",2)

		print("Espero 1-2-5-6")
		camino_minimo(grafo_d,"1","6")

		#Otro ejemplo camino minimo
		#https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Dijkstrapaso8.jpg/400px-Dijkstrapaso8.jpg

		grafo_d = Grafo(False,True)
		#Vertices
		grafo_d.agregar_vertice('a')
		grafo_d.agregar_vertice('b')
		grafo_d.agregar_vertice('c')
		grafo_d.agregar_vertice('d')
		grafo_d.agregar_vertice('e')
		grafo_d.agregar_vertice('f')
		grafo_d.agregar_vertice('g')
		grafo_d.agregar_vertice('z')
		#Aristas
		grafo_d.agregar_arista("a", "b",16)
		grafo_d.agregar_arista("a", "c",10)
		grafo_d.agregar_arista("a", "d",5)
		grafo_d.agregar_arista("b", "g",6)
		grafo_d.agregar_arista("b", "c",2)
		grafo_d.agregar_arista("b", "f",4)
		grafo_d.agregar_arista("c", "f",12)
		grafo_d.agregar_arista("c", "e",10)
		grafo_d.agregar_arista("c", "d",4)
		grafo_d.agregar_arista("d", "e",15)
		grafo_d.agregar_arista("f", "e",3)
		grafo_d.agregar_arista("e", "z",5)
		grafo_d.agregar_arista("f", "g",8)
		grafo_d.agregar_arista("f", "z",16)
		grafo_d.agregar_arista("g", "z",7)
		print("Espero: a-d-c-b-f-e-z")
		camino_minimo(grafo_d,"a","z")









































main()

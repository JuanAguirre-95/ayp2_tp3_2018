class Vertice:
	"""
	Vertice para la clase grafo
	"""

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
	"""
	Grafo implementado sobre diccionarios
	"""

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
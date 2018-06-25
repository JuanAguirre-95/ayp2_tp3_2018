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
		self.cant_vertices = 0;
		self.es_dirigido = dirigido
		self.es_pesado = pesado
	def __str__(self):
		return str(list(self.dict_vertices))
	def vertices(self):
		return self.dict_vertices
	
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

		if not self.es_dirigido: #si es dirigido
			aristas2[vert1] = peso
		return True

	def obtener_peso(self,vert1, vert2):
		if not self.es_pesado:
			return None

		aristas1 = vert1.obtener_aristas()
		return aristas1[vert2]

	def borrar_vertice(self, vertice):
		if vertice not in self.dict_vertices:
			return False

		for w in self.dict_vertices:
			arist = self.dict_vertices[w].obtener_aristas()
			if vertice in arist:
				arist.pop(vertice)

		self.dict_vertices.pop(vertice)
		return True

	def obtener_vertice(self,vertice):
		return self.dict_vertices[vertice]
def main():
	grafo = Grafo(False,False)

	grafo.agregar_vertice("hola")
	grafo.agregar_vertice("mundo")
	grafo.agregar_vertice("que tal")

	grafo.agregar_arista("hola","mundo")
	grafo.agregar_arista("hola","que tal")

	vertice = grafo.obtener_vertice("hola")
	vertice2 = grafo.obtener_vertice("mundo")


	print(vertice2.obtener_aristas())
	print(vertice.obtener_aristas())
	print(grafo.vertices())
	grafo.borrar_vertice("hola")
	print(grafo.vertices())
	print(vertice2.obtener_aristas())

main()	
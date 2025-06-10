from dataclasses import dataclass

from database.DAO import DAO
from model.modello import Model

model = Model()
dao = DAO()
nodes = dao.get_all_nodes(2000, "flash")
#print(nodes)
print(len(nodes))
edges = dao.get_all_edges(2000, "flash", model.idSightings )

print(len(edges))
for edge in edges:
    sight1 = edge[0]
    sight2 = edge[1]
    print(sight1)
for sight in model.idSightings.values():
    print(sight)
lista = model.ordina_lista()
print(lista)

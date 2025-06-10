from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.idSightings = {}
        for sighting in DAO.get_all_sightings():
            self.idSightings[sighting.id] = sighting
        self.graph = nx.DiGraph()
        self.archi = []

    def build_graph(self, year, shape):
        self.graph.clear()
        nodes = DAO.get_all_nodes(year, shape)
        self.graph.add_nodes_from(nodes)
        edges = DAO.get_all_edges(year, shape, self.idSightings)
        for edge in edges:
            sight1 = edge[0]
            sight2 = edge[1]
            self.arco(sight1, sight2)



    def arco(self, sight1, sight2):

        long1 = sight1.longitude
        long2 = sight2.longitude

        if long1 < long2:
            peso = abs(long1 - long2)
            self.graph.add_edge(sight1, sight2, weight=peso)
            self.archi.append((sight1, sight2, peso))
        else:
            peso = abs(long2 - long1)
            self.graph.add_edge(sight2, sight1, weight=peso)
            self.archi.append((sight2, sight1, peso))

    def ordina_lista(self):
        self.archi.sort(key=lambda x: x[2], reverse=True)
        return self.archi[:5]






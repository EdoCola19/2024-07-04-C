from collections import defaultdict

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.sights = {}
        all_sighitings = DAO.get_all_sightings()
        for sight in all_sighitings:
            self.sights[sight.id] = sight
        self.edges = []
        self.best_score = 0
        self.best_path = []

    def build_graph(self, year, shape):
        self._graph.clear()
        nodes = DAO.get_nodes(year,shape)
        for node in nodes:
            self._graph.add_node(node)
        edges = DAO.get_edges(year, shape)
        for edge in edges:
            id1 = edge["id1"]
            id2 = edge["id2"]
            sight1 = self.sights[id1]
            sight2 = self.sights[id2]
            if sight1.longitude < sight2.longitude:
                peso = (sight2.longitude - sight1.longitude)
                if peso < 0:
                    peso = peso * (-1)
                self._graph.add_edge(sight1, sight2, peso=peso)
                self.edges.append((sight1, sight2, peso))
            elif sight2.longitude < sight1.longitude:
                peso = (sight1.longitude - sight2.longitude)
                if peso < 0:
                    peso = peso * (-1)
                self._graph.add_edge(sight2, sight1, peso=peso)
                self.edges.append((sight2, sight1, peso))

    def trova_cammino_migliore(self):
        self.best_score = 0
        self.best_path = []

        for nodo in self._graph.nodes:
            path = [nodo]
            mesi = defaultdict(int)
            mesi[nodo.datetime.month] = 1
            self._search(nodo, path, mesi, nodo.duration, 100, nodo.datetime.month)

    def _search(self, current, path, mesi_count, last_duration, score, mese_prec):
        if score > self.best_score:
            self.best_score = score
            self.best_path = list(path)

        for succ in self._graph.successors(current):
            if succ in path:
                continue
            if succ.duration <= last_duration:
                continue

            mese_attuale = succ.datetime.month
            if mesi_count[mese_attuale] >= 3:
                continue

            nuovo_punteggio = score + 100
            if mese_attuale == mese_prec:
                nuovo_punteggio += 200

            path.append(succ)
            mesi_count[mese_attuale] += 1

            self._search(succ, path, mesi_count, succ.duration, nuovo_punteggio, mese_attuale)

            path.pop()
            mesi_count[mese_attuale] -= 1









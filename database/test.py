from database.DAO import DAO
from model.modello import Model

model = Model()
dao = DAO()
years = dao.get_years()
print(years)

shapes = dao.get_shapes(1996)
print(shapes
      )

edges = dao.get_edges(1996, "circle")
print(edges)
edgs =model.edges
print(edgs)

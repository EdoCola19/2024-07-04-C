import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        if year is None or shape is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno e una forma prima di procedere"))
            self._view._page.update()
            return
        self._model.build_graph(year, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Grafo costruito con {self._model.graph.number_of_nodes()} nodi e {self._model.graph.number_of_edges()} archi"))
        for arco in self._model.ordina_lista():
            self._view.txt_result1.controls.append(ft.Text(f"{arco[0].id} --> {arco[1].id} | weight = {arco[2]}"))

        self._view._page.update()

    def handle_path(self, e):
        pass

    def fillDD_year(self):
        years = DAO.get_all_years()
        for year in  years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view._page.update()

    def fillDDShapes(self, e):
        year = self._view.ddyear.value
        shapes = DAO.get_all_shapes_for_years(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view._page.update()



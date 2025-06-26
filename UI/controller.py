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
        if not year or not shape:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f""
                 f"Devi selezionare sia un anno sia una forma prima di continuare!"))
            self._view._page.update()

        self._model.build_graph(year,shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model._graph.number_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model._graph.number_of_edges()}"))
        lista = self._model.edges
        lista_ordinata = sorted(lista, key=lambda x: x[2], reverse = True)
        for sight1,sight2,peso in lista_ordinata[:5]:
            self._view.txt_result1.controls.append(ft.Text(f"{sight1.id} --> {sight2.id} | weight: {peso}"))
        self._view._page.update()



    def handle_path(self, e):
        self._model.trova_cammino_migliore()

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio massimo: {self._model.best_score}", size=20)
        )
        for sighting in self._model.best_path:
            self._view.txt_result2.controls.append(
                ft.Text(f"{sighting.id} - {sighting.datetime.strftime('%Y-%m-%d')} - durata: {sighting.duration} s")
            )
        self._view._page.update()

    def fillddyear(self):
        years = DAO.get_years()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year["year"]))
        self._view._page.update()

    def handle_year_change(self, e):
        selected_year = self._view.ddyear.value
        if selected_year:
            self.fillddshape(selected_year)

    def fillddshape(self, year):
        self._view.ddshape.clean()
        shapes = DAO.get_shapes(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape["shape"]))
        self._view._page.update()



import flet as ft
import networkx as nx
from networkx.classes import neighbors

from database.Country import Country
from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_input_year_change(self, event):
        self._model.selected_year = event.data

    def handle_button_calcola(self, event):
        y = int(self._model.selected_year)
        if y is None or y < 1816 or y > 2016:
            self._view.create_alert("Anno selezionato non corretto, deve essere tra il 1816 e 2016")
            return

        self.create_graph(y)
        self.print_details()
        self._view.update_page()

    def create_graph(self, year: int):
        """
        Crea il grafo con i confini dell'anno selezionato.
        Il grafo ha tanti nodi quanti sono gli stati
        Quelli che hanno una connessioni sono gli stati che hanno un confine via terra
        """
        res = DAO.read_contiguities(max_year=year)
        graph = nx.Graph()

        for border in res:
            a = border.country_code_a
            b = border.country_code_b

            exists_a = graph.has_node(Country.prep_for_check(a))
            exists_b = graph.has_node(Country.prep_for_check(b))

            if not exists_a and exists_b:
                graph.add_node(border.country_a)
            elif exists_a and not exists_b:
                graph.add_node(border.country_b)
            elif not exists_a and not exists_b:
                graph.add_node(border.country_a)
                graph.add_node(border.country_b)

            graph.add_edge(a, b)

        self._model.graph = graph
        # Come nodo utilizzo una classe Country
        # Il DAO si occupa di permettermi di iterare le istanze della tabella contiguity
        # Per ogni connessione A, B se è del tipo specificato allora creo una nuova connessione nel grafo
        # Il grafo è contenuto nel model

    def handle_stati_raggiungibili_click(self, event):
        cs = self.list_reachable_countries_from(int(self._model.selected_country_code))

        txt_result: ft.ListView = self._view._txt_result
        txt_result.controls = [
            ft.Text(c.full_name) for c in cs
        ]
        self._view.update_page()

    def print_details(self):
        graph = self._model.graph
        if graph is None:
            return

        txt_result: ft.ListView = self._view._txt_result
        txt_result.controls = [
            ft.Text(f"Numero di componenti connesse: {nx.number_connected_components(graph)}")
        ]

        # Dettaglio dei nodi --> Numero di paesi con cui confina ogni nodo
        for node, adiacents in graph.adj.items():
            neighbors = adiacents.items()
            p = len(neighbors)

            txt_result.controls.append(ft.Text(f"{node.full_name} confina con {p} stati"))

    def handle_selected_item_change(self, event):
        self._model.selected_country_code = event.data

    def  list_reachable_countries_from(self, source_code: int) -> list[Country]:
        """
        Lista i paesi raggiungibili a partire da un determinato paese
        """
        graph = self._model.graph
        if not graph.has_node(Country.prep_for_check(source_code)):
            self._view.create_alert("Hai selezionato uno stato che non esisteva durante quell'anno")
            return []

        tree = nx.dfs_tree(graph, Country.prep_for_check(source_code))
        l = []
        for node, _ in tree.adj.items():
            l.append(DAO.read_country_by_id(node))

        return l

    def create_countries_dropdown(self) -> ft.Dropdown:
        countries = DAO.read_countries()

        options = [ ft.dropdown.Option(
            key=str(c.code),
            text=c.full_name
        ) for c in countries]
        d = ft.Dropdown(
            options=options,
            on_change=self.handle_selected_item_change,
            label="Stato",
            hint_text="Seleziona uno stato"
        )

        return d
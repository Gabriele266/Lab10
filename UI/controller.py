import flet as ft
import networkx as nx

from database.Country import Country
from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

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
        pass
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph: nx.Graph | None = None          # Grafo creato dalla funzione
        self.selected_year: int | None = None       # Anno selezionato nel menu dropdown
        self.selected_country_code: str | None   = None   # Codice del paese selezionato
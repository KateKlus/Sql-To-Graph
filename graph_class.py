

class Graph:
    def __init__(self):
        self.graph = [('R', 'R')]

    # Добавляем узел
    def add_node(self, node_name, parent, tables):
        self.graph.append((node_name, parent))
        for table in tables:
            self.graph.append((node_name, table))

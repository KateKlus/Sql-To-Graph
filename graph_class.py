
class Graph:
    def __init__(self):
        self.graph = [('R', 'R')]

    # Добавляем узел
    def add_node(self, node_name, parent, tables):
        self.graph.append((node_name, parent))
        for table in tables:
            if table != '':
                self.graph.append((node_name, table))

    # Вернем список узлов
    def get_node_list(self):
        return self.graph

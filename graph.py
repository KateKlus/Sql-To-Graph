import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, graph_layout='spring',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               text_font='sans-serif'):

    # Создаем граф
    g = nx.Graph()

    # Добавляем соединительные линии
    for edge in graph:
        g.add_edge(edge[0], edge[1])

    # Выбираем шаблон отображения
    if graph_layout == 'spring':
        graph_pos = nx.spring_layout(g)
    elif graph_layout == 'spectral':
        graph_pos = nx.spectral_layout(g)
    elif graph_layout == 'random':
        graph_pos = nx.random_layout(g)
    else:
        graph_pos = nx.shell_layout(g)

    # Отрисовываем граф
    nx.draw_networkx_nodes(g, graph_pos, node_size=node_size,
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(g, graph_pos, width=edge_tickness,
                           alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(g, graph_pos, font_size=node_text_size,
                            font_family=text_font)

    # Показываем граф
    plt.show()

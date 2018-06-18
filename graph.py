import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, graph_layout='spring',
               node_size=1600, node_alpha=0.3,
               node_text_size=12, edge_alpha=0.3, edge_tickness=1,
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

    # Окрашиваем узлы в соответствии с типом
    color_map = []
    legend_map = []
    for node in g:
        if node == 'R':
            color_map.append('red')
            legend_map.append('Final result')
        elif node[0] == 's':
            color_map.append('blue')
            legend_map.append('Subqueries')
        else:
            color_map.append('green')
            legend_map.append('Tables')

    # Отрисовываем граф
    nx.draw_networkx_nodes(g, graph_pos, node_size=node_size,
                           alpha=node_alpha, node_color=color_map)
    nx.draw_networkx_edges(g, graph_pos, width=edge_tickness,
                           alpha=edge_alpha, edge_color='black')
    nx.draw_networkx_labels(g, graph_pos, font_size=node_text_size,
                            font_family=text_font)

    # TODO добавить отрисовку легенды
    # Показываем граф
    plt.show()

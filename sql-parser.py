import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import string


alphabet = list(string.ascii_uppercase)


# Получаем строку из файла и подготавливаем
def get_string(string):
    for line in string:
        line = line.strip()
        print(line)
        return line


def sql_to_graph(query_string):
    graph = ""
    ddd = ""
    select_list = query_string.strip().split("select")
    result_list = []

    for x in range(len(select_list)):
        if (select_list[0] == " " or select_list[0] == "") and x == 0:
            pass
        else:
            result_list.append("select" + select_list[x])

    num_graph = []
    b_graph = [""] * len(result_list)
    maximum = 0
    for x in range(len(result_list)):
        count_open = ddd.count('(')
        count_close = ddd.count(')')
        num_graph.append(count_open - count_close)
        ddd += result_list[x]
        if (count_open - count_close) > maximum:
            maximum = count_open - count_close
    global index_graph
    index_graph = 0
    for y in range(maximum + 1):
        index_graph = 0
        global proverit
        proverit = False
        for x in range(len(result_list)):
            if num_graph[x] == 0 and proverit is True:
                index_graph += 1
            if num_graph[x] < 0:
                index_graph = 0
                proverit = False
            if num_graph[x] >= 0:
                b_graph[x] = (b_graph[x] + alphabet[index_graph])
                proverit = True
            num_graph[x] -= 1

    for x in range(len(result_list)):
        count_open = ddd.count('(')
        count_close = ddd.count(')')
        num_graph[x] = count_open - count_close
        ddd += "select " + result_list[x]
        if (count_open - count_close) > maximum:
            maximum = count_open - count_close

    for x in range(len(result_list)):
        graph += b_graph[x]
        graph += "\t"
        for y in range(num_graph[x]):
            graph += "\t"
        graph += result_list[x] + "\n"
    print(graph)
    #b_graph.reverse()
    adjacency_list = b_graph_to_adjacency_list(b_graph)
    draw_graph(adjacency_list)


def b_graph_to_adjacency_list(b_graph):
    adjacency_list = {}
    for n in range(1, len(b_graph) + 1):
        adjacency_list.update({n: []})
    for n in adjacency_list:
        node = b_graph[n - 1]
        for i in b_graph:
            if i.startswith(node):
                nodes = adjacency_list.get(n)
                nodes.append(b_graph.index(i) + 1)
                adjacency_list.update({n: nodes})
    adjacency_list.update({0: []})
    for i in b_graph:
        if len(i) == 1:
            root_nodes = adjacency_list.get(0)
            root_nodes.append(b_graph.index(i) + 1)
            adjacency_list.update({0: root_nodes})

    print(adjacency_list)
    print(b_graph)
    return adjacency_list


def draw_graph(adjacency_list):
    g = nx.MultiDiGraph()
    g.add_nodes_from(adjacency_list.keys())
    for k, v in adjacency_list.items():
        g.add_edges_from(([(k, t) for t in v]))

    print(g)

    node_size = 500
    node_alpha = 0.3
    node_text_size = 12
    edge_alpha = 0.3
    edge_tickness = 1
    text_font = 'sans-serif'

    # Окрашиваем узлы в соответствии с типом
    color_map = []
    legend_map = []
    for node in g:
        if node == 0:
            color_map.append('red')
        else:
            color_map.append('green')
            legend_map.append('Tables')

    graph_pos = graphviz_layout(g)
    nx.draw_networkx_nodes(g, graph_pos, node_size=node_size, alpha=node_alpha, node_color=color_map)
    nx.draw_networkx_edges(g, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color='black')
    nx.draw_networkx_labels(g, graph_pos, font_size=node_text_size, font_family=text_font)

    plt.show()


input_data = open('./input-data/sql/m5.sql', 'r')
query_str = get_string(input_data)
sql_to_graph(query_str)

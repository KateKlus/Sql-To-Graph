import networkx as nx
from graphviz import Digraph
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
    adjacency_list = b_graph_to_adjacency_list(b_graph)
    draw_graph(adjacency_list)


def b_graph_to_adjacency_list(b_graph):
    adjacency_list = {}
    for n in b_graph:
        adjacency_list.update({n: []})
    for n in b_graph:
        parent = n[:-1]
        if parent != '':
            nodes = adjacency_list.get(parent)
            nodes.append(n)
            adjacency_list.update({parent: nodes})
        print(adjacency_list)

    adjacency_list.update({'R': []})
    for i in b_graph:
        if len(i) == 1:
            root_nodes = adjacency_list.get('R')
            root_nodes.append(i)
            adjacency_list.update({'R': root_nodes})

    print(adjacency_list)
    print(b_graph)
    return adjacency_list


def draw_graph(adjacency_list):
    u = Digraph('unix')
    u.attr(size='6,6')
    u.node_attr.update(color='lightblue2', style='filled')

    g = nx.MultiDiGraph()
    g.add_nodes_from(adjacency_list.keys())
    for k, v in adjacency_list.items():
        for i in v:
            if k != i:
                u.edge(str(k), str(i))

    print(g)
    u.view()


input_data = open('./input-data/sql/m5.sql', 'r')
query_str = get_string(input_data)
sql_to_graph(query_str)

import re as reg
import string
import networkx as nx
from graphviz import Digraph

alphabet = list(string.ascii_uppercase)
keywords = ['union', 'minus', 'intersect', 'union_all']


result_tree = []
tree = []
part = []
graph = {'R': []}


class Part:
    def __init__(self, sql_query="", presence_of_brackets=False):
        self.sql_query = sql_query
        self.presence_of_brackets = presence_of_brackets

    def get_sql_query(self):
        return self.sql_query

    def get_presence_of_brackets(self):
        return self.presence_of_brackets

    def set_sql_query(self, sql_query):
        self.sql_query = sql_query

    def set_presence_of_brackets(self, presence_of_brackets):
        self.presence_of_brackets = presence_of_brackets


class Node:
    def __init__(self, name,body):
        self.name = name
        self.body = body

    def get_name(self):
        return self.name

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body

    def set_name(self, name):
        self.name = name


class BracketPosition:
    def __init__(self, left_position=None, right_position=None, left_char=None, right_char=None):
        self.left_position = left_position
        self.right_position = right_position
        self.left_char = left_char
        self.right_char = right_char

    def get_left_position(self):
        return self.left_position

    def get_right_position(self):
        return self.right_position

    def get_left_char(self):
        return self.left_char

    def get_right_char(self):
        return self.right_char

    def set_left_position(self, left_position):
        self.left_position = left_position

    def set_right_position(self, right_position):
        self.right_position = right_position

    def set_left_char(self, left_char):
        self.left_char  =left_char

    def set_right_char(self, right_char):
        self.right_char = right_char


def parents_separator():
    global tree, result_tree, part
    sql_str = ""
    num = 0
    for x in range(0, len(part)):
        if part[x].get_presence_of_brackets() is False:
            sql_str += part[x].get_sql_query()
        if part[x].get_presence_of_brackets() is True:
            sql_str += "chi_ldren" + str(num)
            num += 1

    # проверяем наличие ключевых слов, если еть такие то меняем родителя
    parser_string = '(.*)(union|intersect|union_all|minus)(.*)'
    sql_str = sql_str.replace("union all", "union_all")
    print(sql_str)
    if reg.match(parser_string, sql_str) is not None:
        res1 = reg.match(parser_string, sql_str).group(1)
        res2 = reg.match(parser_string, sql_str).group(3)

        num = 0
        repeat_child_index = 0
        repeat_child_index1 = 0
        flag = "chi_ldren"
        for x in range(0, len(part)):
            if part[x].get_presence_of_brackets() is True:
                if reg.match("(.*)chi_ldren(.*)", res1) is not None:
                    children_count = reg.findall(flag, res1)
                    repeat_child_index += len(children_count)
                    for i in range(0, len(children_count)):
                        if repeat_child_index > 1:
                            res1 = res1.replace("chi_ldren" + str(num), "(" + part[x].get_sql_query() + ")")
                        else:
                            res1 = res1.replace("chi_ldren" + str(num), part[x].get_sql_query())
                        num += 1
                else:
                    children_count = reg.findall(flag, res2)
                    repeat_child_index1 += len(children_count)
                    for i in range(0, len(children_count)):
                        if repeat_child_index1 > 1:
                            res2 = res2.replace("chi_ldren" + str(num), "(" + part[x].get_sql_query() + ")")
                        else:
                            res2 = res2.replace("chi_ldren" + str(num), part[x].get_sql_query())
                        num += 1

        tree.append(Node(tree[0].get_name() + "A", res2))
        tree.append(Node(tree[0].get_name() + "B", res1))
        temp_sql = "(" + tree[-2].get_name() + ") " + reg.match(parser_string, sql_str).group(2) + " (" + tree[-1].get_name() + ")"
        result_tree.append(Node(tree[0].get_name(), temp_sql))
    else:
        parent = ""
        parent_index = 0
        for x in range(0, len(part)):
            if part[x].get_presence_of_brackets():
                tree.append(Node(tree[0].get_name() + alphabet[parent_index], part[x].get_sql_query()))
                parent += " (" + tree[-1].get_name() + ") "
                parent_index += 1
            else:
                parent += part[x].get_sql_query()
        result_tree.append(Node(tree[0].get_name(), parent))
    tree.pop(0)


def parse(sql_string, CBP):
    global part
    part.clear()
    if sql_string != "":
        part.append(Part("", False))
        index = 0
        x = 0
        if len(CBP) == 0:
            part[-1].set_sql_query(sql_string)
        else:
            while x < len(sql_string):
                if index < len(CBP):
                    if x == CBP[index][0]:
                        x += 1
                        if part[-1].get_sql_query() == "" or part[-1].get_sql_query() == " " or part[-1].get_sql_query() == None:
                            part[-1].set_presence_of_brackets(True)
                        else:
                            part.append(Part("", True))
                    if x == CBP[index][1]:
                        x += 1
                        if x != len(sql_string) - 1:
                            part.append(Part("", False))
                        index += 1
                if x < len(sql_string):
                    temp_sql = part[-1].get_sql_query() + sql_string[x]
                    part[-1].set_sql_query(temp_sql)
                x += 1

    # Убираем лишнее
    for x in range(0, len(part)):
        match = reg.match("(.*)select(.*)", part[x].get_sql_query())
        if part[x].get_presence_of_brackets() is True and match is None:
            part[x].set_presence_of_brackets(False)
            part[x].set_sql_query("(" + part[x].get_sql_query() + ")")

    q = 0
    while q < len(part) - 1:
        if part[q].get_presence_of_brackets() is False and part[q + 1].get_presence_of_brackets() is False:
            temp_sql = part[q].get_sql_query() + part[q + 1].get_sql_query()
            part[q].set_sql_query(temp_sql)
            part.pop(q + 1)
            q = -1
        q += 1

    print(len(part))
    for i in part:
        print("\n*** " + str(i.get_presence_of_brackets()) + "    " + str(i.get_sql_query()))


def sql_to_graph(query_string):
    global tree, result_tree, part
    tree = []
    result_tree.clear()
    part.clear()

    tree.append(Node(alphabet[0], query_string))
    CBP = children_bracket_position(tree[0].get_body())
    parse(tree[0].get_body(), CBP)
    parents_separator()
    while len(tree) > 0:
        CBP = children_bracket_position(tree[0].get_body())
        parse(tree[0].get_body(), CBP)
        parents_separator()
    print("=============")
    for i in result_tree:
        print(i.get_name() + "\t" + i.get_body())

    doubles = True
    while doubles:
        doubles = remove_duplicates()

    print("\n=============")
    for i in result_tree:
        print(i.get_name() + "\t" + i.get_body())

    rename_nodes()

    build_graph()
    print("\n=============")
    print(graph)
    tree = tree_to_txt()
    return [tree, graph]


def rename_nodes():
    num = 1
    for x in result_tree:
        name = x.get_name()
        for y in result_tree:
            body = y.get_body()
            if body.find("(" + name + ")") != -1:
                new_body = body.replace("(" + name + ")", "(N"+str(num)+")")
                y.set_body(new_body)
        new_name = "N"+str(num)
        x.set_name(new_name)
        num += 1


def remove_duplicates():
    global parent, child, re, first, x, y
    first = ""
    re = False
    parent = ""
    child = ""
    x = 0
    tree_len = len(result_tree)
    while x < tree_len - 1:
        y = x + 1
        first = result_tree[x].get_body().replace(" ", "")
        while y < tree_len:
            seconde = result_tree[y].get_body().replace(" ", "")
            if first == seconde:
                re = True
                parent = "(" + result_tree[x].get_name() + ")"
                child = "(" + result_tree[y].get_name() + ")"
                result_tree.pop(y)
                tree_len = len(result_tree)
                for z in result_tree:
                    temp = z.get_body().replace(child, parent)
                    z.set_body(temp)
                break
            y += 1
        x += 1
    return re


def children_bracket_position(sql_string):
    global part
    part.clear()
    brackets = {')': '('}
    CBP = []
    inner_brackets_ind = []

    # Найдем позиции скобок
    brackets_positions = find_brackets_positions(sql_string, brackets)
    # Вывод позиций
    for bp in brackets_positions:
        CBP.append([bp.get_left_position(), bp.get_right_position()])

    # Найдем пары вложенных скобок
    if len(CBP) > 1:
        global x, y
        for x in range(len(CBP) - 1, 0, -1):
            for y in range(x-1, -1, -1):
                if CBP[y][0] > CBP[x][0] and CBP[y][1] < CBP[x][1]:
                    inner_brackets_ind.append(y)
                else:
                    x = y + 1
                    break
                if y == 0:
                    x = 0

    inner_brackets_ind = list(set(inner_brackets_ind))
    inner_brackets_ind.sort(reverse=True)

    # Удалим пары вложенных скобок
    for x in range(0, len(inner_brackets_ind)):
        index = inner_brackets_ind[x]
        CBP.pop(index)
    return CBP


def find_brackets_positions(sql_string, brackets):
    temp_stack = []
    stack = []
    try:
        for i in range(0, len(sql_string)):
            if sql_string[i] == '(':
                temp_stack.append(BracketPosition(left_position=i, left_char=sql_string[i]))

            elif sql_string[i] == ')':
                if len(temp_stack) > 0 and temp_stack[len(temp_stack) - 1].get_left_char() == '(':
                    bracket_position = temp_stack.pop()
                    bracket_position.set_right_char(sql_string[i])
                    bracket_position.set_right_position(i)
                    stack.append(bracket_position)
                else:
                    raise ValueError
    except ValueError:
        print("Ошибка в синтаксисе")
    return stack


def build_graph():
    global graph
    for x in result_tree:
        graph.update({x.get_name(): []})

    for x in result_tree:
        if len(x.get_name()) == 1:
            root_nodes = graph.get('R')
            root_nodes.append(x.get_name())
            graph.update({'R': root_nodes})

        words = x.get_body().split(" ")
        for w in words:
            if w.startswith('(') and w.endswith(')'):
                child_nodes = graph.get(x.get_name())
                if child_nodes.count(w[1:-1]) == 0:
                    child_nodes.append(w[1:-1])

    for x in result_tree:
        sql = x.get_body()
        sql = sql.replace(',', '')
        tables = []
        if sql.find('where') == -1:
            sub_str = sql[sql.find('from') + 4: len(sql)]
            tables.extend(sub_str.split(' '))
        else:
            sub_str = sql[sql.find('from') + 4: sql.find('where')]
            tables.extend(sub_str.split(' '))

        # Уберем пустые элементы
        tab = []
        for t in tables:
            if t != '':
                tab.append(t)

        # Избавимся от конструкций as
        global i
        i = len(tab) - 1
        while i > -1:
            if tab[i] == 'as':
                tab.pop(i + 1)
                tab.pop(i)
                tab.pop(i - 1)
                i -= 2
            i -= 1

        # Избавимся от узлов типа (...) и ключевых слов
        t_i = len(tab) - 1
        while t_i > -1:
            if tab[t_i].startswith('(') or tab[t_i].endswith(')') or keywords.count(tab[t_i]) != 0:
                tab.pop(t_i)
            t_i -= 1

        nodes = graph.get(x.get_name())
        nodes.extend(tab)
        graph.update({x.get_name(): nodes})


def draw_graph(adjacency_list):
    u = Digraph(format='pdf')
    g = nx.MultiDiGraph()

    g.add_nodes_from(adjacency_list.keys())

    #color_map = []

    for k, v in adjacency_list.items():
        for i in v:
            if k != i:
                u.edge(str(k), str(i))

    # for node in g:
    #     res = reg.match('N[0..9]*', node)
    #     if res is not None:
    #         u.get_node(node).attr['color'] = 'blue'
    #     else:
    #         u.get_node(node).attr['color'] = 'green'

    #nx.set_node_attributes(g, color_map, 'node_color')
    u.attr(size='6,6')
    u.node_attr.update(style='filled', color='lightblue2')

    u.render(format='pdf', filename='graph')
    u.render(format='png', filename='graph_cairo')
    u.render(format='svg', filename='graph_gd')


def tree_to_txt():
    string = ""
    for x in result_tree:
        string += x.get_name() + '\t' + x.get_body() + '\n'
    return string


# query = "select a4, b4, d4, a5, b5, e5, f5, s26.a3, s26.b3, s26.c3, s26.d3, s26.a2, s26.b2, s26.c2, s26.a1, s26.b1, s26.c1, s26.d1 from (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where a1 in (select a17 from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3)) and a1 in (select a17 from (select a3 as a17 from t3, t4 where d3=d4 and a3<=d3))), (select * from (select * from t4, t5 where a4=a5 and a5 in (select a5 from t5 where f5>=value) and a4 in (select a4 from t4 where a4<>b4)) where a5 not in (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2)))) where d4=d5) as s26, (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where (d1+c2)>=all((select max(d11) from (select avg(d1) as d11 from t1) union (select avg(c2) as d11 from t2)))) where a3 <=(select avg(a17)*2 as a18 from (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2))))) as s28 where s28.a3=s26.a3;"
# query1 = "select a4, b4, d4, a5, b5, e5, f5, s26.a3, s26.b3, s26.c3, s26.d3, s26.a2, s26.b2, s26.c2, s26.a1, s26.b1, s26.c1, s26.d1 from (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where a1 in (select a17 from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3)) and a1 in (select a17 from (select a3 as a17 from t3, t4 where d3=d4 and a3<=d3))), (select * from (select * from t4, t5 where a4=a5 and a5 in (select a5 from t5 where f5>=value) and a4 in (select a4 from t4 where a4<>b4)) where a5 not in (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2)))) where d4=d5) as s26, (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where (d1+c2)>=all((select max(d11) from (select avg(d1) as d11 from t1) union (select avg(c2) as d11 from t2)))) where a3 <=(select avg(a17)*2 as a18 from (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2))))) as s28 where s28.a3=s26.a3;"
# query2 = "SELECT * FROM (SELECT * FROM Table1 WHERE Field1 = Value1 UNION SELECT * FROM Table2 WHERE Field1 = Value2) union (select * from t2) AS t WHERE Field2 = Value3 "
# query3 = "SELECT * FROM (SELECT * FROM Table1 WHERE Field1 = Value1 UNION SELECT * FROM Table2 WHERE Field1 = Value2) AS t WHERE Field2 = Value3"
#query4 = "select a4, b4, d4, a5, b5, e5, f5, s26.a3, s26.b3, s26.c3, s26.d3, s26.a2, s26.b2, s26.c2, s26.a1, s26.b1, s26.c1, s26.d1 from (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where a1 in (select a17 from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3)) and a1 in (select a17 from (select a3 as a17 from t3, t4 where d3=d4 and a3<=d3))), (select * from (select * from t4, t5 where a4=a5 and a5 in (select a5 from t5 where f5>=value) and a4 in (select a4 from t4 where a4<>b4)) where a5 not in (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2)))) where d4=d5) as s26, (select * from (select * from (select * from (select * from t3, (select * from t2, (select * from t1 where c1 like ‘*a*’) where a1=a2 and c2>= (select min(d1) from t1)) where a1=a3) where a1 not in (select * from (select a1 as a13 from (select * from t1 where c1 like ‘*v*’), (select * from t3 where c3 like ‘*v*’) where a1=a3))) where (d1+c2)>=all(select max(d11) from (select avg(d1) as d11 from t1) union (select avg(c2) as d11 from t2))) where a3 <=(select avg(a17)*2 as a18 from (select a5 from (select * from t4, t5 where a4=a5 and a4 in (select a4 from t4 where d4>= (select avg(f5) from t5)) and a5 in (select a5 from t5 where value1 <=b5 and b5<= value2))))) as s28 where s28.a3=s26.a3;"
# children_bracket_position(query)
#
# # sql = 'select * from table2 where field1 = value2)'
# # a = reg.match('(.*)select(.*)', sql)
# # print(a)
#sql_to_graph(query4.lower())

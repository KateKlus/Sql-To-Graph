alphabet = ["A", "B", "C", "D", "E"]


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

    for x in range(0, len(select_list)):
        if (select_list[0] == " " or select_list[0] == "") and x == 0:
            pass
        else:
            result_list.append("select" + select_list[x])

    num_graph = []
    b_graph = [""] * len(result_list)
    maximum = 0
    for x in range(0, len(result_list)):
        count_open = ddd.count('(')
        count_close = ddd.count(')')
        num_graph.append(count_open - count_close)
        ddd += result_list[x]
        if (count_open - count_close) > maximum:
            maximum = count_open - count_close
    global index_graph
    index_graph = 0
    for y in range(0, maximum + 1):
        index_graph = 0
        global proverit
        proverit = False
        for x in range(0, len(result_list)):
            if num_graph[x] == 0 and proverit is True:
                index_graph += 1
            if num_graph[x] < 0:
                index_graph = 0
                proverit = False
            if num_graph[x] >= 0:
                b_graph[x] = (b_graph[x] + alphabet[index_graph])
                proverit = True
            num_graph[x] -= 1

    for x in range(0, len(result_list)):
        count_open = ddd.count('(')
        count_close = ddd.count(')')
        num_graph[x] = count_open - count_close
        ddd += "select " + result_list[x]
        if (count_open - count_close) > maximum:
            maximum = count_open - count_close

    for x in range(0, len(result_list)):
        graph += b_graph[x]
        graph += "\t"
        for y in range(0, num_graph[x]):
            graph += "\t"
        graph += result_list[x] + "\n"
    print(graph)


input_data = open('./input-data/sql/m5.sql', 'r')
query_str = get_string(input_data)
sql_to_graph(query_str)











from graph import draw_graph

# Глобальные переменные
graph = [('R', 'R')]
all_keywords = ['select', '*', 'from', 'where', '(', ')', 'and', 'join', 'order', 'by', 'group', '>', '<', '=', 'in']
global sub_queries_count
sub_queries_count = 0

# Открываем файл
input_data = open('./input-data/sql/m1.sql', 'r')


# Получаем строку из файла и подготавливаем
def get_string(string):
    for line in string:
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace(';', '')
        print(line)
        return line


# Получаем список ключевых слов запроса
def get_query_keywords(query_list):
    query_keywords = []
    for word in query_list.split(' '):
        if all_keywords.count(word) == 1:
            query_keywords.append(word)
    return query_keywords


# Получаем список таблиц запроса
def get_query_tables(query_string):
    from_i = query_string.find('from') + 5
    where_i = query_string.find('where') - 1
    order_i = query_string.find('order') - 1
    if where_i == -2:
        if order_i == -2:
            tables_string = query_string[from_i:]
        else:
            tables_string = query_string[from_i:order_i]
    else:
        tables_string = query_string[from_i:where_i]
    return tables_string.split(', ')


# Получаем список колонок
def get_query_col(query_string):
    select_i = query_string.find('select') + 7
    from_i = query_string.find('from') - 1
    tables_string = query_string[select_i:from_i]
    return tables_string.split(', ')


# Получаем список условий
def get_conditions_col(query_string, keywords):
    if keywords.count('where') >= 1:
        where_i = query_string.find('where') + 6
        conditions_string = query_string[where_i:]
        return conditions_string


# Анализируем строку запроса
def analysis(query, parent='R'):
    global sub_queries_count
    keywords_list = get_query_keywords(query)
    tables_list = get_query_tables(query)
    col_list = get_query_col(query)
    conditions_string = get_conditions_col(query, keywords_list)

    # Вывод отладочной информации
    print("Кллючевые слова: " + str(keywords_list))
    print("Таблицы: " + str(tables_list))
    print("Колонки: " + str(col_list))
    # print("Условия: " + str(conditions_list))

    if keywords_list.count('in') >= 1:
        in_start = conditions_string.find('(') + 2
        in_end = conditions_string.find(')') + 1
        in_conditions = conditions_string[in_start: in_end]
        if in_conditions.split(' ').count('select') >= 1:
            sub_query = conditions_string[in_start: in_end]
            new_query = query[:query.find('where')] + query[query.rfind(')') + 1:]
            node_name = analysis(new_query, parent)
            analysis(sub_query, node_name)

    # Если простой запрс с одним select
    if keywords_list.count('select') == 1:
        sub_queries_count += 1
        node_name = 's' + str(sub_queries_count)
        graph.append((node_name, parent))
        for table in tables_list:
            graph.append((node_name, table))
        print(node_name + ' = ' + query)
        return node_name


# Точка входа
query_str = get_string(input_data)
analysis(query_str)

# Вывод графа инормационных зависимостей
draw_graph(graph)

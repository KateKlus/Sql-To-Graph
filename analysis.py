import gc

# Глобальные переменные
graph = [('R', 'R')]
all_keywords = ['select', '*', 'from', 'where', '(', ')', 'and', 'join', 'order', 'by', 'group', '>', '<', '=', 'in']
sub_queries_count = 0


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


def find_sub_queries_from(query_string, tables_list=[]):
    if query_string.find('(') != -1:
        sub_q_start = query_string.find('(')
        sub_q_end = query_string.find(')') + 1
        sub_query = query_string[sub_q_start: sub_q_end]
        if tables_list.count(sub_query) == 0:
            tables_list.append(sub_query)
        query_string = query_string.replace(sub_query, '')
        find_sub_queries_from(query_string, tables_list)
    return tables_list


# Получаем список таблиц запроса
def get_query_tables(query_string):
    tables_list = []
    from_i = query_string.find('from') + 5
    where_i = query_string.find('where') - 1
    order_i = query_string.find('order') - 1
    if query_string[from_i:where_i].find('(') != -1:
        tables_list = find_sub_queries_from(query_string[from_i:], [])
        for table in tables_list:
            query_string = query_string.replace(table, '')
    where_i = query_string.find('where') - 1
    if where_i == -2:
        if order_i == -2:
            tables_string = query_string[from_i:]
        else:
            tables_string = query_string[from_i:order_i]
    else:
        tables_string = query_string[from_i:where_i]
    tables = tables_string.strip().split(', ')
    tables_list = tables_list + tables
    return tables_list


# Получаем список колонок
def get_query_col(query_string):
    select_i = query_string.find('select') + 7
    from_i = query_string.find('from') - 1
    tables_string = query_string[select_i:from_i]
    return tables_string.split(', ')


# Получаем список условий
def get_conditions_col(query_string, keywords):
    if keywords.count('where') > 0:
        from_i = query_string.find('from') + 5
        where_i = query_string.find('where') - 1
        if query_string[from_i:where_i].find('(') != -1:
            start_i = query_string[from_i:].find(')') + 1
            sub_str = query_string[from_i + start_i:]
            new_where_i = sub_str.find('where') + 6
            conditions_string = sub_str[new_where_i:]
            return conditions_string
        conditions_string = query_string[where_i:]
        return conditions_string


# Анализируем строку запроса
def analysis(query, logging, parent='R'):
    global sub_queries_count
    keywords_list = get_query_keywords(query)
    tables_list = get_query_tables(query)
    col_list = get_query_col(query)
    conditions_string = get_conditions_col(query, keywords_list)

    # Вывод отладочной информации
    if logging:
        print('--------------------------------------')
        print('Запрос: ' + str(query))
        print('Ключевые слова: ' + str(keywords_list))
        print('Таблицы: ' + str(tables_list))
        print('Колонки: ' + str(col_list))
        print("Условия: " + str(conditions_string) + '\n')

    for table in tables_list:
        # Анализируем ключевое слово in
        if keywords_list.count('in') >= 1:
            in_start = conditions_string.find('(') + 2
            in_end = conditions_string.rfind(')')
            in_conditions = conditions_string[in_start: in_end]
            if in_conditions.split(' ').count('select') >= 1:
                sub_query = conditions_string[in_start: in_end]
                from_i = query.find('from') + 5
                where_i = query.find('where') - 1
                if query[from_i:where_i].find('(') != -1:
                    start_i = query[from_i:].find(')') + 1
                    sub_str = query[from_i + start_i:]
                    new_where_i = sub_str.find('where') + from_i + start_i
                    new_query = query[:new_where_i] + query[query.rfind(')') + 1:]
                    tables_list.remove(table)
                    node_name = analysis(new_query, logging, parent)
                else:
                    new_query = query[:query.find('where')] + query[query.rfind(')') + 1:]
                    tables_list.remove(table)
                    node_name = analysis(new_query, logging, parent)
                keywords_list.remove('in')
                analysis(sub_query, logging, node_name)
        elif table.find('select') != -1:
            new_query = query.replace(table, '').replace('  ', ' ')
            tables_list.remove(table)
            node_name = analysis(new_query, logging, parent)
            analysis(table.replace('(', '').replace(')', '').replace('  ', ' '), logging, node_name)

    # Если простой запрс с одним select
    if keywords_list.count('select') == 1:
        sub_queries_count += 1
        node_name = 's' + str(sub_queries_count)
        graph.append((node_name, parent))
        for table in tables_list:
            graph.append((node_name, table))
        if logging:
            print(node_name + ' = ' + query + '\n')
        return node_name
    return 's' + str(sub_queries_count-1)


# Точка входа
def run_analysis(query_string, logging):
    analysis(query_string, logging)
    return graph


# Очистка переменных
def clean_tree():
    gc.collect()
    global graph, sub_queries_count
    graph = [('R', 'R')]
    sub_queries_count = 0

from graph import draw_graph

keywords = ['select', '*', 'from', 'where', '(', ')', 'and', 'join', 'order', 'by', 'group', '>', '<', '=']

input_data = open('./input-data/simple_sql/1.sql', 'r')


def get_string(string):
    for line in string:
        return line


def get_query_keywords(query_list):
    query_keywords = []
    for word in query_list.split(' '):
        if keywords.count(word) == 1:
            query_keywords.append(word)
    return query_keywords


def get_query_tables(query_string):
    from_i = query_string.find('from') + 5
    where_i = query_string.find('where') - 1
    tables_string = query_string[from_i:where_i]
    return tables_string.split(', ')


def get_query_col(query_string):
    select_i = query_string.find('select') + 7
    from_i = query_string.find('from') - 1
    tables_string = query_string[select_i:from_i]
    return tables_string.split(', ')


def get_conditions_col(query_string, keywords):
    if keywords.count('order') == 1:
        where_i = query_string.find('where') + 6
        order_i = query_string.find('order') - 1
        conditions_string = query_string[where_i:order_i]
        if keywords.count('and') >= 1:
            return conditions_string.split(' and ')
        else:
            return [conditions_string]


query = get_string(input_data)

query_keywords_list = get_query_keywords(query)
query_tables_list = get_query_tables(query)
get_query_col_list = get_query_col(query)
get_conditions_col_list = get_conditions_col(query, query_keywords_list)

print(query_keywords_list)
print(query_tables_list)
print(get_query_col_list)
print(get_conditions_col_list)

graph = [('t1', 'w1'), ('t2', 'w1'), ('w1', 'w2'), ('t3', 'w2'), ('w2', 'w3')]

draw_graph(graph)

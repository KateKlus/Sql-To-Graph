import gc
from graph_class import Graph
from graph import draw_graph


sub_queries_count = 0
all_keywords = ['select', 'from', 'where', '(', ')', 'and', 'join', 'inner', 'outer', 'left', 'right', 'distinct',
                'unique', 'all', 'cross', 'natural', 'full', 'using', 'having', 'on', 'union', 'intersect', 'minus',
                'order', 'by', 'group', '>', '<', '=', 'in', 'asc', 'desc', 'nulls', 'first', 'last']


class Subquery:
    def print_info(self):
        print('--------------------------------------')
        print('Узел: ' + self.node_name)
        print('Запрос: ' + self.full_str)
        print('Ключевые слова: ' + str(self.keywords))
        print('Таблицы: ' + str(self.tables))
        print('Колонки: ' + str(self.columns))
        print("Условия: " + str(self.conditions) + '\n')

    # Определяем уровень вложенности скобок
    def get_brackets_levels(self):
        current_level = 0
        current_position = 0
        brackets_levels = {}
        query = self.full_str
        for word in query:
            current_position += 1
            if word == '(':
                current_level += 1
                if brackets_levels.get(current_level) is None:
                    brackets_levels.update({current_level: [current_position, 0]})
                else:
                    current_level += 1
                    brackets_levels.update({current_level: [current_position, 0]})
            if word == ')':
                bracket_indexes = brackets_levels.get(current_level)
                new_indexes = [bracket_indexes[0], current_position]
                brackets_levels.update({current_level: new_indexes})
                current_level -= 1

        return brackets_levels

    # Получаем список колонок
    def get_columns(self):
        select_i = self.full_str.find('select') + 7
        from_i = self.full_str.find('from') - 1
        tables_string = self.full_str[select_i:from_i]
        return tables_string.strip().split(',')

    # Содержат ли "условия" подзапросы
    def analyse_conditions(self):
        conditions = self.conditions
        brackets_levels = self.brackets_levels
        query_string = self.full_str
        global sub_queries_count
        if conditions.split(' ').count('select') >= 1:
            abs_start_i = query_string.find(conditions)
            start_i = conditions.find('(') + abs_start_i + 1
            for level in brackets_levels:
                i = brackets_levels.get(level)
                if start_i == i[0]:
                    end_i = i[1] - 1
                    sub_query_str = query_string[start_i:end_i].strip()
                    sub_queries_count += 1
                    self.conditions = conditions.replace('( ' + sub_query_str + ' )', 's' + str(sub_queries_count))
                    sub_query = Subquery(sub_query_str, 's' + str(sub_queries_count), self.node_name)
                    graph.add_node(sub_query.node_name, sub_query.parent_node, sub_query.tables)

    # Получаем список условий
    def get_conditions(self):
        keywords = self.keywords
        query_string = self.full_str
        if keywords.count('where') > 0:
            i = query_string.find('where')
        elif keywords.count('group') > 0:
            i = query_string.find('group')
        elif keywords.count('order') > 0:
            i = query_string.find('order')
        elif keywords.count('union') > 0:
            i = query_string.find('union')
        elif keywords.count('intersect') > 0:
            i = query_string.find('intersect')
        elif keywords.count('minus') > 0:
            i = query_string.find('minus')
        else:
            i = -1

        conditions_string = query_string[i:]
        return conditions_string

    # Получаем список ключевых слов запроса
    def get_keywords(self):
        query_keywords = []
        for word in self.full_str.split(' '):
            if all_keywords.count(word) == 1:
                query_keywords.append(word)
        return query_keywords

    # Получаем список таблиц запроса
    def get_tables(self):
        global tables_list
        global sub_queries_count
        tables_list = []
        keywords = self.keywords
        query_string = self.full_str
        brackets_levels = self.brackets_levels

        if keywords.count('where') > 0:
            i = query_string.find('where')
        elif keywords.count('group') > 0:
            i = query_string.find('group')
        elif keywords.count('order') > 0:
            i = query_string.find('order')
        elif keywords.count('union') > 0:
            i = query_string.find('union')
        elif keywords.count('intersect') > 0:
            i = query_string.find('intersect')
        elif keywords.count('minus') > 0:
            i = query_string.find('minus')
        else:
            i = len(query_string)

        from_i = query_string.find('from') + 5
        tables_string = query_string[from_i: i]
        # Содержат ли "таблицы" подзапросы
        # TODO with as select
        if tables_string.find('select') != -1:
            start_i = query_string.find('(') + 1
            for level in brackets_levels:
                i = brackets_levels.get(level)
                if start_i == i[0]:
                    end_i = i[1] - 1
                    sub_query_str = query_string[start_i:end_i].strip()
                    sub_queries_count += 1
                    new_query = Subquery(query_string.replace('( ' + sub_query_str + ' )', 's' + str(sub_queries_count)),
                                         's' + str(sub_queries_count), self.node_name)
                    graph.add_node(new_query.node_name, new_query.parent_node, new_query.tables)

                    sub_queries_count += 1
                    sub_query = Subquery(sub_query_str, 's' + str(sub_queries_count), new_query.node_name)
                    graph.add_node(sub_query.node_name, sub_query.parent_node, sub_query.tables)

        else:
            tables_list = tables_string.strip().split(', ')
        return tables_list

    def __init__(self, full_str, node_name, parent_node):
        self.full_str = full_str
        self.node_name = node_name
        self.parent_node = parent_node
        self.keywords = self.get_keywords()
        if self.keywords.count('(') > 0:
            self.brackets_levels = self.get_brackets_levels()
        else:
            self.brackets_levels = {}
        self.tables = self.get_tables()
        self.conditions = self.get_conditions()
        self.columns = self.get_columns()
        self.analyse_conditions()
        self.print_info()


# Получаем строку из файла и подготавливаем
def get_string(string):
    for line in string:
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace(';', '')
        print(line)
        return line


# Очистка переменных
def clean_tree():
    gc.collect()
    global graph, sub_queries_count
    graph = [('R', 'R')]
    sub_queries_count = 0


# Открываем файл
input_data = open('./input-data/sql/m3.sql', 'r')
# Получаем строку запроса
query_str = get_string(input_data)
# Инициируем граф
graph = Graph()
# Запускаем анализ
new_query = Subquery(query_str, 'R', 'R')

# Выводим граф инормационных зависимостей
draw_graph(graph.graph)
print(graph.graph)

# Очищаем переменные
clean_tree()


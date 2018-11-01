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

    def print_pre_info(self):
        print('--------------------------------------')
        print('Узел: ' + self.node_name)
        print('Запрос: ' + self.full_str)
        print('Ключевые слова: ' + str(self.keywords))

    # Переопределяем строку запроса после замены подзапросов их именами
    def set_new_full_str(self, new_str):
        self.full_str = new_str
        self.keywords = self.get_keywords()
        self.print_pre_info()
        if self.keywords.count('(') > 0:
            self.brackets_levels = self.get_brackets_levels()
        else:
            self.brackets_levels = {}
        self.tables = self.get_tables()
        self.conditions = self.get_conditions()
        self.columns = self.get_columns()

    # Определяем уровень вложенности скобок
    def get_brackets_levels(self):
        current_level = 0
        previous_levels = []
        current_position = 0
        brackets_levels = {}
        query = self.full_str
        for symbol in query:
            current_position += 1
            if symbol == '(':
                current_level += 10
                if brackets_levels.get(current_level) is None:
                    brackets_levels.update({current_level: [current_position, 0]})
                    previous_levels.append(current_level)
                else:
                    current_level += 1
                    previous_levels.append(current_level)
                    brackets_levels.update({current_level: [current_position, 0]})
            if symbol == ')':
                if brackets_levels.get(current_level)[1] == 0:
                    bracket_indexes = brackets_levels.get(current_level)
                    new_indexes = [bracket_indexes[0], current_position]
                    brackets_levels.update({current_level: new_indexes})
                else:
                    if current_level % 10 != 0:
                        current_level -= current_level % 10
                    else:
                        current_level -= 10
                    bracket_indexes = brackets_levels.get(current_level)
                    new_indexes = [bracket_indexes[0], current_position]
                    brackets_levels.update({current_level: new_indexes})
                previous_levels.reverse()
                for level in previous_levels:
                    if brackets_levels.get(level)[1] == 0:
                        current_level = level
                previous_levels.reverse()
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
        if conditions.split(' ').count('select') >= 1:
            abs_start_i = query_string.find(conditions)
            start_i = conditions.find('(') + abs_start_i + 1
            for level in brackets_levels:
                i = brackets_levels.get(level)
                if start_i == i[0]:
                    end_i = i[1] - 1
                    sub_query_str = query_string[start_i:end_i].strip()
                    self.sub_queries_count += 1
                    self.conditions = conditions.replace('( ' + sub_query_str + ' )', 's' + str(self.sub_queries_count))
                    self.full_str = query_string.replace('( ' + sub_query_str + ' )', 's' + str(self.sub_queries_count))
                    Subquery(sub_query_str, 's' + str(self.sub_queries_count), self.node_name, self.graph,
                             self.sub_queries_count)

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
                    self.sub_queries_count += 1
                    self.set_new_full_str(query_string.replace('( ' + sub_query_str + ' )',
                                                               's' + str(self.sub_queries_count)))
                    Subquery(sub_query_str, 's' + str(self.sub_queries_count), self.node_name, self.graph,
                             self.sub_queries_count)
                    return self.tables
        else:
            tables_list = tables_string.strip().split(', ')
            return tables_list

    def check_for_union(self):
        query_string = self.full_str
        if self.keywords.count('union') > 0:
            start_i = query_string.find('union') + 5
            sub_query_str_left = query_string[start_i:].strip()
            sub_query_str_right = query_string[:start_i - 5].strip()
            new_query_str = ' union '
            if sub_query_str_right.count('select') > 0:
                new_query_str = 's' + str(self.sub_queries_count + 1) + new_query_str
                self.sub_queries_count += 1
                Subquery(sub_query_str_right, 's' + str(self.sub_queries_count), self.node_name, self.graph,
                         self.sub_queries_count)
            else:
                new_query_str = sub_query_str_right + ' union '
            if sub_query_str_left.count('select') > 0:
                new_query_str = new_query_str + 's' + str(self.sub_queries_count + 1)
                self.sub_queries_count += 1
                Subquery(sub_query_str_left, 's' + str(self.sub_queries_count), self.node_name, self.graph,
                         self.sub_queries_count)
            else:
                new_query_str = ' union ' + sub_query_str_left
            self.set_new_full_str(new_query_str)

    def __init__(self, full_str, node_name, parent_node, graph, sub_queries_count=1):
        self.sub_queries_count = sub_queries_count
        self.graph = graph
        self.full_str = full_str
        self.node_name = node_name
        self.parent_node = parent_node
        self.keywords = self.get_keywords()
        self.print_pre_info()
        if self.keywords.count('(') > 0:
            self.brackets_levels = self.get_brackets_levels()
        else:
            self.brackets_levels = {}
        self.tables = self.get_tables()
        self.conditions = self.get_conditions()
        self.columns = self.get_columns()
        self.check_for_union()
        self.analyse_conditions()
        self.print_info()
        graph.add_node(self.node_name, self.parent_node, self.tables)

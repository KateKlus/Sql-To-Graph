from graph_class import Graph
from graph import draw_graph
from subquery_class import Subquery


# Получаем строку из файла и подготавливаем
def get_string(string):
    for line in string:
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace('  ', ' ').replace(';', '')
        print(line)
        return line


# Открываем файл
input_data = open('./input-data/sql/m4.sql', 'r')
# Получаем строку запроса
query_str = get_string(input_data)
# Инициируем граф
graph = Graph()
# Запускаем анализ
new_query = Subquery(query_str, 's1', 'R', graph)

# Выводим граф инормационных зависимостей
draw_graph(graph.graph)
print(graph.graph)

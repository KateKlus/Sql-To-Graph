from analysis import run_analysis, get_string, clean_tree
from graph import draw_graph

# Открываем файл
input_data = open('./input-data/sql/m4.sql', 'r')

query_str = get_string(input_data)
graph = run_analysis(query_str, True)

# Выводим граф инормационных зависимостей
draw_graph(graph)
print(graph)

# Очищаем переменные
clean_tree()

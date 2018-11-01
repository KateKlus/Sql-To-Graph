from subquery_class import Subquery
from graph_class import Graph


sql = open('./done_sql.sql', 'r')
graphs_expect = open('./done_graph.txt', 'r')
graphs_actual = open('./actual_graphs.txt', 'a')
count = 0


# Запускаем прогон тестов
def run_tests():
    for line in sql:
        global count
        count += 1
        print("Обработка выражения №" + str(count))
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace(';', '')
        graph = Graph()
        Subquery(line, 's1', 'R', graph)
        graphs_actual.write(str(graph.get_node_list()) + '\n')


# Очищаем файл выводы
def clean_output_file():
    graphs = open('./actual_graphs.txt', 'w')
    graphs.write('')
    graphs.close()


# Сравниваем результат прогона с ожидаемым результатом
def compare_results():
    global count
    t1 = graphs_expect.read().splitlines()
    t2 = open('./actual_graphs.txt').read().splitlines()

    for i in range(0, count-1):
        str1 = t1.pop(0)
        str2 = t2.pop(0)
        if str1 == str2:
            print("Success")
        else:
            print("Failed")
            print(str1 + '\n' + str2)


# Запускаем тестирование
clean_output_file()
run_tests()
graphs_actual.close()
compare_results()

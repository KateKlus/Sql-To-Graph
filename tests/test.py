from analysis import run_analysis, clean_tree
from difflib import ndiff

sql = open('./done_sql.sql', 'r')
graphs_expect = open('./done_graph.txt', 'r')
graphs_actual = open('./actual_graphs.txt', 'a')
count = 0


def run_tests():
    for line in sql:
        global count
        count += 1
        print("Обработка выражения №" + str(count))
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace(';', '')
        actual_graph = run_analysis(line, True)
        graphs_actual.write(str(actual_graph) + '\n')
        clean_tree()


def clean_output_file():
    graphs = open('./actual_graphs.txt', 'w')
    graphs.write('')
    graphs.close()


def compare_results():
    global count
    t1 = graphs_expect.read().splitlines()
    t2 = open('./actual_graphs.txt').read().splitlines()
    if t1 == t2:
        print("Success")
        print("Total count: " + str(count))
    else:
        print("Failed")
        print(''.join(ndiff(t1, t2)))


clean_output_file()
run_tests()
graphs_actual.close()
compare_results()

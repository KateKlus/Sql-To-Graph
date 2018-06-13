from analysis import run_analysis, clean_tree


sql = open('./done_sql.sql', 'r')
graphs_expect = open('./done_graph.txt', 'r')
graphs_actual = open('./actual_graphs.txt', 'a')


def run_tests():
    for line in sql:
        line = line.strip().replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace(';', '')
        actual_graph = run_analysis(line)
        graphs_actual.write(str(actual_graph) + '\n')
        clean_tree()


def clean_output_file():
    graphs_actual = open('./actual_graphs.txt', 'w')
    graphs_actual.write('')
    graphs_actual.close()


clean_output_file()
run_tests()

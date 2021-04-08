import timeit
from functools import partial

import matplotlib.pyplot as plt

from cpatminer.ast_tree import AstTree, calculate_run_time, AnalysisNodeVisitor, run_first_experiment, run_second_experiment
from cpatminer.utils import create_data_directory, read_python_files, read_csv_file, calculate_node_numbers


if __name__ == '__main__':

    first_experiment_run_time = []
    second_experiment_run_time = []
    number_of_nodes = []
    number_of_nodes1 = []
    trees = []
    # files = [
    # ]
    repo_list = read_csv_file('repo_list.csv')
    create_data_directory(repo_list)
    files = read_python_files()
    for file_name in files:
        ast_tree = AstTree()
        ast_tree.read_file(file_name)
        trees.append(ast_tree)

    for i in range(5, len(trees), 5):
        batch_of_trees = trees[:i]
        number_of_nodes.append(calculate_node_numbers(batch_of_trees))
        first_experiment_run_time.append(
            timeit.timeit(
                partial(run_first_experiment, batch_of_trees),
                number=10)
        )
    assert 1 == 1

    for j in range(5, len(trees), 5):
        batch_of_trees = trees[:j]
        second_experiment_run_time.append(timeit.timeit(
                partial(run_second_experiment, batch_of_trees),
                number=10)
        )
    plt.plot(number_of_nodes, first_experiment_run_time, lw=2, color='red',
             label='Original Algorithm')
    plt.plot(number_of_nodes, second_experiment_run_time, lw=2, color='blue',
             label='Proposed algorithm')
    plt.title('Comparing the original implementation with the proposed algorithm')
    plt.xlabel('Number of nodes')
    plt.ylabel('Running time')

    plt.legend()
    plt.show()
    assert 1 == 1



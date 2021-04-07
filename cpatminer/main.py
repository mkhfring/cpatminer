import os
from functools import partial

from cpatminer.ast_tree import AstTree, calculate_run_time, AnalysisNodeVisitor
from cpatminer.utils import create_data_directory, read_python_files, read_csv_file, topological_sort

trees = []
# files = [
#     os.path.join('data', file_name) for file_name in os.listdir('data/')
# ]
repo_list = read_csv_file('repo_list.csv')
create_data_directory(repo_list)
files = read_python_files()
for file_name in files:
    ast_tree = AstTree()
    ast_tree.read_file(file_name)
    trees.append(ast_tree)

test_tree = trees[0]
tree = AnalysisNodeVisitor(test_tree)
tree_call = partial(tree.generic_visit, test_tree.parsed_code)
tree_call()
topological_sort(tree)
for node in tree.tree.nodes:
    if hasattr(node, 'max_level'):
        print(node.max_level)
for tree in trees:
    calculate_run_time(tree, 100)


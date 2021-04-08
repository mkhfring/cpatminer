import os
import csv
import queue
from functools import partial

import git

from cpatminer.ast_tree import AnalysisNodeVisitor


def create_data_directory(repo_list):
    dir_name = 'data'
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        for repo in repo_list:
            try:
                git.Git('data').clone(repo)
            except Exception as e:
                pass
    else:
        os.makedirs(dir_name)
        for repo in repo_list:
            git.Git('data').clone(repo)


def read_csv_file(filename):
    repo_list_result = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            repo_list_result.append(row)

    return repo_list_result[0]


def read_python_files():
    python_file_list = []
    for root, dirs, files in os.walk("data"):

        for file in files:
            if file.endswith(".py") and not '__init__' in file and not 'setup' in file:
                python_file_list.append(os.path.join(root, file))

    return python_file_list


def calculate_node_numbers(tree_list):
    number_of_nodes = 0
    for ast_tree in tree_list:
        tree = AnalysisNodeVisitor(ast_tree)
        tree_call = partial(tree.generic_visit, ast_tree.parsed_code)
        tree_call()
        number_of_nodes += len(tree.tree.nodes)

    return number_of_nodes


def topological_sort(tree):
    tree = tree.tree
    for node in tree.nodes:
        node.max_level = -1

    rank_queue = queue.Queue()
    for node in tree.nodes:
        max_level = 0
        if hasattr(node, 'marked'):
            continue
        root = node
        root.level = 0
        rank_queue.put(root)
        root.marked = True
        while not rank_queue.empty():
            current_node = rank_queue.get()
            if not hasattr(current_node, 'children'):
                break
            for child in current_node.children:
                if not hasattr(child, 'marked'):
                    rank_queue.put(child)
                    child.level = current_node.level + 1
                    if child.level > max_level:
                        max_level = child.level
                    child.marked = True

        node.max_level = max_level

    return tree


if __name__ == "__main__":
    repo_list = read_csv_file('repo_list.csv')
    create_data_directory(repo_list)
    read_python_files()

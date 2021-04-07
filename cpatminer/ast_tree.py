import ast
from collections import defaultdict
from datetime import datetime
from functools import partial
import os
import timeit


class Node:
    def __init__(self, node):
        self.node = node
        self.name = None
        self.childs = []

class AstTree:

    def __init__(self):
        self.nodes = []
        self.file_name = None

    def read_file(self, file_name):
        self.file_name = file_name
        with open(file_name) as source:
            self.parsed_code = ast.parse(source.read())
            assert 1 == 1


class NodeVisitor(ast.NodeVisitor):
    def visit_Str(self, tree_node, mode=1):
        print('{}'.format(tree_node.s))


class AnalysisNodeVisitor(ast.NodeTransformer):

    def __init__(self, tree):
        self.tree = tree
        self.unique_id = 1


    def visit_Assign(self, node):
        node.node_type = 'assign'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Assign and fields: ', node._fields)

    def visit_Compare(self, node):
        node.node_type = 'compare'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Assign and fields: ', node._fields)

    def visit_BinOp(self, node):
        node.node_type = 'bin_op'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: BinOp and fields: ', node._fields)

    def visit_Expr(self, node):
        node.node_type = 'expression'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Expr and fields: ', node._fields)

    def visit_Num(self,node):
        node.node_type = 'number'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Num and fields: ', node._fields)

    def visit_Name(self, node):
        node.node_type = 'name'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Name and fields: ', node._fields)

    def visit_Str(self, node):
        node.node_type = 'string'
        node.name = type(node).__name__
        self._analyse_node(node)
#        print('Node type: Str and fields: ', node._fields)

    def visit_If(self, node):
        node.node_type = 'if_control'
        node.name = type(node).__name__
        self._analyse_node(node)
        assert 1 == 1

    def visit_While(self, node):
        node.node_type = 'while'
        node.name = type(node).__name__
        self._analyse_node(node)
        assert 1 == 1

    def visit_For(self, node):
        node.node_type = 'for'
        node.name = type(node).__name__
        self._analyse_node(node)
        assert 1 == 1


    def visit_Call(self,node):
        node.node_type = 'call'
        node.name = type(node).__name__
        self._analyse_node(node)
        """ visit a Call node """
#        print(type(node).__name__)

    def visit_Lambda(self,node):
        node.node_type = 'function'
        node.name = type(node).__name__
        self._analyse_node(node)
        """ visit a Function node """
#        print(type(node).__name__)

    def visit_FunctionDef(self,node):
        node.node_type = 'function_def'
        node.name = type(node).__name__
        self._analyse_node(node)

    def _analyse_node(self, node):
        self.tree.nodes.append(node)
        self.creat_node_tree_recursive(node)

        # if hasattr(node, 'childern'):
        #     ast.NodeTransformer.generic_visit(self, node)
        # else:
        #     node.children = []

        # for child in ast.iter_child_nodes(node):
        #     child.name = type(node).__name__
        #     node.children.append(child)
        ast.NodeTransformer.generic_visit(self, node)

    def creat_node_tree_recursive(self, node):
        children = [node for node in ast.iter_child_nodes(node)]
        if len(children) == 0:
            return
        else:
            node.children = children
            for child in children:
                self.creat_node_tree_recursive(child)


class AstGraphGenerator(object):

    def __init__(self, source):
        self.graph = defaultdict(lambda: [])
        self.source = source  # lines of the source code

    def __str__(self):
        return str(self.graph)

    def _getid(self, node):
        try:
            lineno = node.lineno - 1
            return "%s: %s" % (type(node), self.source[lineno].strip())

        except AttributeError:
            return type(node)

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)

            elif isinstance(value, ast.AST):
                node_source = self._getid(node)
                value_source = self._getid(value)
                self.graph[node_source].append(value_source)
                self.visit(value)


def create_tree_bfs(ast_tree):
    for node in ast.walk(ast_tree.parsed_code):
        current_node = Node(node)
        current_node.name = node.__class__.__name__
        print("_____" + str(current_node.name))
        for child in ast.iter_child_nodes(node):
            current_child = Node(child)
            current_child.name = current_child.__class__.__name__
            current_node.childs.append(current_child)
            child.parent = current_node

        ast_tree.nodes.append(current_node)


def calculate_run_time(ast_tree, number_of_execution=1):
    tree = AnalysisNodeVisitor(ast_tree)
    tree_call = partial(tree.generic_visit, ast_tree.parsed_code)
    tree_call()
    print(
        ast_tree.file_name,
        "Runnig time: " + str(
        timeit.timeit(
        tree_call,
        number=100)
        ),
        f"|||| number of nodes: {len(tree.tree.nodes)}"
    )
    assert 1 == 1


if __name__ == "__main__":

    trees = []
    files = [
        os.path.join('data', file_name) for file_name in os.listdir('data/')
    ]
    for file_name in files:
        ast_tree = AstTree()
        ast_tree.read_file(file_name)
        trees.append(ast_tree)

    for tree in trees:
        calculate_run_time(tree, 100)


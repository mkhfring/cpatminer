import ast
import astor
from collections import defaultdict


class ASTParser:
    def __init__(self):
        pass

    def read_file(self, file_name):
        with open(file_name) as source:
            self.tree = ast.parse(source.read())

#class AnalysisNodeVisitor(ast.NodeVisitor):
#
#    def visit_Import(self,node):
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_ImportFrom(self,node):
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_Assign(self,node):
#        from pudb import set_trace; set_trace()
#        print('Node type: Assign and fields: ', node._fields)
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_BinOp(self, node):
#        print('Node type: BinOp and fields: ', node._fields)
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_Expr(self, node):
#        print('Node type: Expr and fields: ', node._fields)
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_Num(self,node):
#        print('Node type: Num and fields: ', node._fields)
#
#    def visit_Name(self,node):
#        print('Node type: Name and fields: ', node._fields)
#        ast.NodeVisitor.generic_visit(self, node)
#
#    def visit_Str(self, node):
#        print('Node type: Str and fields: ', node._fields)
#
#from collections import deque
#
#def walk(node):
#    queue = deque([node])
#    while queue:
#        node = queue.popleft()
#        if isinstance(node, tuple):
#            queue.extend(node[1:])  # add the children to the queue
#        yield node
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
                # self.graph[type(node)].append(type(value))
                self.visit(value)


if __name__ == "__main__":
    parser = ASTParser()
    parser.read_file("example.py")
    graph = AstGraphGenerator(parser.tree)
    for node in parser.tree.body:
        graph.visit(node)
        assert 1==1

#    visitor = AnalysisNodeVisitor().visit_Assign(parser.tree)
    print(ast.dump(parser.tree))

    assert 1 == 1




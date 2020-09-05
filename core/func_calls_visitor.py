import ast
from collections import deque
from ast import NodeVisitor
'''
visit keyword arguments
'''
class KWVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = []

    @property
    def name(self):
        return ",".join(self._name)

    def visit_keyword(self, node):
        if node.arg is not None:
            self._name.append(node.arg)

'''
visit function call nodes
'''
class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()
    @property
    def name(self):
        return ".".join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)
    # handle attrinutes of a function calls
    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)

def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_visitor = FuncCallVisitor()
            call_visitor.visit(node.func)
            kw_visitor = KWVisitor()
            try:
                kw_visitor.visit(node)
                func_calls += [(call_visitor.name, kw_visitor.name)]
            except:
                func_calls += [(call_visitor.name, "")]  # no keyword arguments found
    return func_calls

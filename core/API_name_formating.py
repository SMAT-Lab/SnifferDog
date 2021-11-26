import os
import sys
import json
import ast
from multiprocessing import Pool
from .util import get_path_by_extension
from .func_calls_visitor import get_func_calls

# visit assignment statements
class AssignVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_obj = {}
    def visit_Assign(self, node):
        call_name = get_func_calls(node.value)
        # for an assignment and its right side has a function call
        # map this function call to its left
        if len(call_name)>0 and isinstance(node.targets[0],ast.Name):
            self.class_obj[node.targets[0].id] = call_name[-1]["name"]
        return node

def get_api_ref_id(tree):
    id2fullname  = {}  # key is the imported module while the value is the prefix
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            items = [nn.__dict__ for nn in node.names]
            for d in items: 
                if d['asname'] is None:  # alias name not found, use its imported name
                    id2fullname[d['name']] = d['name']
                else:
                    id2fullname[d['asname']] = d['name'] # otherwise , use alias name
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            # for import from statements
            # module names are the head of a API name
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None: # alias name not found
                    id2fullname[d['name']] = node.module+'.'+d['name'] 
                else:
                    id2fullname[d['asname']] = node.module+'.'+d['name']
    return id2fullname

# formating function calls
def func_call_format(func_call_names, id2fullname):
    result = []
    for name in func_call_names:
        
        name_parts = name.split('.')
        if name_parts[0] in id2fullname:
            full_name = id2fullname[name_parts[0]] + '.'+ ".".join(name_parts[1:])
            result += [full_name.rstrip('.')]
   
    return result

def get_API_calls(code):

    tree = ast.parse(code, mode='exec')
    visitor = AssignVisitor()
    visitor.visit(tree)
    class2obj = visitor.class_obj
    func_calls_names = get_func_calls(tree)

    
    new_func_calls_names = []
    
    for call_name_entry in func_calls_names:
        name = call_name_entry["name"]
        name_parts = name.split('.')  # object value
     
        if name_parts[0] in class2obj and len(name_parts)==2:
            new_func_calls_names +=[class2obj[name_parts[0]]+'.'+'.'.join(name_parts[1:])]
        else:
            new_func_calls_names.append(name)
    id2fullname = get_api_ref_id(tree)
  
    func_calls_names = func_call_format(new_func_calls_names, id2fullname)
    
    return func_calls_names


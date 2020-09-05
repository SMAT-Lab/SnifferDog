import os
import json
import ast

def get_path_by_extension(root_dir, flag='.py'):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if not f[0] == '.']  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths

def get_code_list(path):
    content = open(path).read()
    try:
        content = json.loads(content)
        if 'worksheets' in content:
            cells = content['worksheets'][0]['cells']
            source_flag = 'input'
        else:
            cells = content['cells']
            source_flag = 'source'
        cells = list(filter(lambda x:x['cell_type']=='code', cells))
        sources = []
        for cell in cells:
            # filter out cells without execution count
            if 'execution_count' in cell and cell['execution_count'] is not None:
                # remove magic functions
                code_lines = cell[source_flag]
                if code_lines is not None:
                    code_lines = list(filter(lambda x:len(x)>0 and x[0] not in ['%', '!', '#'], code_lines)) #
                    s = "".join(code_lines)
                    sources.append(s)
        return sources
    except:
        return []
# to convert the jupyter notebook to python script

def build_ast(code):
    try:
        tree = ast.parse(code, mode='exec')
        return tree
    except Exception as e:  # to avoid non-python code
        print("Syntax Error!!!", e)
        return None


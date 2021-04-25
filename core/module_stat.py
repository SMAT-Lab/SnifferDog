import os
import sys
import ast
import json
import pkgutil
from .util import get_code_list, get_path_by_extension
from .API_name_formating import  get_API_calls
from multiprocessing import Pool
# load standard Python modules

std_modules27 =  open('data/std_modules.2.7.18.txt').readlines()
std_modules31 =  open('data/std_modules.3.1.5.txt').readlines()
std_modules32 =  open('data/std_modules.3.2.6.txt').readlines()
std_modules33 =  open('data/std_modules.3.3.7.txt').readlines()
std_modules34 =  open('data/std_modules.3.4.10.txt').readlines()
std_modules35 =  open('data/std_modules.3.5.9.txt').readlines()
std_modules36 =  open('data/std_modules.3.6.10.txt').readlines()
std_modules37 =  open('data/std_modules.3.7.7.txt').readlines()
std_modules38 =  open('data/std_modules.3.8.3.txt').readlines()
std_modules = std_modules27+std_modules31+std_modules32+std_modules33+std_modules34+std_modules35+std_modules36+std_modules37+std_modules38
std_modules = set(map(lambda x:x.strip(), std_modules))

def single_file(filename):
    try:
        code_text = get_source(filename)
        print(filename, code_text)
        func_calls_names= get_API_calls(code_text)
        func_calls_names = [name.split(':')[0] for name in func_calls_names]
        return func_calls_names
    except:
        return []
# extract source code from notebooks or python source files
def get_source(filename):
    if filename.endswith('.py'):
        return open(filename).read()
    elif filename.endswith('.ipynb'):
        code = get_code_list(filename)
        return "\n".join(code)

def get_all_folder_names(root_dir, flag='.py'):
    folder_names = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        files = [f.rstrip('.py') for f in files if f.endswith(flag)]
        folder_names.extend(dirs)
    return folder_names

def get_module_names(filename, std_modules, local_folders):
    try:
        module_names = []
        source = get_source(filename)
        tree = ast.parse(source, mode='exec')
        search_path = ['.']
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    module_names.append(d['name'].split('.')[0])
            #if isinstance(node, ast.ImportFrom) and node.module is not None and node.level==0:
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                # for import from statements
                # module names are the head of a API name
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    module_names.append(node.module.split('.')[0])
        local_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
        local_modules.extend(local_folders)
        module_names = [name for name in module_names if name not in local_modules and name not in std_modules]
        return module_names
    except Exception as e :# to avoid non-python code
        print("Syntax Error!!!", e)
        return None


def main():
    parse_module_names()

def collect_module_single(repo_dir):
    local_folders = get_all_folder_names(repo_dir)
    all_fns_py =  get_path_by_extension(repo_dir, flag='.py')
    all_fns_nb =  get_path_by_extension(repo_dir, flag='.ipynb')
    all_fns = all_fns_py+all_fns_nb 
    module_names = []
    for fn in all_fns:
        pwd = os.getcwd() # save current path
        working_dir = os.path.dirname(fn)
        os.chdir(working_dir)  # go to that  folder
        #module_name_tmp = get_module_names(fn, std_modules, local_folders)
        module_name_tmp = get_module_names(fn, std_modules, [])
        if module_name_tmp is not None:
            module_names.extend(module_name_tmp)
        os.chdir(pwd)
    module_names = list(set(module_names))
    return module_names 

def API_extracting_single(nb_path):
    all_results = {}
    #module_repos = json.loads(open('mining_API/data/module_repos.json').read())
    repo_name = nb_path.split('/')[5]
    print(nb_path)
    repo_path = "/".join(nb_path.split('/')[:6])
    module_names = collect_module_single(repo_path)
    result = get_code_list(nb_path)
    code = "".join(result)
    func_calls_names= get_API_calls(code)
    func_calls_names = [name.split(':')[0] for name in func_calls_names]
    n_threads = 8
    results = {}
    with Pool(n_threads) as pool:
        all_file_names = get_path_by_extension(repo_path)
        tmp_res = pool.map(single_file, all_file_names)
        tmp_res = tmp_res + func_calls_names
        results = {'API':tmp_res, 'module': module_names}
    return results
#if __name__ == '__main__':
    #main()
    #module_stat_report()
    #module_collect_repo()
    #get_subject_repos()
    #API_extracting()

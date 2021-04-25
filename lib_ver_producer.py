import sys
import os
import json
import time
from functools import reduce
import functools
from pkg_resources import parse_version
from functools import cmp_to_key
import nbformat
import ast
from core.API_name_formating import  get_API_calls 
from core.module_stat import  API_extracting_single 

# parse a single lib's all APIs
def parse_lib_APIs(lines):
    name = ""
    d = {}
    lines = list(map(lambda x:x.strip(), lines))
    name = lines[0].split('.')[0]
    for line in lines:
        API_name, versions =  line.split(':')
        d[API_name] = versions.split(',')
    return name, d

def get_module_names(source, std_modules, local_folders):
    try:
        tree = ast.parse(source, mode='exec')
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    module_names.append(d['name'].split('.')[0])
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                # for import from statements
                # module names are the head of a API name
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    module_names.append(node.module.split('.')[0])
        return module_names
    except Exception as e :# to avoid non-python code
        print("Syntax Errror !!!", e)
        return None

def get_modules_again(nb_path):
    with open(nb_path) as f:
        nb = nbformat.read(f, as_version=4)
        # filter out cells without execution count
        cells = list(filter(lambda x:x['cell_type'] == 'code' and x['execution_count'] is not None, nb.cells))
        source_list = map(lambda x:x['source'], cells)
        source_lines = "\n".join(source_list).split('\n')
        # either 0 or not a magic function
        source_lines = filter(lambda x:len(x)==0 or x[0] not in ['%', '#', '!'], source_lines)
        source = '\n'.join(source_lines)
        results = get_API_calls(source)
        results = [r.split(':')[0] for r in results]
        return results

def module2package():
    root_dir = 'data'
    all_lib_fns = os.listdir(root_dir)
    API_database = {}
    m2p = {}
    for fn in all_lib_fns:
        tmp_dir = os.path.join(root_dir, fn)
        API_data_tmp = json.loads(open(tmp_dir).read())
        names = set()
        for k in API_data_tmp.keys():
            names.add(k.split('.')[0])
        for name in names:
            m2p[name]=fn
        API_database[fn] = API_data_tmp
    return m2p, API_database

def list_intersec(all_sets):
    #input: a list of lists
    #output : a list
    if len(all_sets)>0:
        new_lst = reduce(lambda x, y : x & y, all_sets)
        new_lst = list(new_lst)
        new_lst.sort(key= lambda x: parse_version(x))
        return new_lst
    else:
        return None
def version_resolve(version_result):
    new_result= {}
    for k, v in version_result.items():
        new_result[k] = list_intersec(v)
    return new_result

def API_version_lookup(API_data, name):
    for k, v in API_data.items():
        if k.split(',')[0] == name:
            return v
    # cannot find this API
    return []
def version_intersection(result):
    new_res = {}
    for k, v in result.items():
        if v is None:
            new_res[k] = v
        else:
           v = [set(l) for l in v if len(l)>0]
           new_v = list_intersec(v)
           if new_v is None or  len(new_v) == 0:
               new_res[k] = None
           else:
               new_res[k] = new_v 
    return new_res
def load_API_bank():
    data_dir = 'API-bank-data/'
    m2p = {}  # module to packages
    all_filenames = os.listdir(data_dir)
    API_DB = {}
    all_modules = []
    for fn in all_filenames:
        path = os.path.join(data_dir, fn)
        API_data = json.loads(open(path).read())
        for m in API_data['module']: 
            package_name = fn[:-5]
            module_name = m.split('/')[-1]
            all_modules.append(module_name)
            m2p[module_name] = package_name
            API_DB[package_name] = API_data['API']
    return m2p, API_DB

def lst_unfold(lst):
    new_lst = []
    for l in lst:
        if isinstance(l, list):
            new_lst.extend(l)
        else:
            new_lst.append(l)
    return new_lst

def main():
    nb_path = sys.argv[1]
    req_entries = []
    used_API_info = API_extracting_single(nb_path)
    tmp_module = used_API_info['module']
    tmp_API = used_API_info['API']
    tmp_API = lst_unfold(tmp_API)
    #print(tmp_API)
    #m2p, API_DB = load_API_bank()
    return 

    if all(x in m2p for x in tmp_module):
        result = {}
        package_names = [m2p[m_name] for m_name in tmp_module if m_name in m2p]
        package_names = set(package_names)
        #req_path = os.path.join(target_dir, repo_name)
        if len(tmp_API) == 0:
            for pn in package_names:
                entry = "{}".format(pn)
                req_entries.append(entry)
            #f = open(req_path, 'w')
            #req_content = "\n".join(req_entries)
            #print(len(req_entries))
            #f.write(req_content)
            #f.close()
        else:
            for API in tmp_API:
                m_name = API.split('.')[0]
                tmp_package_name = m2p[m_name]
                versions = API_version_lookup(API_DB[tmp_package_name], API)
                if m_name in result:
                    result[tmp_package_name].append(versions)
                else:
                    result[tmp_package_name] = [versions]

            new_result = version_intersection(result)
            for pn in package_names:
                if pn not in new_result:
                    new_result[pn] = None
            for k, v in new_result.items():
                if v is not None:
                    if len(v)==1:
                        entry = "{}=={}".format(k,v[0])
                    else:
                        entry = "{}>={},<={}".format(k, v[0],v[-1])
                    req_entries.append(entry)
                else:
                    entry = "{}".format(k)
                    req_entries.append(entry)
            req_content = "\n".join(req_entries)
            #print(len(req_entries))
            print(req_content)
            #f = open(req_path, 'w')
            #f.write(req_content)
            #f.close()
if __name__ == '__main__':
    main()


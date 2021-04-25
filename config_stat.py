import os
import sys
import json
def get_nb_file(filenames):
    for fn in filenames:
        if fn.endswith('.ipynb'):
            return fn
def get_conda_file(filenames):
    for fn in filenames:
        if fn.endswith('.yml'):
            return fn
def check(filenames):
    d = {'pip':False, 'req':False, 'conda':False, 'setup':False}
    for fn in filenames:
        dir_name = os.path.dirname(fn)
        dir_name = dir_name.split('/')
        if dir_name[-2] != 'data':
            continue
        base_name = os.path.basename(fn)
        if base_name == 'requirements.txt':
            d['req'] = True
        if base_name== 'Pipfile':
            d['pip'] = True
        if base_name.endswith(".yml"):
            d['conda'] = True
        if base_name == 'setup.py':
            d['setup'] = True
    return d

def is_valid_conda(conda_file):
    content = open(conda_file).read()
    if content.find('dependencies')>=0:
        return True
    return False
def main():
    n_req = 0
    n_conda = 0
    n_pip = 0
    n_setup = 0

    content = open('config_stat.json','r').read() 
    results = json.loads(content)
    n_all = 0
    req_rows = []
    for r in results:
        filenames = r[1]
        d = check(filenames)
        repo_name = os.path.basename(r[0])
        if d['req'] is True:
            n_req += 1
            nb_file = get_nb_file(filenames)
            #print("{}|{}|{}".format(repo_name, os.path.join(r[0], 'requirements.txt'), nb_file))
            #req_rows.append() 
        #if d['conda'] is True and d['req'] is not True:
        if d['conda'] is True:
            nb_file = get_nb_file(filenames)
            conda_file  = get_conda_file(filenames)
            if is_valid_conda(conda_file):
                #print(conda_file)
                if not conda_file.endswith( '_config.yml'):
                    print("{}|{}|{}".format(repo_name, os.path.join(r[0], conda_file), nb_file))
                    n_conda += 1
        #if d['pip'] and d['conda'] is not True and d['req'] is not True:
        if d['pip']:
            n_pip += 1
            #print("{}|{}|{}".format(repo_name, os.path.join(r[0], 'Pipfile'), nb_file)) 
        if d['setup']:
            n_setup += 1
            #print("{}|{}|{}".format(repo_name, os.path.join(r[0], 'Pipfile'), nb_file))
        #    pass
        #if d['setup'] == False and d['req'] == False and d['conda'] == False and d['pip'] == False:
        #    nb_files = get_nb_file(filenames)
        #    print("{}|{}".format(repo_name, nb_files))
        #if d['setup'] or  d['req'] or d['conda'] or d['pip']:
        #    nb_file = get_nb_file(filenames)
        #    #print(nb_file) 
        #    n_all += 1
    ##print(len(results))
    print("req: {}, conda: {}, pip: {}, setup: {}".format(n_req, n_conda, n_pip, n_setup))
    print(n_all)

if __name__ == '__main__':
    main()

import os
import sys
import json
from multiprocessing import Pool

def get_path_by_extension(root_dir):
    filenames = []
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if not f[0] == '.']  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for f in files:
            filenames.append(os.path.join(root, f))
    return (root_dir, filenames)

def is_contain_yml(filenames):
    for fn in filenames:
        if fn.endswith('.yml'):
            return True
    return False

def is_contain_pipfile(filenames):
    return 'Pipfile' in filenames

def parse_module_names():

    all_repos = open('folder_names.txt', 'r').readlines()
    all_repos = list(map(lambda x:os.path.join('/mnt/fit-Knowledgezoo/Github_repos_download/data/', x.strip()), all_repos))
    #all_repos = all_repos[0:50]
    results = {}
    n_threads = 4
    with Pool(n_threads) as pool:
        results = pool.map(get_path_by_extension, all_repos)
        f = open('config_stat.json','w')
        f.write(json.dumps(results))
        f.close()

    #for folder in all_repos[0:100]:
    #    count += 1
    #    if count%1000==0:
    #        f = open('config_stat.json','w')
    #        f.write(json.dumps(results))
    #        f.close()
    #        print(count)

        #folder = folder.strip()
        #repo_dir = os.path.join('/mnt/fit-Knowledgezoo/Github_repos_download/data/', folder)
        #req_dir = os.path.join(repo_dir, 'requirements.txt')
        #if os.path.exists(req_dir):
 
        #filenames = get_path_by_extension(repo_dir) 
        #results[repo_dir]= filenames
        #results[repo_dir]=  {
        #        "conda": is_contain_yml(filenames),
        #        'pip': is_contain_pipfile(filenames),
        #        'req': 'requirements.txt' in filenames,
        #        'setup': 'setup.py' in filenames
        #        }
        #f = open('config_stat.json','w')
        #f.write(json.dumps(results))
        #f.close()


def main():
    parse_module_names()

if __name__ == '__main__':
    main()

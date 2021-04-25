import sys
import os
import nbformat

def load_all_rows():
    filename = 'folder-git.txt'
    all_row = {}
    for line in open(filename).readlines():
        line = line.strip()
        tmp = line.split(',')
        all_row[tmp[0]] =  tmp[1]
    return all_row

def main():
    filename = sys.argv[1]
    repo_names = open(filename).readlines()
    repo_names = [line.strip() for line in repo_names]
    all_row = load_all_rows()
    for k, v in all_row.items():
        print(v)

    return 0
    for tmp_line  in repo_names:
        tmp = tmp_line.strip().split('|')
        env_dir = "/".join(tmp[2].split('/')[6:])
        nb_dir =  "/".join(tmp[3].split('/')[6:])
        try:
            #print(tmp[2])
            with open(tmp[3], 'r') as f:
                nb = nbformat.read(f, as_version=4)
                version = nb['metadata']['language_info']['version']
                print("{},{},{},{},{}".format(tmp[0], all_row[tmp[0]], version, env_dir, nb_dir))
        except:
                # ID name,git repo,  python version, env_file, nb file
                print("{},{},{},{}".format(tmp[1], all_row[tmp[1]], version, env_dir, "bad file")) 
    return 0
if __name__ == '__main__':
    main()

import os
import json
import sys
from pkg_resources import parse_version
from functools import reduce
def main():
    filenames = os.listdir('API-bank-data/')
    n_all = 0
    same_name_API_dict = {}
    n_changes = 0
    n_versions = 0 
    n_del = 0
    n_add = 0
    for fn in filenames:
        API_data = json.loads(open('API-bank-data/'+fn).read())
        API_data = API_data['API']
        all_versions = set()
        for v in API_data.values():
            all_versions.update(v)
        n_versions += len(all_versions)
        all_versions = list(all_versions)
        all_versions.sort(key=lambda x: parse_version(x))
        if len(all_versions)>0:
            max_v = all_versions[-1]
            min_v = all_versions[0]
        else:
            max_v = []
        for k, v in API_data.items():
            tmp = k.split(',')
            name = tmp[0]
            args = tmp[1]
            if name not in same_name_API_dict:
                same_name_API_dict[name] = [args]
                if max_v not in v:
                    n_del += 1
                if min_v not in v:
                    n_add += 1
            else:
                same_name_API_dict[name].append(args) 
        n_all += len(API_data)
    n_same_API = len(same_name_API_dict)
    for k,v in same_name_API_dict.items():
        if len(v)>1:
           arg_set = [set(tmp.split(';')) for tmp in v]
           new_lst = reduce(lambda x, y : x & y, arg_set)
           if len(new_lst)>1:
               n_changes += 1
    n_all = len(same_name_API_dict)
    print("The number of libs {}".format(len(filenames)))
    print("The number of releases {}".format(n_versions))
    print("The number of total APIs {}".format(n_all))
    print("The number of added {}".format(n_add))
    print("The number of removals {}".format(n_del))
    print("The number of updated {}".format(n_changes))

if __name__ == '__main__':
    main()

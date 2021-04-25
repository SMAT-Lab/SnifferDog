import json
import sys
import os
import requests
import wget
import tarfile

#invalid_suffixes = ('.exe', '.whl')
invalid_suffixes = ('.exe')
data_dir = '.'
def single_package(package_name):
    url = "https://pypi.python.org/pypi/{}/json".format(package_name)
    r = requests.get(url)
    if r.status_code != 200:
        print("failed to fetch {}".format(package_name))
        return 0
    working_dir = os.path.join(os.path.join(data_dir, package_name))
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
        data= json.loads(r.text)
        versions = data["releases"].keys()
        for v in versions:
            urls = [ele['url'] for ele in data["releases"][v]]
            new_dir = os.path.join(working_dir, v)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            for url in urls:
                if url.endswith(invalid_suffixes):
                    continue
                wget.download(url, os.path.join(new_dir))
def main():
    package_name = sys.argv[1]
    single_package(package_name)

if __name__ == '__main__':
    main()



import os
import sys
import nbformat

def main():
    fn = sys.argv[1]
    try:
        with open(fn, 'r') as f:
            nb = nbformat.read(f, as_version=4)
            version = nb['metadata']['language_info']['version']
            print("Python version for this notebook is {}".format(version))
    except Exception as e:
        pass
if __name__ == '__main__':
    main()


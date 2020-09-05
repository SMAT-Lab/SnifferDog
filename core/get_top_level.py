import os
import sys
from wheel_inspect import inspect_wheel

def main():
    fname = sys.argv[1]
    output = inspect_wheel(fname)
    print(output['dist_info']['top_level'])
    print(output['derived']['modules'])
    return 0

if __name__ == '__main__':
    main()



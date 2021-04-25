import os
import sys
import nbformat


def main():
    row_file = sys.argv[1]
    #filenames = open('pip.nb.all').readlines()
    #filenames = open('req.nb.all').readlines()
    filenames = open(row_file).readlines()
    py2 = 0
    py34 = 0
    other = 0
    #for row in filenames[3428:]:
    for row in filenames:
        fn = row.strip().split('|')[-1]
        if fn == 'None':
            continue
        try:
            with open(fn, 'r') as f:
                    nb = nbformat.read(f, as_version=4)
                    version = nb['metadata']['language_info']['version']
                    if version[0] == '3' and version[2] not in ['4', '3', '2', '1']:
                        #new_str = "{}|{}".format(version[0:3], row.strip())
                        #print( row.strip())
                        print("{}|{}".format(version[0:3], row.strip()))
                        pass
                    else:
                        if version[0] == '3':
                            py34 += 1
                        else:
                            py2 +=1

        except Exception as e:
            other += 1
            pass

    #print("Python2 {}  Python34 {}  Other {} ".format(py2, py34,  other) )


    return 0

if __name__ == '__main__':
    main()


import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

def run_single_notebook():
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            nb = nbformat.read(f, as_version=4)
            # filter out cells without execution count
            cells = list(filter(lambda x:x['cell_type'] == 'code' and
                x['execution_count'] is not None, nb.cells))

            # if you wish to run the notebooks in the original execution counter order
            # then sort code cells by oec values:
            # cells.sort(key=lambda x:x['execution_count'])

            nb.cells = cells # assign new cells
            ep = ExecutePreprocessor(timeout=600)#timeout is set as 10 mins
            res = ep.preprocess(nb, {'metadata': {'path': os.path.dirname(filename)}})

            print('success')
    except Exception as e:
        print(e)
        print('failed-filename:', filename)

    return 0
if __name__ == '__main__':
    run_single_notebook()

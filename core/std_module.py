import sys
import re
import requests

def main():
    url = "https://docs.python.org/3/py-modindex.html"  # 3.8
    url = "https://docs.python.org/3.7/py-modindex.html"  # 3.7
    url = "https://docs.python.org/3.6/py-modindex.html"  # 3.6
    url = "https://docs.python.org/3.5/py-modindex.html"  # 3.5
    url = "https://docs.python.org/3.4/py-modindex.html"  # 3.4
    url = "https://docs.python.org/3.3/py-modindex.html"  # 3.3
    url = "https://docs.python.org/3.2/py-modindex.html"  # 3.2
    url = "https://docs.python.org/3.1/modindex.html" # 3.1

    #url = "https://docs.python.org/2.7/py-modindex.html"  # 2.7 
    r = requests.get(url)
    text = r.text
    #these_regex='<code class="xref">(.+?)</code>'
    these_regex='<tt class="xref">(.+?)</tt>'
    pattern=re.compile(these_regex)
    lib_names =re.findall(pattern,text)
    std_module_names = []
    for name in lib_names:
        name = name.split('.')[0]
        if name not in std_module_names:
            std_module_names.append(name)
    print("\n".join(std_module_names))



if __name__ == '__main__':
    main()

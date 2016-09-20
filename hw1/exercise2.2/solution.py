from __future__ import print_function

map(lambda x : print(x, end=" "),
    filter(lambda x : x % 2 != 0, range(50, 150)))

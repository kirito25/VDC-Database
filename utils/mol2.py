import re

def molecules(string):
    """
    A generator that which takes a string consisting of 
    multiple mol2 molecules and generate them individually for the user
    as a tuple (name, data)
    """
    start = '@<TRIPOS>MOLECULE\n'
    begin = string.find(start, 0)
    end = string.find(start, begin + 1)
    while 0 < end < len(string):
        name = string[len(start) + begin : string.find('\n', begin + len(start))]
        yield (name, string[begin:end])
        begin = end + 0
        end = string.find(start, begin + 1)
    # yield the left over text
    name = string[len(start) + begin : string.find('\n', begin + len(start))]
    yield (name, string[begin:])


if __name__ == '__main__':
    import sys
    f = open(sys.argv[1])
    s = f.read()
    g = molecules(s)
    print g.next()
    f.close()


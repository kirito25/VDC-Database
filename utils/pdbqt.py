import re

def models(string):
    """
    Takes the string representation of an entire pdbqt file
    and generates each model to the user as a tuple(name, string).
    If the name is not available than its None
    """
    string = string.split('\n')
    name = re.compile(r'Name.*', re.IGNORECASE)
    start = re.compile(r'^MODEL')
    start_line = None
    for i, line in enumerate(string):
        if start_line is not None and start.match(line):
            n = '\n'.join(string[start_line:i]) + '\n'
            try:
                yield (name.findall(n)[0].split(' ')[-1], n)
            except IndexError:
                yield (None, n)
            start_line = None
        if start.match(line):
            start_line = i
    # make sure to yield the leftover one
    yield (name.findall(n)[0].split(' ')[-1], '\n'.join(string[start_line:i]) + '\n')


if __name__ == '__main__':
    import sys
    f = open(sys.argv[1])
    s = f.read()
    print list(models(s))[-1]
    f.close()


"""
Mapping as describe in http://files.docking.org/3D/
ex.
    ABCDEF
    A - molecular weight
    B - logP
    C - reactivity
    D - purchasability
    E - pH
    F - net charge

"""
import re

molecular_weight = {
    'A': 200,
    'B': 250,
    'C': 300,
    'D': 325,
    'E': 350,
    'F': 375,
    'G': 400,
    'H': 425,
    'I': 450,
    'J': 500,
    'K': 600
}

log_p = {
    'A': -1,
    'B': 0,
    'C': 1,
    'D': 2,
    'E': 2.5,
    'F': 3,
    'G': 3.5,
    'H': 4,
    'I': 4.5,
    'J': 5,
    'K': 6
}

reactivity = {
    'A': 'anodyne',
    'B': 'bother',
    'C': 'clean',
    'E': 'mild',
    'G': 'reactive',
    'I': 'hot chemistry'
}

purchasability = {
    'A': 'in stock',
    'B': 'in stock',
    'C': 'agent',
    'D': 'make on demand',
    'E': 'boutique',
    'F': 'annotated'
}

pH = {
    'R': 'ref',
    'M': 'mild',
    'L': 'low',
    'H': 'high'
}

net_charge = {
    'N': 0,
    'M': -1,
    'L': -2,
    'O': 1,
    'P': 2
}

def parse_filename(name):
    """
    Convert the 6 character into the dictionary of their meaning.
    Keys:
        'weight', 'logP', 'reactivity', 'purchasability', 'pH', 'charge'

    returns None is not 6 characters long, is not a string, or there is an error
    """
    if len(name) < 6 or type(name) is not str:
        return None
    name = name[:6]
    name = name.upper()
    try:
        info = {
            'weight': molecular_weight[name[0]],
            'logP': log_p[name[1]],
            'reactivity': reactivity[name[2]],
            'purchasability': purchasability[name[3]],
            'pH': pH[name[4]],
            'charge': net_charge[name[5]]
        }
    except KeyError:
        return None
    return info

def parse(filename):
    """
    Takes a filename from dowloaded from zinc15 tranches and
    return a dictionary of what the file name means, the file..
    """
    a = parse_filename(filename[:6])
    if a is None:
        return None
    a['file'] = filename
    a['type'] = filename.split('.')[-1]
    return a

if __name__ == "__main__":
    import sys
    a = parse(sys.argv[1])
    print a




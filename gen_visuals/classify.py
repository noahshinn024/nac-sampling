import json

"""
BIN KEY:
    0: zero
    1: [-0.2, -0.1625)
    2: [-0.1625, -0.125)
    3: [-0.125, -0.0875)
    4: [-0.0875, -0.05)
    5: infinity

"""

NBINS = 6

with open('./data-nacs.json', 'r') as f:
    data = json.load(f)
    l = len(data['atom_types'])
    
    bins = []
    for i in range(l):
        mag = abs(data['energy_differences'][i] * 27.2107)
        if mag > 0.2:
            bins += [0]
        elif mag > 0.1625:
            bins += [1]
        elif mag > 0.125:
            bins += [2]
        elif mag > 0.0875:
            bins += [3]
        elif mag > 0.05:
            bins += [4]
        else:
            bins += [5]

    new_data = {}
    new_data['species'] = data['atom_types']
    new_data['coords'] = data['coords']
    new_data['nacs'] = data['nacs']
    new_data['norms'] = data['norms']
    new_data['e_diffs'] = data['energy_differences']
    new_data['bin'] = bins

    with open(f'nacs-{NBINS}-bins.json', 'w') as f:
        json.dump(new_data, f)
        print(f'dumped {l} structures to file')

with open(f'./nacs-{NBINS}-bins.json', 'r') as f:
    data = json.load(f)
    nstructures = len(data['species'])
    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    infinity = 0
    for i in range(nstructures):
        b = data['bin'][i]
        if b == 0:
            zero += 1
        elif b == 1:
            one += 1
        elif b == 2:
            two += 1
        elif b == 3:
            three += 1
        elif b == 4:
            four += 1
        elif b == 5:
            infinity += 1
        else:
            import sys
            print(f'exiting: {b} is not a valid bin!')
            sys.exit(0)

    print(f'BINS:')
    print(f'zero: {zero}, {(zero / nstructures):.4f}')
    print(f'one: {one}, {(one / nstructures):.4f}')
    print(f'two: {two}, {(two / nstructures):.4f}')
    print(f'three: {three}, {(three / nstructures):.4f}')
    print(f'four: {four}, {(four / nstructures):.4f}')
    print(f'infinity: {infinity}, {(infinity / nstructures):.4f}')








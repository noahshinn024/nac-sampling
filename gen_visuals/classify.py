import json

"""
BIN KEY:
    0: zero
    1: non-zero
    2: infinity

"""

# with open('./data-nacs.json', 'r') as f:
    # data = json.load(f)
    # l = len(data['atom_types'])
    
    # bins = []
    # for i in range(l):
        # mag = abs(data['energy_differences'][i] * 27.2107)
        # if mag > 0.2:
            # bins += [0]
        # elif mag > 0.05:
            # bins += [1]
        # else:
            # bins += [2]

    # new_data = {}
    # new_data['species'] = data['atom_types']
    # new_data['coords'] = data['coords']
    # new_data['nacs'] = data['nacs']
    # new_data['norms'] = data['norms']
    # new_data['e_diffs'] = data['energy_differences']
    # new_data['bin'] = bins

    # with open('nacs-3-bins.json', 'w') as f:
        # json.dump(new_data, f)
        # print(f'dumped {l} structures to file')

with open('./nacs-3-bins.json', 'r') as f:
    data = json.load(f)
    nstructures = len(data['species'])
    zero = 0
    non_zero = 0
    infinity = 0
    for i in range(nstructures):
        b = data['bin'][i]
        if b == 0:
            zero += 1
        elif b == 1:
            non_zero += 1
        elif b == 2:
            infinity += 1
        else:
            import sys
            print(f'exiting: {b} is not a valid bin!')
            sys.exit(0)

    print(f'BINS:')
    print(f'zero: {zero}, {(zero / nstructures):.4f}')
    print(f'non-zero: {non_zero}, {(non_zero / nstructures):.4f}')
    print(f'infinity: {infinity}, {(infinity / nstructures):.4f}')








import sys
import json
import numpy as np

assert len(sys.argv) == 4
RD_FILE = sys.argv[1]
WR_FILE = sys.argv[2]
NBINS = sys.argv[3]

with open(RD_FILE, 'r') as f:
    data = json.load(f)
    l = len(data['species'])
    
    bins = []
    for i in range(l):
        # mag = abs(data['e_diffs'][i] * 27.2107)
        mag = abs(data['e_diffs'][i])
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

    data['bin'] = bins

    with open(WR_FILE, 'w') as f:
        json.dump(data, f)
        print(f'dumped {l} structures to file')

with open(WR_FILE, 'r') as f:
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








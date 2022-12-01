import os
import json

NBINS = 6
_EFFECTIVE_N_BINS = NBINS - 2
_WDIR = f'{NBINS}-bins'
LABELED_DATA_FILE = f'./nacs-{NBINS}-bins.json'

if not os.path.exists(_WDIR):
    os.mkdir(_WDIR)


with open(LABELED_DATA_FILE, 'r') as f:
    data = json.load(f)
    nstructures = len(data['species'])

    new_data = {}
    for i in range(_EFFECTIVE_N_BINS):
        new_data[str(i + 1)] = {
            'species': [],
            'coords': [],
            'nacs': [],
        }

    print(f'assigning {nstructures} structures...')
    for i in range(nstructures):
        bin_ = str(data['bin'][i])
        if bin_ in new_data.keys():
            new_data[bin_]['species'] += [data['species'][i]]
            new_data[bin_]['coords'] += [data['coords'][i]]
            new_data[bin_]['nacs'] += [data['nacs'][i]]

    for k, v in new_data.items():
        wfile = os.path.join(_WDIR, f'{NBINS}-bins-{k}-data.json')
        bin_nstructures = len(v['species'])
        with open(wfile, 'w') as wf:
            json.dump(v, wf)
            print(f'dumped {bin_nstructures} structures to `{wfile}`')

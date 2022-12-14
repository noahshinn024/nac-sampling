import json

with open('./data-nacs.json', 'r') as f:
    data = json.load(f)
    new_data = {
        'species': data['atom_types'],
        'coords': data['coords'],
        'e_diffs': data['energy_differences'],
        'norms': data['norms'],
        'nacs': data['nacs'],
    }
    with open('./data-nacs-new.json', 'w') as wf:
        json.dump(new_data, wf)

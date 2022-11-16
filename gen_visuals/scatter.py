import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

with open('./data-nacs.json', 'r') as f:
    data = json.load(f)
    e_diffs = data['energy_differences']
    avg_nac_elems = np.abs(np.asarray(data['nacs'])).mean(axis=(1, 2))

# xy = np.vstack([e_diffs, avg_nac_elems])
# z = gaussian_kde(xy)(xy)
    
# plt.scatter(e_diffs, avg_nac_elems, c=z, s=100)
plt.scatter(e_diffs, avg_nac_elems)
# plt.show()
plt.savefig('e_diff_vs_avg_nac.png')

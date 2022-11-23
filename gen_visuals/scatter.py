import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

with open('../../scratch/filtered-005-02.json', 'r') as f:
    data = json.load(f)
    e_diffs = np.asarray(data['e_diffs']) * 27.2114
    avg_nac_elems = np.abs(np.asarray(data['nacs'])).mean(axis=(1, 2))

# xy = np.vstack([e_diffs, avg_nac_elems])
# z = gaussian_kde(xy)(xy)
    
# plt.scatter(e_diffs, avg_nac_elems, c=z, s=100)
plt.scatter(e_diffs, avg_nac_elems)
plt.xlabel('energy difference (eVs)')
plt.ylabel('avg nac elem value')
# plt.xlim(-0.2, 0.0)
# plt.ylim(0.0, 25.0)
# plt.show()
plt.savefig('e_diff_vs_avg_nac_02_005_full.png')

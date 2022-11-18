import json
import numpy as np
import matplotlib.pyplot as plt

NBINS = 20

with open('./data-nacs.json') as f:
    data_orig = json.load(f)
    orig = np.abs(np.asarray(data_orig['nacs'])).mean(axis=(1, 2))
    orig_energies = np.asarray(data_orig['energy_differences']) * 27.2114

# with open('./out.json') as f:
    # data_sampled = json.load(f)
    # sampled = np.stack([np.abs(np.asarray(sample['nacs'])).mean() for sample in data_sampled], axis=0)
    # sampled = np.stack([np.asarray(sample['e_diff']) for sample in data_sampled], axis=0)

fig, axs = plt.subplots()
axs.hist(orig_energies, range=(-1.0, 0.0))
axs.set_xlabel('energy differences (eVs)')
axs.set_ylabel('count')
# plt.show()
plt.savefig('e_diff.png')
import sys
sys.exit()

fig, axs = plt.subplots(1, 2, sharey=False)
plt.suptitle('', fontsize=14)

axs[0].hist(orig, bins=NBINS)
axs[0].set_xlabel('avg nac elem')
axs[0].set_ylabel('count')
# axs[0].set_ylabel('avg element value of nac matrix')

axs[1].hist(orig_energies, bins=NBINS)
# axs[1].set_xlabel('downsampled e diff')
axs[1].set_xlabel('energy diff (hartrees)')
# axs[1].set_ylabel('downsampled count')
axs[1].set_ylabel('count')

plt.savefig('avg_nac_elem.png')
plt.show()

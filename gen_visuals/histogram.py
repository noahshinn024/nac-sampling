import json
import numpy as np
import matplotlib.pyplot as plt

from typing import List

NBINS = 20
BIN_WIDTH = 0.015

with open('../../scratch/filtered-005-02.json') as f:
    data_orig = json.load(f)
    orig = np.abs(np.asarray(data_orig['nacs'])).mean(axis=(1, 2))
    orig_energies = np.asarray(data_orig['e_diffs']) * 27.2114

# with open('./out.json') as f:
    # data_sampled = json.load(f)
    # sampled = np.stack([np.abs(np.asarray(sample['nacs'])).mean() for sample in data_sampled], axis=0)
    # sampled = np.stack([np.asarray(sample['e_diff']) for sample in data_sampled], axis=0)

def get_assigned_pts(arr: np.ndarray, bins: np.ndarray) -> List[np.ndarray]:
    res = [[] for _ in range(NBINS)]
    for pt in arr:
        for i, b in enumerate(bins):
            if pt >= b and pt < b + BIN_WIDTH:
                res[i] += [pt]
    res = [np.asarray(res[i]) for i in range(NBINS)]
    return res

fig, axs = plt.subplots()
mean = orig.mean()
std = orig.std()
axs.hist(orig, range=(mean - std * 3, mean + std * 3))
# n, bins, patches = axs.hist(orig, bins=NBINS, range=(-0.2, -0.05))
axs.set_xlabel('avg nac elem value')
axs.set_ylabel('count')
axs.set_title(f'Histogram of avg nac elem values mean={mean.round(2)}, std={std.round(2)}')
plt.show()
plt.savefig('avg_nac_elem_value.png')
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

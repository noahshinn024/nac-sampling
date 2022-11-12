import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple


nargs = len(sys.argv)
if nargs < 2 or nargs > 6:
    print(f'usage: [data file] [should display (default = True)] [should save (default = False)] [verbose (default = True)] [save to (default = check_classified.png)]')
    sys.exit(1)

DATA_FILE = sys.argv[1]
SHOULD_DISPLAY = bool(sys.argv[2])
SHOULD_SAVE = bool(sys.argv[3])
VERBOSE = bool(sys.argv[4])
SAVE_TO = sys.argv[5]
NBINS = 2


def _load(file: str) -> list:
    with open(file) as f:
        return json.load(f)

def _get_avg_nac_elem(nacs: list) -> float:
    return np.asarray(nacs).mean()

def _split_extract_data(data: list) -> Tuple[list, list]:
    is_like_zero_lst = []
    is_not_like_zero_lst = []
    for structure in data:
        avg_nac_elem = _get_avg_nac_elem(structure['nacs'])
        if structure['is_like_zero']:
            is_like_zero_lst += [avg_nac_elem]
        else:
            is_not_like_zero_lst += [avg_nac_elem]
    return is_like_zero_lst, is_not_like_zero_lst

def check_classified(
        file: str,
        should_display: bool = True,
        should_save: bool = False,
        verbose: bool = True,
        save_to: str = 'check_classified.png'
    ) -> None:
    data = _load(file)
    is_like_zero_data, is_not_like_zero_data = _split_extract_data(data)

    _, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    axs[0].hist(is_like_zero_data, NBINS)
    axs[1].hist(is_not_like_zero_data, NBINS)

    if verbose:
        print(f'plotting {len(is_like_zero_data)} `near zero` points and {len(is_not_like_zero_data)} `not near zero` points...')

    if should_display:
        plt.show()

    if should_save:
        plt.savefig(save_to)
          

if __name__ == '__main__':
    check_classified(DATA_FILE, SHOULD_DISPLAY, SHOULD_SAVE, VERBOSE, SAVE_TO)

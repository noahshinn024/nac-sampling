import sys
import json
<<<<<<< HEAD
=======
import argparse
>>>>>>> dev
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple

<<<<<<< HEAD

nargs = len(sys.argv)
if nargs < 2 or nargs > 6:
    print(f'usage: [data file] [should display (default = True)] [should save (default = False)] [verbose (default = True)] [save to (default = check_classified.png)]')
    sys.exit(1)

DATA_FILE = sys.argv[1]
SHOULD_DISPLAY = bool(sys.argv[2])
SHOULD_SAVE = bool(sys.argv[3])
VERBOSE = bool(sys.argv[4])
SAVE_TO = sys.argv[5]
=======
>>>>>>> dev
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
<<<<<<< HEAD
=======
            print(structure['is_like_zero'])
>>>>>>> dev
            is_like_zero_lst += [avg_nac_elem]
        else:
            is_not_like_zero_lst += [avg_nac_elem]
    return is_like_zero_lst, is_not_like_zero_lst

def check_classified(
        file: str,
        should_display: bool = True,
        should_save: bool = False,
<<<<<<< HEAD
        verbose: bool = True,
        save_to: str = 'check_classified.png'
=======
        save_to: str = 'check_classified.png',
        verbose: bool = True
>>>>>>> dev
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
          
<<<<<<< HEAD

if __name__ == '__main__':
    check_classified(DATA_FILE, SHOULD_DISPLAY, SHOULD_SAVE, VERBOSE, SAVE_TO)
=======
def run() -> None:
    parser = argparse.ArgumentParser(description='A classification dataset checker.')
    parser.add_argument('-f', '--file', help='json file')
    parser.add_argument('-d', '--display', default=True, help='whether or not to display histogram(s)')
    parser.add_argument('-s', '--save', default=False, help='whether or not to save histogram(s) to png file')
    parser.add_argument('--verbose', default=True, help='whether or not to log checkpoint to console')
    parser.add_argument('--saveto', default='check_classified.png', help='png file in which to save histogram(s))')
    args = vars(parser.parse_args())
    if any(map(lambda x: x is None, args.values())):
        print('must supply all arguments -> run `python check_classified.py --help` to see a complete list of options')
    else:
        check_classified(
            file=args['file'],
            should_display=args['display'],
            should_save=args['save'],
            save_to=args['saveto'],
            verbose=args['verbose']
        )
    

if __name__ == '__main__':
    run()
>>>>>>> dev

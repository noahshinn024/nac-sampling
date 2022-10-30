# nac-sampling
A package used for faster sampling of non-adiabatic coupling datasets.

## Requirements
  - `rust`

## Installation
build from source
```
git clone https://github.com/noahshinn024/nac-sampling &&
cd nac-sampling &&
make
```

## To Run
```
./out --file <file.json> --nstructures 1000 --units hartree
```
results will be in `./out.json` unless specified by the `--wf` flag

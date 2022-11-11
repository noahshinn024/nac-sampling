# nac-sampling
A package used for faster sampling and classification of non-adiabatic coupling datasets written in Rust.

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

#### Downsampling Dataset Generation Example
```
./out --file <file.json> --nstructures 1000 --nbins 5 /
--upperbounds 0.1 0.3 0.7 1.5 inf --units hartree /
--verbose true
```
This command will generate a downsampled dataset split with `nstructures/nbins` `structures` in each `bin`. The dataset will be stored in `./out.json` unless specified by the `--wf` flag.

#### Classification and Downsampling Dataset Generation Example
```
./out --file <file.json> --nstructures 1000 --classify true /
--classifyby e_diff --classifybyvalue 0.3 --units hartree /
--verbose true
```
This command will generate a classification dataset split with 500 structures on both sides. The dataset will be stored in `./out.json` unless specified by the `--wf` flag.

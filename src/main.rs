use clap::Parser;
use serde::{Deserialize, Serialize};
use serde_json;
use std::fs;

//const UPPER_BOUNDS: &'static [&'static f64] = &[&0.1, &0.3, &0.7, &1.5, &f64::INFINITY];
const UPPER_BOUNDS: [f64; 5] = [0.1, 0.3, 0.7, 1.5, f64::INFINITY];
const NBINS: usize = 5;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    file: String,

    #[arg(short, long, default_value_t = 100)]
    nstructures: usize,

    #[arg(short, long)]
    units: String,
}

#[derive(Serialize, Deserialize)]
struct Structure {
    species: Vec<String>,
    coords: Vec<Vec<f64>>,
    e_diff: f64,
    nacs: Vec<Vec<f64>>,
    norm: f64,
}

fn scale_e_units(energy: f64, units: String) -> f64 {
    if units.eq("hartree") {
        energy * 27.2107
    } else if units.eq("kcal") || units.eq("kcal/mol") {
        energy * 23.0609
    } else {
        energy
    }
}

fn assign_sizes(nstructures: usize, nbins: usize) -> Vec<usize> {
    let mut res = Vec::new();
    let mut c: usize = 0;
    let n: usize = nstructures / nbins as usize;
    for _ in 0..(nbins - 1) {
        res.push(n);
        c = c + n;
    }
    res.push(nstructures - c);
    res
}

fn get_bin(val: f64, nbins: usize) -> usize {
    for i in 0..nbins {
        if val < UPPER_BOUNDS[i] {
            return i;
        }
    }
    return nbins - 1;
}

fn main() {
    let args = Args::parse();
    let units = &args.units.to_lowercase();

    let data = fs::read_to_string(args.file).expect("error with file");
    let json_data: serde_json::Value = serde_json::from_str(&data).expect("invalid JSON");
    let species_data = json_data.get("atom_types").unwrap();
    let coords_data = json_data.get("coords").unwrap();
    let e_diffs_data = json_data.get("energy_differences").unwrap();
    let nacs_data = json_data.get("nacs").unwrap();
    let norms_data = json_data.get("norms").unwrap();
    let total_nstructures = e_diffs_data.as_array().unwrap().len();

    let mut nadded_structures = 0;
    let mut nseen_structures = 0;
    let mut res: Vec<Structure> = Vec::new();
    let max_bin_sizes = assign_sizes(args.nstructures, NBINS);
    let mut cur_bin_sizes: [usize; NBINS] = [0; NBINS];
    while nadded_structures < args.nstructures - 1 && nseen_structures < total_nstructures - 1 {
        let e_diff: f64 = scale_e_units(
            e_diffs_data
                .get(nseen_structures)
                .unwrap()
                .as_f64()
                .unwrap()
                .abs(),
            units.to_string(),
        );
        let bin_idx = get_bin(e_diff, NBINS);
        if cur_bin_sizes[bin_idx] < max_bin_sizes[bin_idx] {
            let species_raw = species_data
                .get(nseen_structures)
                .unwrap()
                .as_array()
                .unwrap();
            let species = species_raw
                .iter()
                .map(|x| x.as_str().unwrap().to_string())
                .collect();
            let coords_raw = coords_data
                .get(nseen_structures)
                .unwrap()
                .as_array()
                .unwrap();
            let coords = coords_raw
                .iter()
                .map(|x| {
                    x.as_array()
                        .unwrap()
                        .iter()
                        .map(|y| y.as_f64().unwrap())
                        .collect::<Vec<f64>>()
                })
                .collect::<Vec<Vec<f64>>>();
            let nacs_raw = nacs_data.get(nseen_structures).unwrap().as_array().unwrap();
            let nacs = nacs_raw
                .iter()
                .map(|x| {
                    x.as_array()
                        .unwrap()
                        .iter()
                        .map(|y| y.as_f64().unwrap())
                        .collect::<Vec<f64>>()
                })
                .collect::<Vec<Vec<f64>>>();
            let norm = norms_data.get(nseen_structures).unwrap().as_f64().unwrap();
            let s = Structure {
                species,
                coords,
                e_diff,
                nacs,
                norm,
            };
            res.push(s);
            cur_bin_sizes[bin_idx] = cur_bin_sizes[bin_idx] + 1;
            nadded_structures = nadded_structures + 1;
            println!(
                "adding to bin #{}; total: {}",
                bin_idx, cur_bin_sizes[bin_idx]
            );
        }
        nseen_structures = nseen_structures + 1;
    }
}

use clap::Parser;
use serde::{Deserialize, Serialize};
use serde_json;
use std::fs;

//const UPPER_BOUNDS: &'static [&'static f64] = &[&0.1, &0.3, &0.7, &1.5, &f64::INFINITY];
//const NBINS: usize = 5;
//const UPPER_BOUNDS: [f64; 5] = [0.1, 0.3, 0.7, 1.5, f64::INFINITY];
//const NBINS: usize = 2;
//const UPPER_BOUNDS: [f64; NBINS] = [0.3, f64::INFINITY];

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    file: String,

    #[arg(short, long, default_value_t = 100)]
    nstructures: usize,

    #[arg(short, long, default_value_t = String::from("hartree"))]
    units: String,

    #[arg(short, long, default_value_t = String::from("out.json"))]
    wf: String,

    #[arg(short, long, default_value_t = String::from("false"))]
    classify: String,

    #[arg(short, long, default_value_t = String::from("e_diff"))]
    classifyby: String,

    #[arg(short, long, default_value_t = 0.3)]
    classifybyvalue: f64,

    #[arg(short, long, default_value_t = 5)]
    nbins: usize,

    #[arg(short, long, default_value_t = String::from("0.1 0.3 0.7 1.5 inf"))]
    upperbounds: String,

    #[arg(short, long, default_value_t = String::from("false"))]
    verbose: String,
}

#[derive(Serialize, Deserialize)]
struct Structure {
    species: Vec<String>,
    coords: Vec<Vec<f64>>,
    e_diff: f64,
    nacs: Vec<Vec<f64>>,
    norm: f64,
    is_like_zero: u8,
}

fn parse_upperbounds(s: String, nbins: usize) -> Result<Vec<f64>, String> {
    fn parse_f64(string: &str) -> f64 {
        if string.to_string() == String::from("inf") {
            f64::INFINITY
        } else {
            string.parse().unwrap()
        }
    }
    let lst: Vec<f64> = s.split_whitespace().map(parse_f64).collect();
    let l = lst.len();
    if l != nbins {
        panic!(
            "number of bins: {} does not match number of upper bounds: {} provided!",
            nbins, l
        );
    }
    Ok(lst)
}

fn scale_e_units(energy: f64, units: String) -> f64 {
    if units.eq("hartree") || units.eq("hartrees") {
        energy * 27.2107
    } else if units.eq("kcal") || units.eq("kcals") || units.eq("kcal/mol") || units.eq("kcals/mol")
    {
        energy * 23.0609
    } else {
        energy
    }
}

fn assign_sizes(nstructures: usize, nbins: usize) -> Vec<usize> {
    let mut res = Vec::<usize>::with_capacity(nbins);
    let mut c: usize = 0;
    let n: usize = nstructures / nbins as usize;
    let mut iter = nbins - 1;
    while iter > 0 {
        res.push(n);
        c += n;
        iter -= 1;
    }
    res.push(nstructures - c);
    res
}

fn get_bin(val: f64, nbins: usize, upperbounds: &Vec<f64>) -> usize {
    for i in 0..nbins {
        if val < upperbounds[i] {
            return i;
        }
    }
    return nbins - 1;
}

fn get_truth_value(string: &str) -> Result<bool, &'static str> {
    match string {
        "true" => Ok(true),
        "t" => Ok(true),
        "false" => Ok(false),
        "f" => Ok(false),
        _ => Err("value `{}` cannot be converted to a boolean"),
    }
}

fn main() {
    let args = Args::parse();
    let mut nbins = args.nbins;
    let mut upperbounds = parse_upperbounds(args.upperbounds, args.nbins).unwrap();
    let is_classify = get_truth_value(&args.classify).unwrap();
    let verbose = get_truth_value(&args.verbose).unwrap();
    if is_classify {
        nbins = 2;
        upperbounds = vec![args.classifybyvalue, f64::INFINITY];
    }

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
    let mut res: Vec<Structure> = Vec::<Structure>::with_capacity(args.nstructures);
    let max_bin_sizes = assign_sizes(args.nstructures, nbins);
    let mut cur_bin_sizes: Vec<usize> = Vec::<usize>::with_capacity(nbins);
    while nadded_structures < args.nstructures && nseen_structures < total_nstructures {
        let e_diff: f64 = e_diffs_data
            .get(nseen_structures)
            .unwrap()
            .as_f64()
            .unwrap();
        let e_diff_ev: f64 = scale_e_units(e_diff.abs(), units.to_string());
        let bin_idx = get_bin(e_diff_ev, nbins, &upperbounds);
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
            let mut is_like_zero = 0;
            if is_classify {
                is_like_zero = (e_diff < 0.3) as u8;
            }
            let s = Structure {
                species,
                coords,
                e_diff,
                nacs,
                norm,
                is_like_zero,
            };
            res.push(s);
            cur_bin_sizes[bin_idx] += 1;
            nadded_structures = nadded_structures + 1;
            if verbose {
                println!(
                    "adding to bin #{}; total: {}",
                    bin_idx, cur_bin_sizes[bin_idx]
                );
            }
        }
        nseen_structures = nseen_structures + 1;
    }

    let json = serde_json::to_string(&res).unwrap();
    fs::write(args.wf, json).unwrap();
}

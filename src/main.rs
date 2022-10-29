use serde::{Deserialize, Serialize};
use serde_json;
use std::fs;

//const UPPER_BOUNDS: &'static [&'static f64] = &[&0.1, &0.3, &0.7, &1.5, &f64::INFINITY];
const UPPER_BOUNDS: [f64; 5] = [0.1, 0.3, 0.7, 1.5, f64::INFINITY];
const NBINS: usize = UPPER_BOUNDS.len();
const NSTRUCTURES: usize = 1000;
const NATOMS: usize = 6;

#[derive(Serialize, Deserialize, Clone, Copy)]
struct Structure {
    species: [char; NATOMS],
    coords: [[f64; 3]; NATOMS],
    e_diff: f64,
    nacs: [[f64; 3]; NATOMS],
    norm: f64,
}

fn assign_sizes() -> [usize; NBINS] {
    let mut res: [usize; NBINS] = [0; NBINS];
    let mut c: usize = 0;
    let n: usize = NSTRUCTURES / NBINS as usize;
    for i in 0..(NBINS - 1) {
        res[i] = n;
        c = c + n;
    }
    res[NBINS - 1] = NSTRUCTURES - c;
    res
}

fn get_bin(val: f64) -> usize {
    for i in 0..NBINS {
        if val < UPPER_BOUNDS[i] {
            return i;
        }
    }
    return NBINS - 1;
}

fn main() {
    let data = fs::read_to_string("../sample.json").expect("error with file");
    let json_data: serde_json::Value = serde_json::from_str(&data).expect("invalid JSON");
    let species = json_data.get("atom_types").unwrap();
    let coords = json_data.get("coords").unwrap();
    let e_diffs = json_data.get("energy_differences").unwrap();
    let nacs = json_data.get("nacs").unwrap();
    let norms = json_data.get("norms").unwrap();

    let mut cur_nstructures = 0;
    let mut res: [Structure; NSTRUCTURES] = [Structure {
        species: ['a'; NATOMS],
        coords: [[0.0; 3]; NATOMS],
        e_diff: 0.0,
        nacs: [[0.0; 3]; NATOMS],
        norm: 0.0,
    }; NSTRUCTURES];
    let max_bin_sizes = assign_sizes();
    let mut cur_bin_sizes: [usize; NBINS] = [0; NBINS];
    // TODO: early termination
    while cur_nstructures < NSTRUCTURES {
        let e_diff: f64 = e_diffs.get(cur_nstructures).unwrap().as_f64().unwrap();
        let bin_idx = get_bin(e_diff);
        if cur_bin_sizes[bin_idx] < max_bin_sizes[bin_idx] {
            println!(
                "adding to bin #{}; total: {}",
                bin_idx, cur_bin_sizes[bin_idx]
            );
            //let s = Structure {
            //species: species.get(cur_nstructures).unwrap(),
            //coords: coords.get(cur_nstructures).unwrap(),
            //e_diff: e_diffs.get(cur_nstructures).unwrap(),
            //nacs: nacs.get(cur_nstructures).unwrap(),
            //norm: norms.get(cur_nstructures).unwrap(),
            //};
            //res[cur_nstructures] = s;
            cur_bin_sizes[bin_idx] = cur_bin_sizes[bin_idx] + 1;
            cur_nstructures = cur_nstructures + 1;
        }
        //println!(s.to_string());
    }
}

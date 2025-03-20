// TODO
// Docstrings
// Maybe refactor so it can be tested? Make tests work

// Other things
// src/concatenate and src/create fasta should not need to load vamb

// Requires a FASTA parser in Rust, w. sequence validation and
// OPTIONAL name validation (concat may rename)

// Also gzip de/compressor

use numpy::{PyReadwriteArray1, PyReadwriteArray2};
use pyo3::prelude::*;

const fn make_lut() -> [u8; 256] {
    let mut lut = [4u8; 256];
    let mut i: usize = 0;
    while i < 128 {
        match i as u8 {
            b'A' | b'a' => lut[i] = 0,
            b'C' | b'c' => lut[i] = 1,
            b'G' | b'g' => lut[i] = 2,
            b'T' | b't' => lut[i] = 3,
            _ => (),
        };
        i += 1;
    }
    lut
}

const LUT: [u8; 256] = make_lut();

#[pyfunction]
fn kmercounts(mut counts: PyReadwriteArray1<u32>, bytes: Vec<u8>, k: u8) {
    if k == 0 || k > 7 {
        panic!("k must be between 1 and 7");
    }

    let mut kmer = 0u32;
    let mut countdown = k - 1;
    let mask = (1u32 << (2 * k)) - 1;
    let counts_slice = counts.as_slice_mut().unwrap();

    if counts_slice.len() != 1 << (2 * k) {
        panic!("Counts array has wrong length");
    }

    for &byte in bytes.as_slice() {
        // Safety: A u8 cannot be out of bounds for a length 256 array
        let &val = unsafe { LUT.get_unchecked(byte as usize) };
        if val == 4 {
            countdown = k;
        }

        kmer = ((kmer << 2) | (val as u32)) & mask;

        if countdown == 0 {
            // Safety: We just masked the lower 2k bits, so kmer is in the range 0..2^2k
            unsafe {
                *counts_slice.get_unchecked_mut(kmer as usize) += 1;
            }
        } else {
            countdown -= 1;
        }
    }
}

struct ContiguousTrueRanges<'a> {
    mask: &'a [bool],
    pos: usize,
}

impl<'a> ContiguousTrueRanges<'a> {
    fn new(mask: &'a [bool]) -> Self {
        Self { mask, pos: 0 }
    }
}

impl Iterator for ContiguousTrueRanges<'_> {
    type Item = std::ops::Range<usize>;

    fn next(&mut self) -> Option<Self::Item> {
        let len = self.mask.len();

        if self.pos >= len {
            return None;
        }

        // Find next true
        let n_until_start = match self.mask[self.pos..].iter().position(|x| *x) {
            Some(i) => i,
            None => {
                self.pos = len;
                return None;
            }
        };

        // Find next false
        let end: usize = match self.mask[self.pos + n_until_start + 1..]
            .iter()
            .position(|x| !*x)
        {
            Some(i) => i,
            None => {
                let res = self.pos + n_until_start..len;
                self.pos = len;
                return Some(res);
            }
        };

        let span = self.pos + n_until_start..self.pos + n_until_start + end + 1;
        self.pos = span.end + 1;
        Some(span)
    }
}

// Add a test for ContiguousTrueRanges
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_contiguous_true_ranges() {
        let mask = vec![false, true, true, false, false, true, true, true, false];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![1..3, 5..8]);

        let mask = vec![false, true, true, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![1..4]);

        let mask = vec![true, true, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![0..3]);

        let mask = vec![false, false, false];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![]);

        let mask = vec![true, false, true, false, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![0..1, 2..3, 4..5]);
    }
}

#[pyfunction]
fn overwrite_matrix(mut matrix: PyReadwriteArray2<f32>, mask: PyReadwriteArray1<bool>) -> usize {
    let nrow = matrix.as_array().shape()[0];
    let ncol = matrix.as_array().shape()[1];

    let mask_slice = mask.as_slice().unwrap();

    if nrow != mask_slice.len() {
        panic!("Matrix and mask must have the same number of rows");
    }

    let matrix = matrix.as_slice_mut().unwrap();
    let mut write_row_index: usize = 0;

    for range in ContiguousTrueRanges::new(mask.as_slice().unwrap()) {
        // If range.start is 0, then it copies into its own position needlessly
        if range.start != 0 {
            // Range here is all wrong
            matrix.copy_within(range.start * ncol..range.end * ncol, write_row_index * ncol);
        }
        write_row_index += range.len();
    }

    write_row_index
}

/// A Python module implemented in Rust.
#[pymodule]
fn vambcore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kmercounts, m)?)?;
    m.add_function(wrap_pyfunction!(overwrite_matrix, m)?)?;
    Ok(())
}

# Truth-Table Quotients Do Not Close One-Tape MCSP Magnification: Small Fibers, Exact Cosets, and a Defect-Inflation Dichotomy

[![verify](https://github.com/Li-Hongmin/one-tape-mcsp-truth-table-quotients/actions/workflows/verify.yml/badge.svg)](https://github.com/Li-Hongmin/one-tape-mcsp-truth-table-quotients/actions/workflows/verify.yml) [![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.24054917-blue)](https://doi.org/10.5281/zenodo.24054917)

**Hongmin Li** (Institute of Science Tokyo; The University of Tokyo) · ORCID [0000-0003-0228-0600](https://orcid.org/0000-0003-0228-0600)

Main result of the manuscript: counting and additive-combinatorial barriers show that truth-table quotients (small fibres, exact cosets, defect inflation) cannot transfer known one-tape MCSP lower bounds to the small thresholds required by hardness magnification.

- Manuscript on rStation: <https://rstation.ai/problems/p_vs_np/papers/1/v1> (version 1)
- Archived on Zenodo: concept DOI [10.5281/zenodo.24054917](https://doi.org/10.5281/zenodo.24054917) (all versions); this repository mirrors version 1, DOI [10.5281/zenodo.24054918](https://doi.org/10.5281/zenodo.24054918)

## Contents

- `paper/paper.md`, `paper/one-tape-mcsp-truth-table-quotients.pdf` — the manuscript (version 1).
- `verification/` — the supplement of that version, unpacked unchanged; its own README describes each file.
- `.github/workflows/verify.yml` — reruns every check below on each push.

## What the programs check

| Check | Command (run inside `verification/`) |
|---|---|
| Exhaustive checks on tiny parameters | `python checks.py` |

The programs check the finite and exact computations used in the manuscript; the mathematical arguments are those written in the paper.

## Reproducing

```sh
cd verification
python checks.py
```

Requirements: Python 3.9+. Run the commands from a copy if you want to keep the recorded outputs untouched.

## Cite

```bibtex
@misc{li2026onetapemcsptruthtablequo,
  author    = {Li, Hongmin},
  title     = {Truth-Table Quotients Do Not Close One-Tape MCSP Magnification: Small Fibers, Exact Cosets, and a Defect-Inflation Dichotomy},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24054917},
  url       = {https://doi.org/10.5281/zenodo.24054917}
}
```

## License

Manuscript and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT (see `LICENSE`).

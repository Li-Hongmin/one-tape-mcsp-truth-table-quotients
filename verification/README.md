# Supplement: finite sanity checks

`checks.py` (Python 3, standard library only; runs in under a second) exhaustively checks, on tiny parameters:

- exact circuit complexity (fan-in-2 AND/OR, NOT, size = number of gates incl. NOT) of all 2-variable functions and of all 3-variable functions of size at most 5;
- point-indicator cost at most 2n-1 and point-flip cost at most CC(f)+2n+3;
- Harper's vertex-isoperimetric theorem on the 4-cube over all subsets, and its iterated form |A+B_j| >= |I_j| for A = L_t (n=3, truth-table cube of dimension 8), including that closed neighbourhoods of simplicial initial segments are initial segments;
- the downset upward-edge identity used in (39);
- the coset-quotient bound |A+A|/|A| <= m (52), and that 2^{dim Stab} divides |L_t|;
- the factorization (58), the counting bound (59) and inequality (55) for random maps Q on A = L_t, and exactness of (55) for the two-label predicate map;
- the Q_0 example (N=6) and the tensor/dummy-padding identities (3o), (7).

Expected output: `1048 checks passed`.

These are numerical sanity checks on small cases, not proofs of the asymptotic statements in the paper.

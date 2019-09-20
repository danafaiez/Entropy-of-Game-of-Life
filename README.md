**About this repository**



This repository includes multiple optimization codes:

* [min.c](https://github.com/danafaiez/optimization-/blob/test/min.c) includes a minimization process using GSL library which minimizes the
observational entropy with position and energy coarse graining, S_EX, with respect to the phase factor phi = E_{i}t.
It also includes minimization of the entanglement entropy, S_ent, between two partitions of the system, with respect to the phase factor phi = E_{i}t.
The expectation value of the number operator, is also calculated at the end of this optimization process.


* [max_region_prob.c](https://github.com/danafaiez/optimization-/blob/test/max_region_prob.c) maximizes the probability that the wavefunction in localized
within specific lattice sites. This optimization is done using GSL library and the maximization is with respect
to the phase factor phi = E_{i}t. The expectation value of the number operator, is also calculated at the end of this optimization process.


* [S_min_minimum.c](https://github.com/danafaiez/optimization-/blob/test/S_min_minimum.c) is a minimization process
similar to min_S_EX of S_EX, but with a starting phase that corresponds to a local minimum (calculated from doing a minimization).

**Current bugs**

[S_min_minimum.c](https://github.com/danafaiez/optimization-/blob/test/S_min_minimum.c) currently has some bugs that I ahven't been able to resolve.

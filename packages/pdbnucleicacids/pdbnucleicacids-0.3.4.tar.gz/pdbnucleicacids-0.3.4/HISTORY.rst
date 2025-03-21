=======
History
=======


0.3.4 (2025-03-14)
------------------

* New __repr__ for DSNA
* New gitlab CI pipeline
    * Automatic release in gitlab packages and PyPI
    * Job rules that don't waste machine minutes
    * Use virtualenv caching correctly
* Remove pyup badge


0.3.3 (2025-03-10)
------------------

* Fix: while parsing nucleotides with only backbone or
  part of it, it raised errors since they don't have the base atoms


0.3.2 (2025-03-10)
------------------

* Fix: new algorithm for building double stranded nucleic acids
  which better addresses many interruptions in the double strands


0.3.1 (2025-03-9)
------------------

* Fix: new algorithm for building nucleic acids (starting from the 5' end) is more accurate
* Fix: base-pairs can be in the same chain
* Fix: looser radius for building nucelic acids,
  or else structures like 10MH would have one nucleotide by itself
* Remove old code like MMCIF2DataFrame and utils


0.3.0 (2025-03-4)
------------------

* New base-pairing rules, address DNA and
* Generic class that enables own rules to be coded


0.2.1
------------------

* Building and deploying docs on readthedocs.


0.2.0
------------------

* NABuilder, DSNABuilder, NucleicAcid and DoubleStrandNucleicAcid classes.


0.1.0 (2024-09-18)
------------------

* First release on PyPI.

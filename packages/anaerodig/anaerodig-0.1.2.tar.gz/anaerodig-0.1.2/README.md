The anaerodig package is designed for Anaerobic Digestion modelling.
It contains:
- Abstract Base Classes to structure new AD models
- An implementation of ADM1 model (Batstone et al. 2002)
- An implementation of AM2 model (Bernard et al. 2001)
Both these implementations rely on JIT compilation for efficient simulations

The implementation of ADM1 relies on the PyADM1 module (see license below). It has been extensively revised to rely on structured classes rather than scripts.
The implementation of AM2 is original.

The package was written while the author conducted his PhD at Universite de Lille, with financial support from SUEZ.

NOTE: This package needs to be thoroughly tested before further use! If you notice any odd behavior, do not hesitate to report the issue.

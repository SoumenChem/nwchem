#!/bin/bash -f
# source env. variables
 source $TRAVIS_BUILD_DIR/travis/nwchem.bashrc
 nprocs=2
 if [[ "$ARMCI_NETWORK" == "MPI-PR" ]]; then
   nprocs=3
 fi
 if [[ "$NWCHEM_MODULES" == "tce" ]]; then
   cd $NWCHEM_TOP/QA && USE_SLEEPLOOP=1 ./runtests.mpi.unix procs $nprocs tce_n2 tce_ccsd_t_h2o tce_h2o_eomcc
   cd $NWCHEM_TOP/QA && USE_SLEEPLOOP=1 ./runtests.mpi.unix procs $nprocs tce_ipccsd_f2 tce_eaccsd_ozone
 else
   cd $NWCHEM_TOP/QA && ./runtests.mpi.unix procs $nprocs dft_he2+ 
   cd $NWCHEM_TOP/QA && USE_SLEEPLOOP=1 ./runtests.mpi.unix procs $nprocs h2o_opt cosmo_h2o_dft tddft_h2o h2o2-response
   cd $NWCHEM_TOP/QA && USE_SLEEPLOOP=1 ./runtests.mpi.unix procs $nprocs dft_siosi3
   cd $NWCHEM_TOP/QA && USE_SLEEPLOOP=1 ./runtests.mpi.unix procs $nprocs pspw pspw_md
 fi

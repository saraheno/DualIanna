
# First time only (only on UMD cluster)

git clone https://github.com/UVa-Calvision/dd4hep-rivanna.git

cd dd4hep-rivanna/

cd container/

source ./build.sh


# Always


conda deactivate  (if you are on the U. Maryland cluster)

apptainer shell -B /cvmfs:/cvmfs -B /data:/data ~eno/apptainer/alma9.sif  (on UMD cluster)

source /cvmfs/sw.hsf.org/key4hep/setup.sh


# again only the first time

export NUMBER_OF_JOBS=16


mkdir -p install

git clone -b dual_crys_calo_digi git@github.com:saraheno/k4RecCalorimeter.git

mkdir -p k4RecCalorimeter/build

cmake -S k4RecCalorimeter/ -B k4RecCalorimeter/build/ -D CMAKE_INSTALL_PREFIX=$PWD/install

cmake --build k4RecCalorimeter/build --parallel ${NUMBER_OF_JOBS}

cmake --install k4RecCalorimeter/build

cd k4RecCalorimeter

k4_local_repo $PWD/../install

cd ..

git clone git@github.com:saraheno/DualIanna.git || echo "Already exists"

mkdir -p DualIanna/build

cmake -S DualIanna -B DualIanna/build -D CMAKE_INSTALL_PREFIX=$PWD/install -D CMAKE_PREFIX_PATH=$PWD/install

cmake --build DualIanna/build --parallel ${NUMBER_OF_JOBS}

cmake --install DualIanna/build


# every time

(from the mother area)

source install/bin/thisDualIanna.sh

export PYTHONPATH=$PWD/install/python:$PYTHONPATH

# to make events


cd DualIanna/compact

```
 ddsim --compactFile=DRConly.xml --runType=batch -G --steeringFile SCEPCALsteering.py --outputFile=junk.root --part.userParticleHandler= -G --gun.position="0. 0.*mm -80*cm" --gun.direction "0. 0. 1." --gun.energy "20*GeV" --gun.particle="pi-" -N 1
```

# to digitize

cd DualIanna/compact

k4run digi_dualcrys.py -IOSvc.Input junk.root -IOSvc.Output yuck.root -n 2

maybe --CaloDigitizaerFunc.signalFileName

# just saving this.  ignore

git clone git@github.com:saraheno/DualIanna.git

git clone -b dual_crys_calo_digi git@github.com:saraheno/k4RecCalorimeter.git

cd k4RecCalorimeter

mkdir build install

cd build 

cmake -DCMAKE_INSTALL_PREFIX=../install ..

make -j8 install 


cd ../../DualIanna

mkdir build install

cd build

cmake -DDD4HEP_USE_GEANT4=ON -DBoost_NO_BOOST_CMAKE=ON -DDD4HEP_USE_LCIO=ON -DROOT_DIR=$ROOTSYS -D CMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install -D DD4HEP_USE_EDM4HEP=ON -DBoost_USE_DEBUG_RUNTIME=OFF ..



make -j8 install

cd ../../k4RecCalorimeter

k4_local_repo $PWD/../install

cd ../DualIanna

source ./install/bin/thisDualIanna.sh



# old documentation

This is a simulation of a dual readout crystal calorimeter (currently the code is work in progress).
See https://iopscience.iop.org/article/10.1088/1748-0221/15/11/P11005 for the concept.

## If you are not on alma9-like OS, but can use singularity
```
singularity run -B /cvmfs:/cvmfs -B /data:/data docker://gitlab-registry.cern.ch/sft/docker/alma9-core:latest
# at Baylor
# singularity run -B /cvmfs:/cvmfs -B /cms/data:/cms/data docker://gitlab-registry.cern.ch/sft/docker/alma9-core:latest
```

## All times:
```
source /cvmfs/sft.cern.ch/lcg/views/LCG_107/x86_64-el9-gcc14-opt/setup.sh
```

## First time only:
```
# setup directory
mkdir stuff4stuff
cd stuff4stuff

# git clone, compile, install
git clone ssh://git@gitlab.cern.ch:7999/calvisionsimulation/DualTestBeam.git
# or try sarah's version
# git clone git@github.com:saraheno/DualTestBeam.git
cd DualTestBeam
mkdir build
mkdir install
cd build

cmake -DDD4HEP_USE_GEANT4=ON -DBoost_NO_BOOST_CMAKE=ON -DDD4HEP_USE_LCIO=ON  -DROOT_DIR=$ROOTSYS -D CMAKE_BUILD_TYPE=Release  -DCMAKE_INSTALL_PREFIX=../install ..

# maybe at Baylor?
cmake -DDD4HEP_USE_GEANT4=ON -DBoost_NO_BOOST_CMAKE=ON -DDD4HEP_USE_LCIO=ON -DROOT_DIR=$ROOTSYS -D CMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install -D DD4HEP_USE_EDM4HEP=ON ..



make -j4
make install
```

## All times
```
cd to stuff4stuff/DualTestBeam
source ./install/bin/thisDualTestBeam.sh
cd compact
```

## running in batch mode

Look in [massjobs.py](https://gitlab.cern.ch/calvisionsimulation/DualTestBeam/-/blob/master/compact/massjobs.py) to see how to run it
to analyze the output, look at [massjobs_s2.py](https://gitlab.cern.ch/calvisionsimulation/DualTestBeam/-/blob/master/compact/massjobs_s2.py).
For Baylor users, see [massjobs_pbsarray.py](https://gitlab.cern.ch/calvisionsimulation/DualTestBeam/-/blob/master/compact/massjobs_pbsarray.py)

or see examples in CI (continuous integration) yaml file for running `ddsim` and `Resolution.C` in
[.gitlab-ci.yml](https://gitlab.cern.ch/calvisionsimulation/DualTestBeam/-/blob/master/.gitlab-ci.yml)

## running interactively
Change `--runType=batc` above to `--runType=vis`.
Then
```
/control/execute vis.mac
/run/beamOn 1
```
On the window that pops up, choose “Miscellany” and “Exit to G4Vis >”
Then do typical GEANT4 visualization commands such as:
```
/vis/viewer/refresh
/vis/viewer/zoomTo 10
/vis/viewer/pan -100 200 cm
exit
```

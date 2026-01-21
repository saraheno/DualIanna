

# Always


singularity run -B /cvmfs:/cvmfs -B /data:/data docker://gitlab-registry.cern.ch/sft/docker/alma9-core:latest


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
 ddsim --compactFile=DRConly.xml --runType=qt -G --steeringFile SCEPCALsteering.py --outputFile=junk.root --part.userParticleHandler= -G --gun.position="0. 0.*mm -80*cm" --gun.direction "0. 0. 1." --gun.energy "20*GeV" --gun.particle="pi-" 
```

the useful commands are /control/execute visqT.mac

# to digitize

cd DualIanna/compact

k4run digi_dualcrys.py 

maybe --CaloDigitizaerFunc.signalFileName

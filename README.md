
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

k4run make_digis.py # <-- this will process the root file -> digis



# To convert to a simple ROOT tree 
```bash
	python convert_to_simple_tree.py -f edm4hep_output.root -o waves.root 
```


# Other Notes


EDM4Hep -- Part of the key4Hep project 
Provides an event data model (A bunch of different classes used for structuring and describing physics detector event data / simulation data )

https://github.com/key4hep/EDM4hep



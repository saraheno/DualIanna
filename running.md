Rough running notes for k4RecCalorimeter and DualIanna
3 Repositories 

If you haven't already, create an alma9 container following the instructions from 
https://github.com/UVa-Calvision/dd4hep-rivanna

Everything below needs to get run inside of that container 


k4RecCalorimeter -- Key4Hep Codebase for processing EDM4Hep Root files -> Digis
***Build This First***

https://github.com/saraheno/k4RecCalorimeter

```bash
> git clone https://github.com/saraheno/k4RecCalorimeter
> cd k4RecCalorimeter
> git checkout dual_crys_calo_digi_experimental
> mkdir build
> mkdir install
# If you haven't already make sure to source /cvmfs/sw.hsf.org/key4hep/setup.sh
> cd build
> cmake -DCMAKE_INSTALL_PREFIX=../install ..
> make -j4
> make install
> k4_local_repo

```


DualIanna -- DD4hep simulation
(experimental branch)
https://github.com/saraheno/DualIanna

```bash
> git clone https://github.com/saraheno/DualIanna
> cd DualIanna
> git checkout experimental
> mkdir build
> mkdir install 
> source /cvmfs/sw.hsf.org/key4hep/setup.sh
> cd build
> cmake ..  -D CMAKE_INSTALL_PREFIX=../install -D CMAKE_PREFIX_PATH=../install
> make 
> make install
> cd ..
> source ./install/bin/thisDualIanna.sh 
```

```bash
#Dual Ianna Tree Structure (Removed some extraneous files for clarity)
├── CMakeLists.txt
├── compact
│   ├── digi_dualcrys.py 
│   ├── digi_process.py # Post digi creation toy processor 
│   ├── digi_test.py # Digi Processor 
│   ├── DRBigEcal1.xml
│   ├── DRBigEcal2.xml
│   ├── DRConly.xml # Top Level Geometry XML File for Single Crystal
│   ├── DRDualSampHcal.xml
│   ├── DRDualTestBeam.xml
│   ├── DRFIDEAonly.xml
│   ├── DRFSCEPLAonly.xml
│   ├── DRFSCEPNQonly.xml
│   ├── DRFSCEPonly.xml
│   ├── DRFSCEPSAonly.xml
│   ├── DRJunk.xml
│   ├── DRSampOnly2.xml
│   ├── DRSampOnly.xml
│   ├── DRSingleCrystalCosmicRay.xml
│   ├── materials.xml # cellID and material definitions
│   ├── Overlay3.C
│   ├── README.md
│   ├── Resolution.C
│   ├── SCEPCAL_BOUND.xml # Top Level world boundary visualization
│   ├── SCEPCALConstants2.xml
│   ├── SCEPCALConstants3.xml
│   ├── SCEPCALConstants4.xml
│   ├── SCEPCALConstantsBigEcalR2.xml
│   ├── SCEPCALConstantsBigEcalR3.xml
│   ├── SCEPCALConstantsBigEcalR.xml
│   ├── SCEPCALConstantsBigEcal.xml
│   ├── SCEPCALConstantsBiggerEcal.xml
│   ├── SCEPCALConstantsJunk.xml
│   ├── SCEPCALConstantsS2.xml
│   ├── SCEPCALConstantsS3.xml
│   ├── SCEPCALConstants.xml
│   ├── SCEPCAL_DRCrystal-twoseg.xml
│   ├── SCEPCAL_DRCrystal.xml # Crystal Tower Geometry Definition
│   ├── SCEPCAL_DRFiber2.xml
│   ├── SCEPCAL_DRFiber.xml
│   ├── SCEPCAL_DRSampling2.xml
│   ├── SCEPCAL_DRSampling.xml
│   ├── SCEPCAL_DRUpstream.xml
│   ├── SCEPCAL_ECAL.xml # Visualization Attributes
│   ├── SCEPCAL_EdgeDet.xml # Top Level World Boundaries 
│   ├── SCEPCALelements.xml
│   ├── SCEPCAL_HCAL2.xml
│   ├── SCEPCAL_HCALSamp2.xml
│   ├── SCEPCAL_HCALSamp.xml
│   ├── SCEPCAL_HCAL.xml
│   ├── SCEPCAL_hugeECAL.xml
│   ├── SCEPCAL_Materials.xml
│   ├── SCEPCALsteering_edm.py # edm4hep dd4hep steering file
│   ├── SCEPCALsteering_nocher.py
│   ├── SCEPCALsteering.py # original dd4hep steering file
│   ├── SCEPCAL_Upstream.xml
│   ├── vis2.mac
│   ├── vis3.mac
│   ├── vis4.mac
│   ├── vis5.mac
│   └── vis.mac
├── data
│   └── README.md
├── eve
│   └── README.md
├── include
│   ├── DBParameters.h
│   ├── README.md
│   └── SCEGeant4Output2ROOT.h
├── lib
│   └── G__DualIanna_rdict.pcm
├── README.md
├── scripts
│   └── README.md
└── src
    ├── CVGeant4Output2EDM4hep.cpp # G4Event -> EDM4Hep Output
    ├── DRCrys_geo.cpp # Crystal Geometry Implementation
    ├── DRFiber_geo.cpp
    ├── DRFtubeFiber_geo.cpp
    ├── DRSamp_geo.cpp
    ├── DRUpstream_geo.cpp
    ├── DualCrysCalorimeterDump.cpp
    ├── DualCrysCalorimeterSDAction.cpp
    ├── EdgeDet_geo.cpp
    └── SCEGeant4Output2ROOT.cpp
```


Assuming everything above worked, let's run a simple simulation 

Note: Before running ddsim 

```shell 
> cd DualIanna/compact
> ddsim --compactFile=DRConly.xml --runType=batch -G --steeringFile SCEPCALsteering_edm.py --outputFile=junk.edm4hep.root --part.userParticleHandler= -G --gun.position="0. 0.*mm -80*cm" --gun.direction "0. 0. 1." --gun.energy "20*GeV" --gun.particle="e-" -N20
# now we wait ...
# if it works we'll have an output file labeled junk.edm4hep.root
> k4run digi_test.py # <-- this will process the root file -> digis
```


EDM4Hep -- Part of the key4Hep project 
Provides an event data model (A bunch of different classes used for structuring and describing physics detector event data / simulation data )

https://github.com/key4hep/EDM4hep

The downside I've found is that it makes working with ROOT files more complicated 

You cannot do something like tree->Print() and using the description create data bindings for reading from ROOT. Or at least it does not work in a straightforward manner. You have to go through their interface. 

Python Example digi_process.py 
```bash 
> python digi_process.py -f edm4hep_output.root -o plots.root 
```
Converts the digi waveforms into a structure a bit easier to use in ROOT 
Where you have an event, xs and ys 

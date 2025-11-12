from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import k4DataSvc
dataservice = k4DataSvc("EventDataSvc", input="junk.edm4hep.root")



from Configurables import PodioInput

## The collections refer to collections we want to read
# under the events tree in the root file (I think)
podioinput = PodioInput("PodioInput",
    collections = [
        "MCParticles",
        "DRCNoSegment",
        "EventHeader",
        "DRCNoSegmentContributions"
    ],
    OutputLevel = DEBUG
)

from Configurables import DualCrysSiPMAlgo
## This algorithm will read a filtered list of photons and produce
## digi outputs 
sipmAlgo = DualCrysSiPMAlgo("Calvision SiPM Algo")


## The first part of digis, this will filter out Cherenkov and Scint. Photons
## from the DRCNoSegment collection
from Configurables import DualCrysCalDigi
digi = DualCrysCalDigi("DualCrystalDigis")
digi.CALCollection = ["DRCNoSegment"]
digi.outputCalCollection = "DigitizedCaloHits"

#digi.setProp('EncodingStringParameterName', 'id')
#digi.CalThreshold = 0.03  # MeV
#digi.maxCalHitEnergy = 2.0
digi.OutputLevel = DEBUG


## What we plan on writing (in this case everything) 
from Configurables import PodioOutput
podiooutput = PodioOutput("PodioOutput", filename = "edm4hep_output.root", OutputLevel = DEBUG)
podiooutput.outputCommands = ["keep *"]



## Random # engine 
from Configurables import HepRndm__Engine_CLHEP__RanluxEngine_ as RndmEngine
rndmEngine = RndmEngine('RndmGenSvc.Engine',
  SetSingleton = True,
  Seeds = [ 2345678 ] # default seed is 1234567
)

from Configurables import RndmGenSvc
rndmGenSvc = RndmGenSvc("RndmGenSvc",
  Engine = rndmEngine.name()
)

## The operations (and unsure, possibly order) we plan on performing 

ApplicationMgr(
    TopAlg = [
        podioinput,
        digi,
        sipmAlgo,
        podiooutput
    ],
    EvtSel = 'NONE',
    EvtMax = 20,
    ExtSvc = [rndmEngine,rndmGenSvc,dataservice]
)
 

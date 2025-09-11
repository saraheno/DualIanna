from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import k4DataSvc
dataservice = k4DataSvc("EventDataSvc", input="junk.root")

from Configurables import PodioInput
podioinput = PodioInput("PodioInput",
    collections = [
        "SimCaloHits"
    ],
    OutputLevel = DEBUG
)

from Configurables import DualCrysCalDigi

digi = DualCrysCalDigi("DualCrystalDigitizer")
digi.calCollections = "SimCaloHits"
digi.outputCalCollection = "DigitizedCaloHits"
digi.outputRelCollection = "CaloHitLinks"
digi.CalThreshold = 0.03  # MeV
digi.maxCalHitEnergy = 2.0

# Then include this in your ApplicationMgr.TopAlg or ComponentAccumulator if you're using GaudiConfig2
from Configurables import PodioOutput
podiooutput = PodioOutput("PodioOutput", filename = "./yuckyuckyuck_digi.root", OutputLevel = DEBUG)
podiooutput.outputCommands = ["keep *"]

from Configurables import HepRndm__Engine_CLHEP__RanluxEngine_ as RndmEngine
rndmEngine = RndmEngine('RndmGenSvc.Engine',
  SetSingleton = True,
  Seeds = [ 2345678 ] # default seed is 1234567
)

from Configurables import RndmGenSvc
rndmGenSvc = RndmGenSvc("RndmGenSvc",
  Engine = rndmEngine.name()
)


ApplicationMgr(
    TopAlg = [
        podioinput,
        DualCrysCalDigi,
        podiooutput
    ],
    EvtSel = 'NONE',
    EvtMax = 10,
    ExtSvc = [rndmEngine,rndmGenSvc,dataservice]
)

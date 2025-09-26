from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import k4DataSvc
dataservice = k4DataSvc("EventDataSvc", input="junk.edm4hep.root")



from Configurables import PodioInput
podioinput = PodioInput("PodioInput",
    collections = [
        "MCParticles",
        "DRCNoSegment",
        "EventHeader",
        "DRCNoSegmentContributions"
    ],
    OutputLevel = DEBUG
)


from Configurables import DualCrysCalDigi
digi = DualCrysCalDigi("DualCrystalDigis")
digi.CALCollection = ["DRCNoSegment"]
digi.outputCalCollection = "DigitizedCaloHits"
digi.outputRelCollection = "CaloHitLinks"
#digi.setProp('EncodingStringParameterName', 'id')
digi.CalThreshold = 0.03  # MeV
digi.maxCalHitEnergy = 2.0
digi.OutputLevel = DEBUG

from Configurables import PodioOutput
podiooutput = PodioOutput("PodioOutput", filename = "edm4hep_output.root", OutputLevel = DEBUG)
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
        digi,
        podiooutput
    ],
    EvtSel = 'NONE',
    EvtMax = 10,
    ExtSvc = [rndmEngine,rndmGenSvc,dataservice]
)

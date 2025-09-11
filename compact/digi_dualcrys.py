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

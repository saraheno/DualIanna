from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import k4DataSvc

# follow example to add custom args from: https://github.com/key4hep/K4FWCore
from k4FWCore.parseArgs import parser
parser.add_argument('-f','--file', type=str, default = 'junk.edm4hep.root')
parser.add_argument('-o','--output', type=str, default = 'edm4hep_output.root')
parser.add_argument('--filter', type=str, choices = ['u330', 'o58', 'none'], default = 'none')
my_opts = parser.parse_known_args()
print(my_opts)

dataservice = k4DataSvc("EventDataSvc", input=my_opts[0].file)


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
# default no filter 
if my_opts[0].filter == 'u330':
    sipmAlgo.U330 = True
elif my_opts[0].filter == 'o58':
    sipmAlgo.O58 = True



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
podiooutput = PodioOutput("PodioOutput", filename = my_opts[0].output, OutputLevel = DEBUG)
podiooutput.outputCommands = ["drop *",
                              "keep CalvisionSiPMDigiWaveform",
                              "keep CalvisionSiPMScintWaveform",
                              "keep CalvisionSiPMCerenWaveform",
                              "keep killedCherenPhotons",
                              "keep killedScintPhotons",
                              "keep passedScintPhotons",
                              "keep passedCherenPhotons",
                              "keep EventHeader"]



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
    EvtMax = 200,
    ExtSvc = [rndmEngine,rndmGenSvc,dataservice]
)
 

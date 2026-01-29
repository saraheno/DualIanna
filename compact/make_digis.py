from Gaudi.Configuration import *
from k4FWCore import ApplicationMgr

#from Configurables import k4DataSvc

# follow example to add custom args from: https://github.com/key4hep/K4FWCore
from k4FWCore.parseArgs import parser
parser.add_argument('-f','--file', type=str, default = 'junk.edm4hep.root')
parser.add_argument('-o','--output', type=str, default = 'edm4hep_output.root')
parser.add_argument('--filter', type=str, choices = ['u330', 'o58', 'none'], default = 'none')
parser.add_argument('-d', '--algo', type=str, choices = ['simsipm', 'sasha'], default = 'sasha',
                    help = 'Algorithm to use for digi construction. Sasha is our signal model')
my_opts = parser.parse_known_args()
print(my_opts)

from k4FWCore import IOSvc
io_svc = IOSvc("IOSvc") # or just IOSvc() as "IOSvc" name is used by default
io_svc.Input=my_opts[0].file
io_svc.CollectionNames = [        "MCParticles",
        "DRCNoSegment",
        "EventHeader",
        "DRCNoSegmentContributions"
        ]

io_svc.Output=my_opts[0].output
io_svc.OutputType="RNTuple"
io_svc.outputCommands=["drop *",
                              "keep CalvisionSiPMDigiWaveform",
                               "keep CalvisionSiPMScintWaveform",
                               "keep CalvisionSiPMCherenWaveform",
                               "keep killedCherenPhotons",
                               "keep killedScintPhotons",
                               "keep passedScintPhotons",
                               "keep passedCherenPhotons",
                               "keep EventHeader"]

from Configurables import PodioInput

from Configurables import DualCrysSiPMAlgo
from Configurables import DualCrysSiPMSim

## This algorithm will read a filtered list of photons and produce
## digi outputs

algo = None
if (my_opts[0].algo == 'simsipm'):
    algo = DualCrysSiPMSim('Calvision SiPM Algo')
elif (my_opts[0].algo == 'sasha'):
    algo = DualCrysSiPMAlgo('Calvision SiPM Algo')
# default no filter
if (my_opts[0].algo == 'sasha'): 
    if my_opts[0].filter == 'u330':
        algo.U330 = True
    elif my_opts[0].filter == 'o58':
        algo.O58 = True
elif (my_opts[0].algo == 'simsipm' and my_opts[0].filter != 'none'):
    print(f'Currently no filter support using SimSiPM...Sorry!')
    exit()


if (my_opts[0].algo == 'simsipm'):
    # Print setting the wavelength and response for the simsipm pde calculation
    wavelength = [800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300]
    pde = [0.22, 0.30, 0.40, 0.45, 0.50, 0.50, 0.45, 0.35, 0.25, 0.15, 0.0]
    algo.wavelength = wavelength
    algo.sipmEfficiency = pde
    
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
        digi,
        algo,
    ],
    EvtSel = 'NONE',
    EvtMax = 200,
    ExtSvc = [rndmEngine,rndmGenSvc,io_svc]
)

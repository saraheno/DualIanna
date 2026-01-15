import edm4hep
import ROOT
import numpy as np 
from podio import root_io

import argparse
from ROOT import RDataFrame

parser = argparse.ArgumentParser('Process edm4hep digis output to plots')
parser.add_argument('-f','--file', type=str, default = 'edm4hep_output.root')
parser.add_argument('-o','--output', type=str, default = 'edm4hep_plots.root')


args = parser.parse_args()
reader = root_io.Reader(args.file)

# define our output ROOT file and TTree branches
tf = ROOT.TFile(args.output, 'RECREATE')

print('Reading events')

# build a waveform tree 
def buildWaveformTree(treeName, treeComment, sampling, bins):
    xs = None
    ys = None
    evt = np.array([0])
    ix=np.array([0])
    iy=np.array([0])
    layer=np.array([0])

    xbr = None
    ybr = None
    evtbr = None
    ixbr = None
    iybr = None
    layerbr = None

    tree = ROOT.TTree(treeName, treeComment)
    xs = np.array([0.]*bins)
    for i in range (0,bins):
        xs[i] = i*sampling
            
    ys = np.array([0.]*bins)    
    xbr = tree.Branch("xs", xs, f"xs[{bins}]/D")
    ybr = tree.Branch("ys", ys, f"ys[{bins}]/D")
    evtbr = tree.Branch("event", evt, "event/I")
    ixbr =  tree.Branch("ix", ix, "ix/I")
    iybr =  tree.Branch("iy", iy, "iy/I")
    layerbr = tree.Branch("layer", layer, "layer/I")

    brs = {}
    brs['xs'] = (xbr,xs)
    brs['ys'] = (ybr,ys)
    brs['evt'] = (evtbr,evt)
    brs['ix'] = (ixbr,ix)
    brs['iy'] = (iybr,iy)
    brs['layer'] = (layerbr, layer)
    
    return (tree, brs)


# Hardcoded collection / treenames, so if the upstream digis code changes the collection names
# things will break 
treeNames = ['CalvisionSiPMDigiWaveform','CalvisionSiPMCerenWaveform','CalvisionSiPMScintWaveform']
sevt =  reader.get("events")[0]
trees = {}


# Build our output trees
for name in treeNames:

    collection = sevt.get(name)
    if (collection.size() > 0):
        print(f'Adding collection {name}, events {collection.size()}')
        entry =  collection.at(0)

        trees[name] = buildWaveformTree(name,'Digis',entry.getInterval(),entry.amplitude_size())


# Go through all the photons available
# note! Currently no error handling, this can 
# break 
for event in reader.get("events"):

    for name in trees.keys():
        collection = event.get(name)
        
        tree, brs = trees[name]
        
        for s in range(0,collection.size()):
            ts = collection.at(s)
            cellID = ts.getCellID()
            cix = ((0x7f<<3)&cellID)>>3
            ciy = ((0x7f<<10)&cellID)>>10
            layerid = ((0x7<<20)&cellID)>>20
            brs['ix'][1][0] = cix
            brs['iy'][1][0] = ciy
            brs['layer'][1][0] = layerid
            wave = np.array(ts.getAmplitude())
            bincount = ts.amplitude_size()
            for i in range(0,bincount):
                brs['ys'][1][i] = wave[i]
            

            tree.Fill()
        brs['evt'][1][0] +=1
        
tf.Write()    

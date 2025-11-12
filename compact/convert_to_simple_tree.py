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

tf = ROOT.TFile(args.output, 'RECREATE')

wfs = []
xs = None
ys = None
evt = np.array([0])
ix=np.array([0])
iy=np.array([0])
print('Reading events')
ts = None
tree =  ROOT.TTree("calvision_sim","digigraphs" )
xbr = None
ybr = None
evtbr = None
ixbr = None
iybr = None
for event in reader.get("events"):

    totalcollection = event.get('CalvisionSiPMDigiWaveform')

    if (evt[0] == 0):
        ts = totalcollection.at(0)
        sampling = ts.getInterval()
        xs = np.array([0.]*1024)
        for i in range (0,1024):
            xs[i] = i*sampling

        ys = np.array([0.]*1024)
        xbr = tree.Branch("xs", xs, "xs[1024]/D")
        ybr = tree.Branch("ys", ys, "ys[1024]/D")
        evtbr = tree.Branch("event", evt, "event/I")
        ixbr =  tree.Branch("ix", ix, "ix/I")
        iybr =  tree.Branch("iy", iy, "iy/I")
        



    for s in range(0,totalcollection.size()):
        ts = totalcollection.at(s)
        cellID = ts.getCellID()
        cix = ((0x7f<<3)&cellID)>>3
        ciy = ((0x7f<<10)&cellID)>>10
        ix[0] = cix
        iy[0] = ciy
        wave = np.array(ts.getAmplitude())
        for i in range(0,1024):
            ys[i] = wave[i]

        tree.Fill()
    evt[0]+=1
        
tf.Write()    

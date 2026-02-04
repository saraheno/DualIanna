import edm4hep
import ROOT
import numpy as np 
from podio import root_io
import matplotlib.pyplot as plt

import argparse
from ROOT import RDataFrame

parser = argparse.ArgumentParser('Process edm4hep digis output to plots')
parser.add_argument('-f','--file', type=str, default = 'edm4hep_output.root')
parser.add_argument('-o','--output', type=str, default = 'edm4hep_plots.root')
parser.add_argument('-b','--eventbranch', type=str, default = 'events', help='Name for our events branch')
parser.add_argument('-l','--layer', type=int, default = 0)
parser.add_argument('-m', '--limit', type=int, default=-1, help='limit to cut waveforms / photons, -1 -> pass all (default)')
parser.add_argument('-s','--scale', type=float, default = 1.0)
plotChoice = parser.add_mutually_exclusive_group(required=True)
plotChoice.add_argument('-w', action='store_true')
plotChoice.add_argument('-p', action='store_true')

args = parser.parse_args()
print(args)
tf = ROOT.TFile(args.file)
className = tf.Get('events').Class_Name()

reader = None
if className == 'ROOT::RNTuple':
    print('Using NTuple Reader')
    tf.Close()
    reader = root_io.RNTupleReader(args.file)
elif className == 'TTree':
    print('tree')
    tf.Close()
    reader = root_io.Reader(args.file)
else:
    print(f'Unknown {className}')
    exit(-1)



waveTrees = ['CalvisionSiPMDigiWaveform','CalvisionSiPMCherenWaveform','CalvisionSiPMScintWaveform']
responseTrees = ['killedCherenPhotons', 'killedScintPhotons', 'passedCherenPhotons', 'passedScintPhotons']


if not args.eventbranch in reader.categories:
    print('Cannot find the events category, check the file and try again')
    print(f'Categories {reader.categories}')
    exit(-1)

events = reader.get(args.eventbranch)
eventCount = len(events)

evtstr = None
if eventCount == 1:
    evtstr = f'{eventCount} event'
else:
    evtstr = f'{eventCount} events'

print(evtstr)

# first frame 
frame = events[0]
collections = frame.getAvailableCollections()

print(f'Available collections {collections}')

# check we have all necessary trees
for tree in waveTrees:
    if tree not in collections:
        print(f'Failed to find {tree}...quitting')
        exit(-1)

for tree in responseTrees:
    if tree not in collections:
        print(f'Failed to find {tree}...quitting')
        exit(-1)
    

print('Found all necessary trees, processing data')

class Waveform:
    waveform = None
    ix = 0
    iy = 0
    layer = 0
    amax = 0

class Photon:
    ix = 0
    iy = 0
    layer = 0
    wavelength = 0.


for i in range(0, len(events)):
    frame = events[i]
    waveforms = {}
    
    #grab waveform data
    if args.w:
        for tree in waveTrees:
            waveforms[tree] = {}
            waveforms[tree]['max'] = (0, None)
            collection = frame.get(tree)
            for s in range(0, collection.size()):
                if (s%50) == 0:
                    print(f'Processed {s} of {collection.size()} {tree} waveforms')
                ts = collection.at(s)
                cellID = ts.getCellID()
                ix = ((0x7f<<3)&cellID)>>3
                iy = ((0x7f<<10)&cellID)>>10
                layerid = ((0x7<<20)&cellID)>>20
                wave = np.array(ts.getAmplitude())
                bincount = ts.amplitude_size()
                sampling = ts.getInterval()
                key = f'{ix}-{iy}-{layerid}'
                amax = np.argmax(wave)
                
                #print(f'{sampling}, {bincount}, {xs*sampling}')

                wv = Waveform()
                wv.waveform = wave
                wv.ix = ix
                wv.iy = iy
                wv.layer = layerid
                wv.amax = wave[amax]

                waveforms[tree][key] = wv
                waveforms[tree]['xs'] = np.array(range(0,bincount))*sampling


                if (wave[amax] > waveforms[tree]['max'][0]) and args.layer == layerid:
                    #print(f'bigger waveform {wave[amax]} > {waveforms[tree]["max"][0]}')
                    waveforms[tree]['max'] = (wave[amax], wv)



    #grab photon response data
    if args.p:
        photonResponse = {}
        eV = 1e-6
        for tree in responseTrees:
            photonResponse[tree] = {}
            collection = frame.get(tree)
            for idx in range(0,collection.size()):
                if (idx%10000) == 0:
                    print(f'Processed {idx} of {collection.size()} {tree} photons')

                photon = collection.at(idx)
                cellID = photon.getCellID()
                ix = ((0x7f<<3)&cellID)>>3
                iy = ((0x7f<<10)&cellID)>>10
                layerid = ((0x7<<20)&cellID)>>20
                energy = photon.getEnergy()/eV
                wavelength = 1239.84187 / (1000*energy);
                p = Photon()
                p.ix = ix
                p.iy = iy
                p.layer = layerid
                p.wavelength = wavelength
                
                key = f'{ix}-{iy}-{layerid}'
                if not key in photonResponse[tree]:
                    photonResponse[tree][key] = []

                photonResponse[tree][key].append(p)
                if (args.limit > 0 and idx > args.limit):
                    break


    #'CalvisionSiPMCherenWaveform','CalvisionSiPMScintWaveform'
    if args.w:
        scintWave = waveforms['CalvisionSiPMScintWaveform']['max'][1]
        cherenWave = waveforms['CalvisionSiPMCherenWaveform']['max'][1]
        print(f'{scintWave.ix}, {scintWave.iy}, {scintWave.layer}')
        print(f'{cherenWave.ix}, {cherenWave.iy}, {cherenWave.layer}')
        fig,(ax0,ax1,ax2) = plt.subplots(3,1,layout="constrained")
        ax0.plot(waveforms['CalvisionSiPMScintWaveform']['xs'], scintWave.waveform)
        ax0.set_xlabel('ns',loc='right')
        ax0.set_ylabel('mv')
        ax0.set_title('Scintillation Photons',loc='left')

        ax1.plot(waveforms['CalvisionSiPMCherenWaveform']['xs'], cherenWave.waveform)
        ax1.set_xlabel('ns',loc='right')
        ax1.set_ylabel('mv')
        ax1.set_title('Cherenkov Photons',loc='left')

        ax2.plot(waveforms['CalvisionSiPMScintWaveform']['xs'], 
             scintWave.waveform*args.scale + cherenWave.waveform)
        ax2.set_xlabel('ns', loc='right')
        ax2.set_ylabel('mv')
        ax2.set_title('Combined Photons',loc='left')

        plt.show()
    if args.p:
        fig, (ax0, ax1)= plt.subplots(2,1)

        names = {}
        title = ''

        names['pass'] = 'passedScintPhotons'
        names['kill'] = 'killedScintPhotons'
        title = f'Passed Scintilation Photons vs Killed Scintilation Photons'

        passed = {'scint':[], 'cherenkov':[]}
        cut = {'scint':[], 'cherenkov':[]}

        for k in photonResponse['passedScintPhotons']:
            for p in photonResponse['passedScintPhotons'][k]:
                passed['scint'].append(p.wavelength)
        for k in photonResponse['killedScintPhotons']:
            for p in photonResponse['killedScintPhotons'][k]:
                cut['scint'].append(p.wavelength)

        for k in photonResponse['passedCherenPhotons']:
            for p in photonResponse['passedCherenPhotons'][k]:
                passed['cherenkov'].append(p.wavelength)
        for k in photonResponse['killedCherenPhotons']:
            for p in photonResponse['killedCherenPhotons'][k]:
                cut['cherenkov'].append(p.wavelength)

                
        ax0.hist([passed['scint'], cut['scint']], bins=1000,
                  linewidth=0.25, edgecolor='white', stacked = True,
                  label=['Passed Scint', 'Killed Scint'])
        ax1.hist([passed['cherenkov'], cut['cherenkov']], bins=1000,
                  linewidth=0.25, edgecolor='white', stacked = True,
                  label=['Passed Chernkov', 'Killed Cherenkov'])


        ax0.set(xlim=(200,1200))
        ax1.set(xlim=(200,1200))
        ax0.set_xlabel('nm', loc='right')
        ax1.set_xlabel('nm', loc='right')
        ax0.set_ylabel('counts')
        ax1.set_ylabel('counts')
        ax0.set_title('Passed vs Killed Scintillation Photons')
        ax1.set_title('Passed vs Killed Cherenkov Photons')
        ax0.legend()
        ax1.legend()
        plt.show()

        
        

import ROOT
from ROOT import RDataFrame
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser('Waveform drawer')
parser.add_argument("-f", "--file", type=str, default='test.root')
parser.add_argument('-e','--event', type=int, default = 1)
parser.add_argument('-l','--layer', type=int, default = 0)
parser.add_argument('-s','--scale', type=float, default = 1.0)

args = parser.parse_args()


filterS = f'event=={args.event} && layer == {args.layer}'
print(filterS)
scint = RDataFrame('CalvisionSiPMScintWaveform', args.file).Filter(filterS)
cheren = RDataFrame('CalvisionSiPMCherenWaveform', args.file).Filter(filterS)
combo = RDataFrame('CalvisionSiPMDigiWaveform', args.file).Filter(filterS)

nparrs = ['xs', 'ys', "ix", "iy"]

swaves = scint.AsNumpy(nparrs)
cwaves = cheren.AsNumpy(nparrs)
combowaves = combo.AsNumpy(nparrs)


swavemaxes = []
cwavemaxes = []
combowavemaxes = []
for arr in swaves['ys']:
    swavemaxes.append(np.max(arr))
for arr in cwaves['ys']:
    cwavemaxes.append(np.max(arr))
for arr in combowaves['ys']:
    combowavemaxes.append(np.max(arr))

maxscint = np.argmax(swavemaxes)
maxcheren = np.argmax(cwavemaxes)
maxcombo =  np.argmax(combowavemaxes)
msg =f'Found max event :: scint {maxscint}, {swavemaxes[maxscint]}, cheren {maxcheren}, {cwavemaxes[maxcheren]}'
msg += f' combined {maxcombo}, {combowavemaxes[maxcombo]}'
print(msg)
print(f'scint max ix: {swaves["ix"][maxscint]}, iy: {swaves["iy"][maxscint]}')
print(f'cheren max ix: {cwaves["ix"][maxcheren]}, iy: {cwaves["iy"][maxcheren]}')
print(f'combo max ix: {combowaves["ix"][maxcombo]}, iy: {combowaves["iy"][maxcombo]}')



fig,(ax0,ax1,ax2) = plt.subplots(3,1)
#for i in range (0, len(swaves['xs'])):
#    ax0.plot(swaves['xs'][i], swaves['ys'][i])
ax0.plot(swaves['xs'][maxscint], swaves['ys'][maxscint]*args.scale)    
ax0.set_xlabel('ns',loc='right')
ax0.set_ylabel('mv')
ax0.set_title('Scintilation Photons',loc='left')

#for i in range (0, len(cwaves['xs'])):
#    ax1.plot(cwaves['xs'][i], cwaves['ys'][i])
ax1.plot(cwaves['xs'][maxcheren], cwaves['ys'][maxcheren])


ax1.set_xlabel('ns',loc='right')
ax1.set_ylabel('mv')
ax1.set_title('Cherenkov Photons',loc='left')

#for i in range (0, len(combowaves['xs'])):
#    ax2.plot(combowaves['xs'][i], combowaves['ys'][i])

ax2.plot(combowaves['xs'][maxcombo], swaves['ys'][maxscint]*args.scale + cwaves['ys'][maxcheren])
ax2.set_xlabel('ns', loc='right')
ax2.set_ylabel('mv')
ax2.set_title('Combined Photons',loc='left')

plt.show()

#waveforms = rdf.Filter('event==3 && layer==0').AsNumpy(['xs', 'ys'])
# ax.plot(waveforms['xs'][0], waveforms['ys'][0])
# plt.title('Single Photon Response')
# plt.xlabel('ns')
# plt.ylabel('mv')
# plt.show()

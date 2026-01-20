from ROOT import RDataFrame
import numpy as np
import matplotlib.pyplot as plt

import argparse


parser = argparse.ArgumentParser("Basic Signal Analysis")
parser.add_argument("-f", "--file", type=str, default='test.root')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--scintillation', action='store_true')
group.add_argument('-c', '--cherenkov', action='store_true')


args = parser.parse_args()



dfs = {}

names = ['passedScintPhotons', 'passedCherenPhotons', 'killedScintPhotons', 'killedCherenPhotons']
for name in names:
    rdf = RDataFrame(name, args.file)

    dfs[name] =     rdf.AsNumpy(["wavelength"])



fig, axes= plt.subplots()

names = {}
title = ''
if args.scintillation:
    names['pass'] = 'passedScintPhotons'
    names['kill'] = 'killedScintPhotons'
    title = f'Passed Scintilation Photons vs Killed Scintilation Photons'
elif args.cherenkov:
    names['pass'] = 'passedCherenPhotons'
    names['kill'] = 'killedCherenPhotons'
    title = f'Passed Cherenkov Photons vs Killed Cherenkov Photons'


    
axes.hist(dfs[names['pass']]['wavelength'], bins=1000, linewidth=0.25, edgecolor='white', label='Passed')
axes.hist(dfs[names['kill']]['wavelength'], bins=1000, linewidth=0.25, edgecolor='white', label='Killed')

axes.set(xlim=(200,1200))
axes.set_xlabel('nm', loc='right')
axes.set_ylabel('counts')
axes.set_title(title)
axes.legend()
plt.show()







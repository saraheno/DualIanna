from ROOT import RDataFrame
import argparse 
import time

parser = argparse.ArgumentParser('2D Histogram of simple digis tree')
parser.add_argument('-f', '--file', type=str, default='edm4hep_plots.root', help='file to process')
parser.add_argument('-l', '--layer', type=int, default = 0, help='Layer to look at')
args = parser.parse_args()

rdf = RDataFrame("CalvisionSiPMDigiWaveform", args.file)

layerFilter = f'layer=={args.layer}'

prof = rdf.Filter(layerFilter).Profile2D(("name", "title", 10, 0, 10, 10, 0, 10), "ix", "iy", "ys")
prof.Draw()

time.sleep(5)



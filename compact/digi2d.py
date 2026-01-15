from ROOT import RDataFrame
import argparse 
import time

parser = argparse.ArgumentParser('2D Histogram of simple digis tree')
parser.add_argument('-f', '--file', type=str, default='edm4hep_plots.root', help='file to process')
args = parser.parse_args()

rdf = RDataFrame("CalvisionSiPMDigiWaveform", args.file)

prof = rdf.Filter("layer==0").Profile2D(("name", "title", 10, 0, 10, 10, 0, 10), "ix", "iy", "ys")
prof.Draw()

time.sleep(5)



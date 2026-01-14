from ROOT import RDataFrame

import time

rdf = RDataFrame("CalvisionSiPMDigiWaveform", "edm4hep_plots.root")

prof = rdf.Profile2D(("name", "title", 10, 0, 10, 10, 0, 10), "ix", "iy", "ys")
prof.Draw()

time.sleep(5)



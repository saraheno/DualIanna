import edm4hep
import ROOT
import numpy as np 
from podio import root_io

reader = root_io.Reader('edm4hep_output.root')

wfs = []
print('Reading events')
evt = 0
for event in reader.get("events"):

    scintcollection = event.get('CalvisionSiPMScintWaveform')
    cerenkovcollection = event.get('CalvisionSiPMCerenWaveform')
    totalcollection = event.get('CalvisionSiPMDigiWaveform')
    print(f'TC Sz: {totalcollection.size()}, CC SZ: {cerenkovcollection.size()}')
    print(f'SC Sz: {scintcollection.size()}')
    scintpts = []
    cerenkovpts = []
    totalpts = []
    xs = []
    dt = 0.2 # sampling time in ns
    for i in range (0, 1024):
        scintpts.append(scintcollection.at(0).getAmplitude().at(i))
        cerenkovpts.append(cerenkovcollection.at(0).getAmplitude().at(i))
        totalpts.append(totalcollection.at(0).getAmplitude().at(i))
        xs.append( i*dt)

    xss = np.array(xs)

    totalgraph = ROOT.TGraph(1024, xss, np.array(totalpts))
    totalgraph.SetTitle("Combined Scint. and Cerenkov Signals;ns;Arb. Unit")
    cerengraph = ROOT.TGraph(1024, xss, np.array(cerenkovpts))
    cerengraph.SetTitle("Cerenkov Signal;ns;Arb. Unit")
    scintgraph = ROOT.TGraph(1024, xss, np.array(scintpts))
    scintgraph.SetTitle("Scintillation Signal;ns;Arb. Unit")

    canvas = ROOT.TCanvas("Digis", "Digis", 1024, 768)
    canvas.Divide(1,3)
    canvas.cd(1)
    totalgraph.Draw()
    canvas.cd(2)
    cerengraph.Draw()
    canvas.cd(3)
    scintgraph.Draw()

    canvas.SaveAs(f"digi-{evt}.png")

    canvas.Clear()
    for i in range(1, totalcollection.size()):
        totalpts = []
        for j in range (0, 1024):
            totalpts.append(totalcollection.at(i).getAmplitude().at(j))
        totalgraph = ROOT.TGraph(1024, xss, np.array(totalpts))
        cellID = totalcollection.at(i).getCellID()
        ix = ((0x7f<<3)&cellID)>>3
        iy = ((0x7f<<10)&cellID)>>10
        totalgraph.SetTitle(f'Total Evt {i}: {ix},{iy};ns;Arb')
        canvas = ROOT.TCanvas("Digis", "Digis", 1024, 768)
        totalgraph.Draw()
        canvas.SaveAs(f"digi-{i}-{ix}-{iy}.png")
        
        
    evt += 1

        


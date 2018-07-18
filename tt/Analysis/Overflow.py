import ROOT
import os
import sys


# sample directory path
directory = 'files_nominal'
file_list = os.listdir(directory)
# loop over all root files
for sample in file_list:
    fin = ROOT.TFile(directory+'/'+sample,"UPDATE")
    
    # loop over all TDirectory
    for key in fin.GetListOfKeys():
        tdirName = key.GetName()
        # get hist name
        for histK in fin.Get(tdirName).GetListOfKeys():
            histName = histK.GetName()
            hist = fin.Get(tdirName).Get(histName)
            histDim = hist.GetDimension()
            nbinX = hist.GetNbinsX()        
            # rebin overflow
            # for 1D
            if histDim==1:
                hist.SetBinContent(hist.GetNbinsX(),hist.GetBinContent(hist.GetNbinsX()+1)+hist.GetBinContent(hist.GetNbinsX()))
                hist.SetBinContent(nbinX+1,0.0)
                hist.SetBinError(hist.GetNbinsX()+1,0.0)
            if histDim==2:
                nbinY = hist.GetNbinsY()
                for ibin in range(nbinY):
                    hist.SetBinContent(hist.GetNbinsX(),ibin,hist.GetBinContent(hist.GetNbinsX()+1,ibin)+hist.GetBinContent(hist.GetNbinsX(),ibin))
                    hist.SetBinContent(nbinX+1,ibin,0.0)
                    #hist.SetBinError(hist.GetNbinsX()+1,0.0)
                for jbin in range(nbinX):
                    hist.SetBinContent(jbin,hist.GetNbinsY(),hist.GetBinContent(jbin,hist.GetNbinsY()+1)+hist.GetBinContent(jbin,hist.GetNbinsX()))
                    hist.SetBinContent(jbin,nbinY+1,0.0)

            #rebinHist = hist.Clone(hist.GetName())
            #fin.Get(tdirName).WriteObject(rebinHist,rebinHist.GetName()+'rb')


                
        


import numpy as np
import os
import subprocess
from ciao_contrib.runtool import *
from sherpa.astro.ui import *
from pychips import *


#save the data of the radial profile in the fileoutput.dat

def savedata(name, output):
    load_data(1,"" + name + "_rprofile_rmid2.fits", 
    3, ["RMID","SUR_BRI","SUR_BRI_ERR"])
    save_data("" + output + ".dat")
    return

#comute the radial profile of EvtFile in the region (annuli) and with the 
#background region regionbkg. The radial profile can be computed for an 
#energy interval [energymin,energymax]

def rpdata(EvtFile, region, regionbkg, energymin, energymax, name, output):
    os.system('dmcopy "' + EvtFile + '[energy=' + energymin + ':' + 
    energymax + ']"  ' + name + '.fits')
    os.system('punlearn dmextract')
    os.system('pset dmextract infile="' + name + '.fits[bin sky=@' 
    + region + ']"')
    os.system('pset dmextract outfile=' + name + '_rprofile2.fits')
    os.system('pset dmextract bkg="' + name + 
    '.fits[bin sky=@' + regionbkg + ']"')
    os.system('pset dmextract opt=generic')
    os.system('dmextract') 
    os.system('punlearn dmtcalc')
    os.system('pset dmtcalc infile=' + name + '_rprofile2.fits')
    os.system('pset dmtcalc outfile=' + name + '_rprofile_rmid2.fits')
    os.system('pset dmtcalc expression="rmid=0.5*(R[0]+R[1])"')
    os.system('dmtcalc')
    #save the data in a file
    savedata(name, output)
    return

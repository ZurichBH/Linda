import subprocess
import os
from ciao_contrib.runtool import *
from sherpa.astro.ui import *
from pychips import *
import sherpa
from sherpa_contrib.chart import *


"""
BEGINNING:
Before running this, you need to find manually the physical coordinates in
ds9. You need also to define a region around the source (source.reg) and 
a region for the background (backg.reg) using ds9. 

With beginning.py you can find and fit the spectra of an AGN (with resp. 
spec and fit_spec) and the coordinates of the AGN, together with its exposure
time and the detector type (coord_exp_type). Marx_and_srcextent projects the 
PSF (previously simulated with ChaRT) and returns the Source Observed Size, 
the PSF Size and the Intrinsic Size (see also sourcextent). The offset PSFs
can be corrected with offset and Marx_offset.

See also:
 -Preparing to run ChaRT: http://cxc.harvard.edu/chart/threads/prep/
 -Using MARX to create an event file: http://cxc.harvard.edu/chart/threads/marx/

"""


#extract the spectrum of a galaxy with ObsId Id

def spec(Id):
    specextract.punlearn()
    specextract.infile="acisf" + Id + "_repro_evt2.fits[sky=region(source.reg)]"
    specextract.outroot="spec"
    specextract.bkgfile="acisf" + Id + "_repro_evt2.fits[sky=region(backg.reg)]"
    a=specextract(weight="no", correctpsf="yes", bkgresp="no")
    return a


def fit_spec(Id, method):
    #specextract.punlearn()
    #specextract.infile="acisf"+Id+"_repro_evt2.fits[sky=region(source.reg)]"
    #specextract.outroot="spec"
    #specextract.bkgfile="acisf"+Id+"_repro_evt2.fits[sky=region(backg.reg)]"
    #a=specextract(weight="no", correctpsf="yes", bkgresp="no")
    load_pha("spec_grp.pi")	
    subtract()
    ignore(":0.5,8.0:")
    set_source(method)
    abs1.nh = 0.07
    guess(p1)
    fit()
    plot_fit()
    plot_chart_spectrum()
    plot_chart_spectrum(elow=1.0, ehigh=8.0)
    save_chart_spectrum("source_flux_chart.dat", elow=1.0, ehigh=8.0)
    return plot_chart_spectrum(elow=1.0, ehigh=8.0)


#Given the coordinates sky(x,y) returns the coordinates RA, Dec, RANom, DecNom, 
#RollNom, theta, phi, the exposure time and the type of the #detector

def coord_exp_type(EventFile, Asol, x, y):
    dmcoords.punlearn()
    dmcoords.infile = '' + EventFile + ''
    dmcoords.asol = '' + Asol + ''
    dmcoords.opt = 'sky'
    dmcoords.x = '' + x + ''
    dmcoords.y = '' + y + ''
    os.system('punlearn dmkeypar')
    a = os.system('dmkeypar ' + EventFile + ' exposure echo+')
    os.system('dmlist ' + EventFile + ' header | grep _NOM')
    return dmcoords(verbose=1), a

#If you want to see more coortinates write print(dmcoords) in the terminal 
#after doing coord_exe_type(...)


#The PSF is projected with marx and the angular size of source and PSF is 
#computed with srcextent
#Parameters: Id = ObsId, Coordinates = theta, phi, RANom, DecNom, RollNom, 
#RA (=RA of the source), Dec (=Dec of the source), Exposure time = exp,
#Type of the detector = Type (could be ACIS-S or ACIS-I)

def Marx_and_srcextent(Id, theta, phi, exp, RANom, DecNom, RollNom, RA, Dec, Type, no):

    #Marx

    os.system('cp /prog/marx/4.5.0/share/marx/pfiles/marx.par ./marx.par')
    os.system('pset ./marx SAOSACFile = HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' + exp + '.fits')
    os.system('pset ./marx OutputDir = HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' + exp + '.dir')
    os.system('pset ./marx DitherModel = INTERNAL')
    os.system('pset ./marx SourceType = SAOSAC')
    os.system('pset ./marx RA_Nom = ' + RANom + '')
    os.system('pset ./marx Dec_Nom = ' + DecNom + '')
    os.system('pset ./marx Roll_Nom = ' + RollNom + '')
    os.system('pset ./marx SourceRA = ' + RA + '')
    os.system('pset ./marx SourceDEC = ' + Dec + '')
    os.system('pset ./marx DetectorType = ' + Type + '')
    os.system('pset ./marx GratingType=NONE')
    os.system('pset ./marx ExposureTime=0.0')
    os.system('marx @@./marx.par')
    os.system('marx2fits HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' +exp+ '.dir marx_HRMA_theta' +theta+ 
    '_phi' +phi+ '_ensource_flux_chart.dat_exp' +exp+ '.fits')
    
	#srcextent

    os.system('punlearn srcextent')
    os.system('pset srcextent srcfile=acisf' + Id + '_repro_evt2.fits')
    os.system('pset srcextent outfile=extent' + no + '.fits')
    os.system('pset srcextent psffile=marx_HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' + exp + '.fits')
    os.system('pset srcextent regfile=source.reg')
    os.system('srcextent verbose=3')


#srcextent alone, if you already have the PSF file (Marx), no is a number  

def sourcextent(Id, Marx, no):
    os.system('punlearn srcextent')
    os.system('pset srcextent srcfile=acisf' + Id + '_repro_evt2.fits')
    os.system('pset srcextent outfile=extent'+ no +'.fits')
    os.system('pset srcextent psffile=' + Marx +'')
    os.system('pset srcextent regfile=source.reg') 
    #source.reg is a circle around the source (ds9)
    os.system('srcextent verbose=3')


#compute the offset of the PSF (Marx) w.r.t the data file (EvtFile)

def offset(EvtFile,Marx):
    os.system('dmlist ' + EvtFile + ' header | grep SIM_ ')
    os.system('dmlist ' + Marx + ' header | grep SIM_ ')


#reprojects the PSF without offset. offx and offz are the difference of offset 
#in x and in z between the data file and the PSF. theta, phi and exp are used 
#to reproduce the name of the PSF.

def Marx_offset(theta, phi, exp, RANom, DecNom, RollNom, RA, Dec, Type, offx, offz):
    os.system('cp /prog/marx/4.5.0/share/marx/pfiles/marx.par ./marx.par')
    os.system('pset ./marx SAOSACFile = HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' +exp+ '.fits')
    os.system('pset ./marx OutputDir = HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' +exp+ '.dir')
    os.system('pset ./marx DitherModel = INTERNAL')
    os.system('pset ./marx SourceType = SAOSAC')
    os.system('pset ./marx RA_Nom = ' + RANom + '')
    os.system('pset ./marx Dec_Nom = ' + DecNom + '')
    os.system('pset ./marx Roll_Nom = ' + RollNom + '')
    os.system('pset ./marx SourceRA = ' + RA + '')
    os.system('pset ./marx SourceDEC = ' + Dec + '')
    os.system('pset ./marx DetectorType = ' + Type + '')
    os.system('pset ./marx GratingType=NONE')
    os.system('pset ./marx ExposureTime=0.0')
    os.system('marx @@./marx.par')
#offset Marx
    os.system('pset ./marx DetOffsetX = ' + offx + '')
    os.system('pset ./marx DetOffsetZ = ' + offz + '')
    os.system('pset ./marx OutputDir=offset_HRMA_theta' + theta + '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' + exp + '.dir')
    os.system('marx @@./marx.par')
    os.system('marx2fits offset_HRMA_theta' +theta+ '_phi' + phi + 
    '_ensource_flux_chart.dat_exp' + exp + '.dir offset_HRMA_theta' +theta+ 
    '_phi' +phi+ '_ensource_flux_chart.dat_exp' +exp+ '.fits')










import subprocess
import os
from ciao_contrib.runtool import *


list_names=[]


#Merges the eventfile (EvtFile, in our case another PSF) and the projected 
#psf (Marx) by using dmimgcalc. The output's name is saved in list_names

def merge(EvtFile, Marx, xmod, ymod, factor):
    dmmerge.punlearn()
    dmmerge(infile='' + EvtFile + ',' + Marx + '[cols -prob]', 
    outfile='merged_' + xmod + ':' + ymod + '_'+factor + '.fits')
    c=dmmerge.outfile
    return list_names.append(c)
	
	
#Decreases the number of photons of the projected psf by reducing the 
#number of its rows, factor= number photons I want/ number total photons

def photons(Marx, xmod, ymod, factor):
    dmtcalc(infile='' + Marx + '', 
    outfile='' + xmod + ':' + ymod + '_' + factor + '.fits', 
    expression='prob=#rand(1)')
    dmcopy(infile='' + xmod + ':' + ymod + '_' + factor + '.fits[prob < ' + factor + ']', 
    outfile='photons_' + xmod + ':' + ymod + '_' + factor + '.fits')
    b=dmcopy.outfile
    return b


#EvtFile is binned to an interval [x=xmin:xmax:pix,y=ymin:ymax:pix], then
#smoothed (see also bin_smooth_deconvolve.py)

def bin(EvtFile, xmin, xmax, ymin, ymax, diff, pix, name, smooth):
    os.system('dmcopy "' + EvtFile + '[bin x=' + xmin + ':' + xmax + ':' 
    + pix + ',y=' + ymin + ':' + ymax + ':' + pix + ']" ' 
    + name + '' + diff + '' + pix + '.fits')
    aconvolve.punlearn()
    aconvolve.infile='' + name + '' + diff + '' + pix + '.fits' 
    aconvolve.outfile='' + name + '' + diff + '' + pix + '' + smooth + '.fits'
    aconvolve.kernelspec='lib:gaus(2,5,1,' + smooth + ',' + smooth + ')' 
    aconvolve.method='fft'
    aconvolve()
    return aconvolve.outfile


#Change the coordinates of the projected psf, reduces the number of its 
#photons (by using photons) and add it to the event file (using merge)
#Parameters: EvtFile=Data form Chandra, Marx=projected PSF, xmod,ymod=
#Modifyed Ra and Dec coordinates, factor=number photons I want/ number total photons.
#bin is already included in this function.

def repxy(EvtFile, Marx, xmod, ymod, factor, xmin, xmax, ymin, ymax, diff, pix, name, smooth):
    reproject_events.infile=Marx
    reproject_events.outfile='reproj_'+xmod+':'+ymod+'_'+factor+'.fits'
    reproject_events.match=''+xmod+' '+ymod+''
    a = reproject_events(verbose=1)
    d = photons(reproject_events.outfile,xmod,ymod,factor)
    h = merge(EvtFile,dmcopy.outfile,xmod,ymod,factor)
    os.system('dmcopy "merged_' + xmod + ':' + ymod + '_' + factor + 
    '.fits[bin x=' + xmin + ':' + xmax + ':' + pix + ',y=' 
    + ymin + ':' + ymax + ':' + pix + ']" ' + name + '' + diff + '' + pix + '.fits')
    aconvolve.punlearn()
    aconvolve.infile='' + name + '' + diff + '' + pix + '.fits' 
    aconvolve.outfile='' + name + '' + diff + '' + pix + '' + smooth + '.fits'
    aconvolve.kernelspec='lib:gaus(2,5,1,' + smooth + ',' + smooth + ')' 
    aconvolve.method='fft'
    aconvolve()
    return aconvolve.outfile

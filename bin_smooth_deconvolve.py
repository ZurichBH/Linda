from ciao_contrib.runtool import *
import os
import subprocess


#the function bin bins a, event file to a coordinates interval 
#[(xmin,ymin):(xmax,ymax)] and then smooth the resutling image. 
#xmax-xmin = ymax-ymin = diff, smooth = smooth parameter,
#pix = the pixel fraction (e.g. 0.1, 0.25, 1...), the output file is
#namediffpixsmooth.fits

def bin(EvtFile, xmin, xmax, ymin, ymax, diff, pix, name, smooth):
    os.system('dmcopy "' + EvtFile + '[bin x=' + xmin + ':' + xmax + ':' + pix + 
    ',y=' + ymin + ':' + ymax + ':' + pix + ']" ' + name + '' + diff + '
    ' + pix +'.fits')
    aconvolve.punlearn()
    aconvolve.infile=''+ name +''+ diff +''+ pix +'.fits' 
    aconvolve.outfile=''+ name +''+ diff +''+ pix +''+ smooth +'.fits'
    aconvolve.kernelspec='lib:gaus(2,5,1,'+smooth+','+smooth+')' 
    aconvolve.method='fft'
    aconvolve()
    return aconvolve.outfile


#Bin a PSF file to the energy range 6 - 7 keV
#the output file is name.fits

def energy(Marx, name):
    dmcopy.infile=''+Marx+'[energy=6000:7000]'
    dmcopy.outfile=''+name+'.fits'
    dmcopy()
    return


#smooth a fits file (EvtFile), the output
#file is name.fits. Is it better to bin
#EvtFile before smoothing it

def smooth(EvtFile, smooth, name):
    aconvolve.punlearn()
    aconvolve.infile=''+EvtFile+'' 
    aconvolve.outfile=''+ name +''+ smooth +'.fits'
    aconvolve.kernelspec='lib:gaus(2,5,1,'+smooth+','+smooth+')' 
    aconvolve.method='fft'
    aconvolve()
    return aconvolve.outfile


#Deconvolve an event file (EvtFile) and its PSF

def deconv(EvtFile, Marx, name):
    
	arestore.infile=''+ EvtFile +''
	arestore.psffile=''+ Marx +''
	arestore.outfile=''+ name +'.fits'
	#arestore.method='lucy'
	arestore.numiter='100'
	return arestore()


#Operation between two image files, the output file is
#name.fits, the operation is oper and the two operands
#are EvtFile and Marx

def operation(EvtFile, Marx, name, oper):
    dmimgcalc.punlearn()
    dmimgcalc.infile=''+ EvtFile +''
    dmimgcalc.infile2=''+ Marx +''
    dmimgcalc.outfile=''+ name +''
    dmimgcalc.operation=''+ oper +''
    return dmimgcalc()

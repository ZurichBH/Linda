import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import copy
import os
import aplpy


#Do not use this in CIAO

#plots the output fits file of simulations.py (just one).
#sep = separation between the two PSF, frac = photon fraction
#emin,emax = energy interval, Name = name of the output image,
#vmax = max of the colorscale

def grafici(Name, vmax, sep, frac, emin, emax):
    gc=aplpy.FITSFigure('' + Name + '.fits')
    gc.add_scalebar(0.000138889)
    gc.scalebar.set_label('       size 0.5"\n separation ' + sep + '"')
    gc.scalebar.set_color('gray')
    gc.scalebar.set_font(size='xx-large',weight='heavy')
    gc.show_colorscale(cmap='gist_heat',stretch='arcsinh',vmin=0.0,vmax=vmax)
    gc.add_label(0.2, 0.9, 'Energy: ' 
    + emin + '- ' + emax + ' keV\n Photons: 1 to ' 
    + frac + '', color ='gray', relative= True, size = 'x-large')
    gc.add_colorbar()
    gc.colorbar.show()
    gc.save('' + Name + '.eps')
    gc.save('' + Name + '.png')
    return gc.colorbar.show()

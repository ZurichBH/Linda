import numpy as np
from matplotlib import pyplot as plt
import astropy
import csv
import pylab


"""
Cancel the text lines from the radial profile data
file before using column_to_array

"""


#Read the columns of a radial profile data file (namefile)
#into arrays 

def column_to_array(namefile):
    arr=[]
    inp=open(""+namefile+".dat","r")
    #read line into array
    for line in inp.readlines():
        for i in line.split():
            arr.append(i)

    x=[]
    for i in range(len(arr)):
        if (i+2*i)<len(arr):
            x.append(arr[i+2*i])
    x=np.array(map(float,x))

    y=[]	
    for i in range(len(arr)):
        if (i+1+2*i)<len(arr):
            y.append(arr[i+1+2*i])
    y=np.array(map(float,y))

    z=[]
    for i in range(len(arr)):
        if (i+2+2*i)<len(arr):
            z.append(arr[i+2+2*i])
    z=np.array(map(float,z))
    print x
    print y
    print z
    return x,y,z


#plot the radial profile of the PSF with the
#radial profile of the simulations (two PSF)
#taken from the radial profile data files
#namesim (simulation) and namepsf (PSF)

def rprofile(namesim,namepsf,output):
    #[col0,col1,col2]=column_to_array(namefile)
    [pcol0,pcol1,pcol2]=column_to_array(namepsf)
    [scol0,scol1,scol2]=column_to_array(namesim)

    arr0=np.array([pcol0,scol0])
    arr1=np.array([pcol1,scol1])
    arr2=np.array([pcol2,scol2])

    arr0_arcsec=arr0*0.5


    arr1_as=arr1/0.5**2
    arr2_as=arr2/0.5**2
    #plt.errorbar(arr0_arcsec[0],arr1_as[0], yerr=arr2_as[0],fmt='c-',ecolor='k')
    plt.errorbar(arr0_arcsec[1],arr1_as[1], yerr=arr2_as[1],fmt='m-',ecolor='k')
    plt.errorbar(arr0_arcsec[0],arr1_as[0], yerr=arr2_as[0],fmt='r-',ecolor='k')
    plt.xlabel('Radial Distance [arcsec]')
    plt.axvline(x=0.6,color='0.5',ls='dashed') 
    plt.ylabel('counts/arcsec^2')
    plt.legend(('0.5 - 8 keV (Two PSF)','0.5 - 8 keV (PSF)'))
    pylab.xlim([0.25,2.5])	
    plt.annotate("Second PSF's center", xy=(0.5, 0.5), size=8,  xycoords='data',
    xytext=(0.15, 0.3), textcoords='axes fraction',rotation=90,
    horizontalalignment='right', verticalalignment='top',)

    plt.show()
    plt.savefig(''+output+'.eps')
    plt.savefig(''+output+'.jpg')
    return



	

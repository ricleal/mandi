from mantid.simpleapi import *
from mantid.api import *
from mantid.kernel import V3D

import numpy as np

from collections import defaultdict

from __future__ import division
import numpy as np
'''

import sys
sys.path.append('/SNS/users/rhf/git/mandi/src')

import mxdiagnostics.symop
reload(mxdiagnostics.symop)
from mxdiagnostics.symop import Reflections

'''

from mxdiagnostics import Reflections

# EDIT:
peaks_ws_name = 'peaks_ws'
space_group = 'P212121'

# get WSs
peaks_ws = mtd[peaks_ws_name]
#
# Funcs
#

def v3d_to_tuple_int(v):
    return (int(v.X()),
    int(v.Y()),
    int(v.Z()))

#
# Main
# 

r = Reflections(space_group)
    
# iterate all peaks
for i in range(peaks_ws.getNumberPeaks()):
    peak = peaks_ws.getPeak(i)
    miller_indice = v3d_to_tuple_int(peak.getHKL())
    intensity = peak.getIntensity()
    sigma = peak.getSigmaIntensity()
    d = peak.getDSpacing()
    r.build_equivalent_reflection_list(miller_indice, intensity, sigma, d)

print len(r)
r.delete_reflections_below_intensity_treshold(0.1)
print len(r)

hkl = r.get_reflection_with_the_most_multiplicity()

print r.reflections[hkl]


i_vector = r.get_value_for_refection(hkl,0)
d_vector = r.get_value_for_refection(hkl,2)
gui_cmd(plt.figure)
gui_cmd(plt.plot, d_vector, i_vector, '.')
gui_cmd(plt.title, '')
gui_cmd(plt.xlabel, 'DSpacing')
gui_cmd(plt.ylabel, 'I')
gui_cmd(plt.show)

#plot all
gui_cmd(plt.figure)

for hkl in r.reflections.keys():
    i_vector = r.get_value_for_refection(hkl,0)
    d_vector = r.get_value_for_refection(hkl,2)
    gui_cmd(plt.plot, d_vector, i_vector, '.')
    
gui_cmd(plt.title, '')
gui_cmd(plt.xlabel, 'DSpacing')
gui_cmd(plt.ylabel, 'I')
gui_cmd(plt.show)



#
# Dummy tests
#

peaks_ws = IntegratePeaksMD( InputWorkspace=MDEW, 
                               PeakRadius=0.01,
                  CoordinatesToUse="Q (sample frame)",
                  BackgroundOuterRadius=0.013, 
                  BackgroundInnerRadius=0.011,
                  PeaksWorkspace=peaks_ws, 
                  IntegrateIfOnEdge=True )


# iterate all peaks
total = peaks_ws.getNumberPeaks()
total_negative = 0
total_ISig_less_than_2 = 0
for i in range(peaks_ws.getNumberPeaks()):
    peak = peaks_ws.getPeak(i)
    intensity = peak.getIntensity()
    sigma = peak.getSigmaIntensity()
    if intensity < 0:
        total_negative+=1
    if np.float64( intensity ) / sigma  < 2 : #gives NAN if sigma = 0
        total_ISig_less_than_2 +=1

print "total",total
print "total_negative",total_negative, total_negative/total
print "total_ISig_less_than_2",total_ISig_less_than_2, total_ISig_less_than_2/total
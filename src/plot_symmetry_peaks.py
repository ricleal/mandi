from mantid.simpleapi import *
from mantid.api import *
from mantid.kernel import V3D

import numpy as np

from collections import defaultdict

from diagnostics import Reflections

'''

'''
# EDIT:
peaks_ws_name = 'event_ws_3870_int'
space_group = 'P212121'
peak_to_plot =''


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


d_vector = peaks_ws.column('DSpacing')

gui_cmd(plt.figure)
gui_cmd(plt.plot, d_vector, peaks[peak_to_plot], '.')
gui_cmd(plt.title, '')
gui_cmd(plt.xlabel, 'DSpacing')
gui_cmd(plt.ylabel, 'I')
gui_cmd(plt.show)
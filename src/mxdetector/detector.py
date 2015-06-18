'''
Created on Jun 18, 2015

@author: rhf
'''

import os
import math
import numpy as np

import sys
sys.path.append('/opt/mantidnightly/bin')
sys.path.append('/home/rhf/git/mantid/Build/bin')

from mantid.simpleapi import *
from mantid.api import *

#FILENAME = os.path.join(os.path.dirname(os.path.realpath(__file__)),"ZZZ.xml")
FILENAME = r'/SNS/users/rhf/2015-05-15_-_Tests_for_Marat/ricardo/MANDI_Definition_2014_08_01.xml'

class Detector(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        ws = LoadEmptyInstrument(FILENAME)
        self.istrument = ws.getInstrument()
    
    def get_pixel_positions_in_space(self,bankname):
        b = self.istrument.getComponentByName(bankname)
        detector_ids_range = range(b.minDetectorID(), b.maxDetectorID() + 1) #555904 -> 2621439
        bank = []
        for det_id in detector_ids_range:
            det = self.istrument.getDetector(det_id)
            pos = det.getPos()
            bank.append([det_id, pos.getX(), pos.getY(), pos.getZ() ])
        # For bankname, Array with all the [det_id, x, y, z]
        bank_arr = np.array(bank)
        return bank_arr
    
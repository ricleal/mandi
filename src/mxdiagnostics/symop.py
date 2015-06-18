#! /usr/bin/env python

import sys
import shlex
import ast
import copy
import os
from collections import defaultdict
import pprint
'''
SymOp.lib structure:

5 4 2 C2 PG2 MONOCLINIC 'C 1 2 1' 
  X,Y, Z 
 -X,Y,-Z 
 1/2+X,1/2+Y,Z 
 1/2-X,1/2+Y,-Z


<sg number> <multiplicity / number of sym operations> <primitive multiplicity> 
<?> <point group> <crystal system> <long name> [<long name alternaytive>
 < ... operations ...>

['194', '24', '24', 'P63/mmc', 'PG6/mmm', 'HEXAGONAL', 'P 63/m 2/m 2/c', 'P 63/m m c']
['195', '12', '12', 'P23', 'PG23', 'CUBIC', 'P 2 3']

'''

FILENAME= os.path.join(os.path.dirname(os.path.realpath(__file__)),"symop.lib")


class SymOp():
    def __init__(self,filename=None):
        #print "Opening", FILENAME
        if filename is None:
            filename= FILENAME
        
        # Every dict will be initilsed as an empty list
        self.lib = {} 
        
        self._parse(filename)
        
        
    def __str__(self):
        return(pprint.pformat(self.lib))
    
    def _parse(self, filename):
        
        point_groups = defaultdict(list)
        with open(FILENAME) as f:
            for line in f:
                if not line.startswith(' '):
                    #head
                    tokens = shlex.split(line,comments=True)
                    if int(tokens[0])>230: # ignoring the remaining SG
                        break
                    
                    self.lib[tokens[3]] = {}                                   
                    self.lib[tokens[3]]["xyz_operations"] = []
                    self.lib[tokens[3]]["hkl_operations"] = []
                    self.lib[tokens[3]]['number'] = int(tokens[0])
                    self.lib[tokens[3]]['multiplicity'] = int(tokens[1])
                    self.lib[tokens[3]]['primitive_multiplicity'] = int(tokens[2])
                    self.lib[tokens[3]]['short_name'] = tokens[3]
                    self.lib[tokens[3]]['point_group'] = tokens[4]
                    self.lib[tokens[3]]['crystal_system'] = tokens[5]
                    self.lib[tokens[3]]['long_name'] = tokens[6]
                    if len(tokens) > 7:
                        self.lib[tokens[3]]['long_name_alternative'] = tokens[7]
                    self.lib[int(tokens[0])] = self.lib[tokens[3]] # index as well by space group number
                    
                    if tokens[4] in point_groups:
                        parse_pg = False
                        self.lib[tokens[3]]["hkl_operations"] = point_groups[tokens[4]]
                    else:
                         parse_pg = True
                else:
                    #body
                    self.lib[tokens[3]]["xyz_operations"].append(line.strip())
                    if parse_pg:
                        point_groups[tokens[4]].append(line.strip())
                        self.lib[tokens[3]]["hkl_operations"].append(line.strip())
        
    
    def point_group_operations(self,space_group_name_or_number):
        '''
        @param point_group_name: E.g. P212121
        
        Return Point group equivalent reflections symetry operations
        
        A monoclinic crystal, has the Laue symmetry of 2/m. The equivalent coordinates, assuming a b-unique axis, 
        are given as (x, y, z), (-x, y, -z), (-x, -y, -z), and (x, -y, z). Thus the intensities of the (h k l), (h k l), (h k l), and (h k l)
        lattice points should have equivalent values. Note that this also means that the intensities of the (h k l), (h k l), (h k l), and (h k l) 
        should also be equivalent to each other but are not necessarily equivalent to (h k l), etc.
        '''
        return self.lib[space_group_name_or_number]["hkl_operations"]
    
    def details(self,space_group_name_or_number):
        return self.lib[space_group_name_or_number]
    
        
    def equivalent_reflections(self,hkl,space_group):
        '''
        '''
        h,k,l = hkl
    
        
        ops = self.point_group_operations(space_group)
        
        eq_reflections = []
        
        for op in ops:
            op = op.replace('X','%s'%h)
            op = op.replace('Y','%s'%k)
            op = op.replace('Z','%s'%l)
            op = op.replace('--','')
            op_tuple = ast.literal_eval(op)
            op_tuple_bijvoet = tuple([-1*x for x in op_tuple])
            eq_reflections.append(op_tuple)
            eq_reflections.append(op_tuple_bijvoet)
        
        eq_reflections.sort()
        return eq_reflections
    

class Reflections():
    def __init__(self,space_group):
        self.symop = SymOp()
        self.space_group = space_group
        self.reflections =  defaultdict(list)
    
    def __str__(self):
        return pprint.pformat(dict(self.reflections))        
    
    def __len__(self):
        return len(self.reflections.items())
    
    def build_equivalent_reflection_list(self,hkl,i,sigma,d=None):
        
        equivalent_reflections = self.symop.equivalent_reflections(hkl,"P222")    
        self.reflections[equivalent_reflections[0]].append((i,sigma,d))
    
    def get_value_for_refection(self,hkl,index_in_tuple):
        '''
        index_in_tuple: 0 I, 1 Sigma, 2 d
        '''
        values = self.reflections[hkl]
        value = [v[index_in_tuple] for v in values]
        return value
    
    def get_reflection_with_the_most_multiplicity(self):
        lens = {}
        for k,v in self.reflections.iteritems():
            lens[k] = len(v)
        
        import operator
        return max(lens.iteritems(), key=operator.itemgetter(1))[0]
    
    def delete_reflections_below_intensity_treshold(self, treshold):
        for k,v in self.reflections.iteritems():
            for idx,igd in enumerate(v):
                if igd[0] < treshold:
                    print 'delete',k,v
                    del(self.reflections[k])
            
    def delete_reflections_below_i_over_sigma_treshold(self, treshold):
        for k,v in self.reflections.iteritems():
            i_over_sigma = v[0]/v[1]
            if i_over_sigma < treshold:
                del(self.reflections[k])
    
    
def test():
    import pprint
    symop = SymOp()
    #print symop

    pprint.pprint( symop.details("P212121") )
    print symop.point_group_operations(19)
    print symop.point_group_operations("P212121")
    
    assert( symop.point_group_operations(19) == symop.point_group_operations("P212121"))
    
    print symop.equivalent_reflections((2,4,7),"P222")
    
    r = Reflections("P212121")
    # equivalent
    r.build_equivalent_reflection_list((2, 4, 7), 10, 2)
    r.build_equivalent_reflection_list((2, -4, -7), 100, 20)
    r.build_equivalent_reflection_list((-2, -4, 7), 1000, 20)
    
    r.build_equivalent_reflection_list((-1, -4, 7), 200, 20)
    r.build_equivalent_reflection_list((-4, -4, 7), 2000, 20)
    r.build_equivalent_reflection_list((-4, 4, 7), 2200, 20)
    print r
    print r.get_value_for_refection((-2, -4, -7),0)
    
   
    
    
if __name__ == '__main__':
    test()  
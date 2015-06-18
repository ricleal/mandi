import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

from mxdetector.detector import Detector


det = Detector('bank32')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


#
# TODO!
#


ids = found['detid'][(found['bankname'] == bankname)]


are_ids_in_bank = np.in1d(bank_arr[:,0],ids)
bank_found = bank_arr[are_ids_in_bank]

distance_bank_found =  distances[ (found['bankname'] == bankname) ]
x = bank_found[:,1]
y = bank_found[:,2]
#z = bank_found[:,3]
z = found['tof'][(found['bankname'] == bankname)]
distance_bank_found /= distance_bank_found.max() # normalise
volume = distance_bank_found * 200
color = 255 - distance_bank_found * 255

area = np.pi * (200 * volume)**2
mymap = plt.get_cmap("copper")
i = ax.scatter(x, y, z, c=color, s=volume, edgecolor='',cmap=mymap)
fig.colorbar(i) 

ax.set_title(bankname)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('TOF')

plt.show()
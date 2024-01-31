import sys
import numpy as np
from ploos.Poscar import POSCAR as PP
from scipy.linalg import solve

#m = np.array( 
# [[ 0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0, -1.0,
#     0.0,  0.0,  0.0, -1.0, 0.0],
#  [ 0.0,  0.0,  2.0, -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0, -2.0,  1.0,
#      0.0,  0.0,  0.0,  1.0, 0.0],
#  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  1.0,  0.0],
#  [ 0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
#  [ 1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0],
#  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  0.0,  0.0],
#  [ 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0],
#  [ 0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0],
#  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,
#      0.0, 1.0,  0.0,  0.0,  1.0], #Qpz
#  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0],
#  [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0],
#  [ 0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
#  [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0],
#  [ 0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0],
#  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0],
#  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
#    -1.0,  0.0,  0.0,  0.0,  1.0],
#  [ 1.0,  0.0,  0.0,  0.0,  0.0,  -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
#    0.0,   1.0,  0.0,  0.0,  0.0],
#  [ 0.0,  -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,
#      0.0,  0.0,  0.0,  0.0,  -1.0]], dtype=np.float64 )
m = np.array( 
 [[ 0.0,  0.0,  1.0,  1.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0, -1.0,
     0.0,  0.0,  0.0, -1.0, 0.0], #Q1
  [ 0.0,  0.0,  2.0, -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0, -2.0,  1.0,
      0.0,  0.0,  0.0,  1.0, 0.0], #Q3
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0, -1.0,
   0.0,  0.0,  0.0,  1.0,  0.0], #Q2
  [ 0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,
   0.0,  0.0,  0.0,  0.0, -1.0], #Qyz
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
   0.0, -1.0,  0.0,  0.0,  0.0], #Qxz
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   -1.0,  0.0, -1.0,  0.0,  0.0], #Qxy
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  1.0,  0.0,  0.0], #Q'x
  [ 0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,
   1.0,  0.0,  0.0,  0.0,  0.0], #Q'y
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,
      0.0, 1.0,  0.0,  0.0,  1.0], #Q'z
  [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,
   0.0,  0.0,  0.0,  0.0,  0.0], #Q''x
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  0.0,  1.0,  0.0], #Q''y
  [ 0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,
   0.0,  0.0,  0.0,  0.0,  0.0], #Q''z
  [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
   0.0,  0.0,  1.0,  0.0,  0.0], #Q'xy
  [ 0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,
   -1.0,  0.0,  0.0,  0.0,  0.0], #Q'yz
  [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,
   0.0,  1.0,  0.0,  0.0, -1.0], #Q'xz
  [ 0.0,  -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0,  0.0,  0.0,
      0.0,  0.0,  0.0,  0.0,  -1.0], # Qryz
  [ 1.0,  0.0,  0.0,  0.0,  0.0,  -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0,
    0.0,   1.0,  0.0,  0.0,  0.0], # Qrxz
  [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   -1.0,  0.0,  1.0,  0.0,  0.0]], #Qrxy
             dtype=np.float64 )



m[0]    *= 1/np.sqrt(6)
m[1]    *= 0.5/np.sqrt(3)
m[2:9]  *= 0.5
m[9:12] *= 1.0/np.sqrt(2)
m[12:]  *= 0.5

c45 = np.cos(0.25*np.pi)
s45 = np.sin(0.25*np.pi)

def calculate_Q(pp, OsRef, cooref, octamode):
    if (octamode == 'tetragonal'):
        oc = pp.octahedron(OsRef)
    else:
        oc = pp.octahedron_cubic(OsRef)
    # library gives octahedron in van Vleck convention
    # go to Bersuker convention
    oc_b = np.roll(oc, 1)
    tmp = oc_b[0]
    oc_b[0] = oc_b[3]
    oc_b[3] = tmp
    coodist = np.array( [pp.getBondLength(o, OsRef)[1] for o in oc_b] )
    rot = np.array( [[c45, s45, 0], [-s45, c45, 0], [0, 0, 1]] )
    if (octamode == 'tetragonal'):
        for i, x in enumerate(coodist):
            coodist[i] = rot @ x
    tmp = coodist - cooref
    return m @ tmp.flatten()

octamode = sys.argv[1]
pref = PP( sys.argv[2] )
pdist = PP( sys.argv[4] )

# octahedron ref
OsRef = int( sys.argv[3] )
oc = pref.octahedron_cubic(OsRef)

# library gives octahedron in van Vleck convention
# go to Bersuker convention
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
cooref = np.array( [pref.getBondLength(o, OsRef)[1] for o in oc_b] )

OsRef = int( sys.argv[5] )
if (octamode == 'cubic'):
    oc = pdist.octahedron_cubic(OsRef)
elif (octamode == 'tetragonal'):
    oc = pdist.octahedron(OsRef)
else:
    print( 'octahedron not implemented for this cell symm' )
    exit(-1)
oc_b = np.roll(oc, 1)
tmp = oc_b[0]
oc_b[0] = oc_b[3]
oc_b[3] = tmp
coodist = np.array( [pdist.getBondLength(o, OsRef)[1] for o in oc_b] )
Qdist = calculate_Q(pdist, OsRef, cooref, octamode)
if (len(sys.argv) == 6):
    for x in np.round( Qdist, 5):
        print(f"{x}",end=' ')
    print()
else:
    mode = int(sys.argv[6])
    print( np.round(Qdist[mode], 7) )

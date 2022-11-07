import sys, re
from ploos import Incar, PlotGUI
from ploos.Parser import *
import numpy as np
from PyQt5.QtWidgets import QApplication

label_ispin1 = [ 'all', 's', 'p', 'd']
label_ispin1_lm = [ 'all', 's', 'px', 'py', 'pz', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2' ]
label_ispin2 = [ 'all', 's+', 's-', 'p+', 'p-', 'd+', 'd-' ]
label_ispin2_lm = [ 'all', 's+', 'px+', 'py+', 'pz+', 'dxy+', 'dyz+', 'dz2+', 'dxz+', 'dx2+', 
        's-', 'px-', 'py-', 'pz-', 'dxy-', 'dyz-', 'dz2-', 'dxz-', 'dx2-' ]
label_ncl = [ 'all', 'stot' , 's(mx)', 's(my)', 's(mz)', 'ptot', 'p(mx)', 'p(my)', 'p(mz)', 
        'dtot', 'd(mx)', 'd(my)', 'd(mz)' ]
label_ncl_lm = [ 'all', 'stot', 's(mx)', 's(my)', 's(mz)', 'pxtot', 'px(mx)', 'px(my)', 'px(mz)', 
        'pytot', 'py(mx)', 'py(my)', 'py(mz)', 'pztot', 'pz(mx)', 'pz(my)', 'pz(mz)', 
        'dxytot', 'dxy(mx)', 'dxy(my)', 'dxy(mz)', 'dyztot', 'dyz(mx)', 'dyz(my)', 'dyz(mz)',
        'dz2tot', 'dz2(mx)', 'dz2(my)', 'dz2(mz)', 'dxztot', 'dxz(mx)', 'dxz(my)', 'dxz(mz)',
        'dx2tot', 'dx2(mx)', 'dx2(my)', 'dx2(mz)' ]


# discarding energy column
# l=0 lm=f ncl=f isp=1 ncol=1
# l=0 lm=f ncl=f isp=2 ncol=2
# l=0 lm=f ncl=t       ncol=3
# l=0 lm=t ncl=f isp=1 ncol=1
# l=0 lm=t ncl=f isp=2 ncol=2
# l=0 lm=t ncl=t       ncol=3
# l=1 lm=f ncl=f isp=1 ncol=2
# l=1 lm=f ncl=f isp=2 ncol=4
# l=1 lm=f ncl=t       ncol=6
# l=1 lm=t ncl=f isp=1 ncol=4
# l=1 lm=t ncl=f isp=2 ncol=8
# l=1 lm=t ncl=t       ncol=17
# l=2 lm=f ncl=f isp=1 ncol=4
# l=2 lm=f ncl=f isp=2 ncol=8
# l=2 lm=f ncl=t       ncol=15
# l=2 lm=t ncl=f isp=1 ncol=9
# l=2 lm=t ncl=f isp=2 ncol=18
# l=2 lm=t ncl=t       ncol=38

def todic(labelarray):
    return { x : i for i, x in enumerate(labelarray) }

def read_total_dos(raw_doscar, nedos, ispin):
    counter = 6
    energy = np.empty( nedos, dtype=float )
    if ( ispin != 2 ):
        dos = np.empty( nedos, dtype=float )
        cdos = np.empty( nedos, dtype=float )
        for i in range( nedos ):
            energy[i], dos[i], cdos[i] = (float(x) for x in split( raw_doscar[counter+i] ))
        return energy, dos, cdos
    else:
        dos_up = np.empty( nedos, dtype=float )
        dos_down = np.empty( nedos, dtype=float )
        for i in range( nedos ):
            energy[i], dos_up[i], dos_down[i] = (float(x) for x in split(
                raw_doscar[counter+i] )[:3])
        return energy, dos_up, dos_down

def read_projected_dos(raw_doscar, nedos, natoms):
    counter = 6 + nedos
    # skip header
    counter += 1
    ncol = len( split( raw_doscar[nedos+7] ) ) - 1 # remove one col for energies
    pldos = np.empty( (natoms, nedos, ncol), dtype=float )
    for i in range( natoms ):
        for j in range( nedos ):
            pldos[i,j] = np.array( [float(x) for x in split( raw_doscar[counter] )[1:] ] )
            counter += 1
        # skip header
        counter += 1
    return pldos, ncol

class DOSCAR:
    ##### COSNTRUCTOR #####
    def __init__(self):
        pass

    def __init__(self, path, efermi=None):
        self.incar = Incar.INCAR( path+'/INCAR' )
#        ispin=0
#        ncl = parse_yn_bool( input('Non-collinear?(y/n): ') )
#        if not ncl: ispin = int( input('ISPIN >> ') )
#        lm = parse_yn_bool( input('lm-decomposed dos?(y/n): ') )
        with open( path+'/DOSCAR', 'r' ) as f:
            doscar = f.readlines()

        self.natoms, _, pdos, _ = [int(n) for n in split( doscar[0] )]
        self.atoms = [str(i) for i in range(1, self.natoms+1)]
        vol, a, b, c, potim = [float(n) for n in split( doscar[1] )]
        tebeg = float( remove_all_whitespace( doscar[2] ) )
        system = remove_all_whitespace( doscar[4] )
        emax, emin, nedos, self.efermi, _ = [float(n) for n in split( doscar[5] )]
        self.nedos = int(nedos)
        self.enableProjector = len(doscar) > self.nedos+7
        counter = 6

        if ( self.incar.ispin != 2 ):
            self.energy, self.dos, self.cdos = read_total_dos( doscar, self.nedos,
                    self.incar.ispin )
        else:
            self.energy, self.dos_up, self.dos_down = read_total_dos( doscar,
                    self.nedos, self.incar.ispin )

        #self.dos /= vol
        if efermi is None:
            self.energy -= self.efermi
        else:
            self.energy -= efermi

        if ( self.enableProjector ):
            self.pldos, ncol = read_projected_dos( doscar, self.nedos, self.natoms )
            # Extract labels
            ncol += 1 # add one col for all
            lm = self.incar.lorbit == 11 or self.incar.lorbit == 1
            global label_ispin1_lm, label_ispin1, label_ispin2_lm, label_ispin2, label_ncl_lm, label_ncl
            if ( self.incar.ispin==1 ):
                if ( lm ): self.guiLabel = label_ispin1_lm[:ncol] 
                else: self.guiLabel = label_ispin1[:ncol]
            elif ( self.incar.ispin==2 ):
                if ( lm ): self.guiLabel = label_ispin2_lm[:ncol]
                else: self.guiLabel = label_ispin2[:ncol]
            elif ( self.incar.ncl ):
                if ( lm ): 
                    self.guiLabel = label_ncl_lm[:ncol]
                else: self.guiLabel = label_ncl[:ncol]
            else: exit('\nUnrecognised structure. Aborting...\n')
            self.label = todic( self.guiLabel )
    ##############################  


    ##### PROJECTOR #####
    def projector(self, atoms, orbitals):
        m = re.compile(r'm')
        projected = np.zeros(self.nedos)
        for aa in atoms:
            atom_index = int(aa)-1
            if len(orbitals) == 1 and orbitals[0] == 'all':
                if self.incar.ncl:
                    tmp = [i-1 for i, label in enumerate(self.guiLabel) if not m.search(label) and label != 'all']
                    for i in tmp:
                        projected += self.pldos[ atom_index, :, i ]
            for oo in orbitals:
                projected += self.pldos[ atom_index, :, self.label[oo]-1 ]
        return projected
    ############################## 

    def sum_in_energy_interval(self, poscar_atom, emin, emax):
        tmp = np.zeros(self.energy.shape)
        iat = poscar_atom - 1
        de = self.energy[1] - self.energy[0]
        for i, e in enumerate(self.energy):
            if ( e+self.efermi >= emin and e <= emax ):
                tmp[i] = sum(self.pldos[iat, i, :])
        return np.trapz(tmp, self.energy)



    ##### PLOTTER #####
    def plot(self):
        app = QApplication(sys.argv)
        form = PlotGUI.App(self)
        form.show()
        app.exec_()

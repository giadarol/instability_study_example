import os
import sys
import numpy as np
sys.path.append('../')

import PyECLOUD.myfilemanager as mfm

dirs = os.listdir('simulations_PyPARIS/')

lsuccess = []

for dd in dirs:
    try:
        # Check that the simulation is complete
        status_fname = 'simulations_PyPARIS/'+dd+'/simulation_status.sta'
        sta = {}
        with open(status_fname, 'r') as fid:
            exec(fid.read(), sta)
        
        assert(sta['present_part_done'])
        
        # Check that output files are not corrupted
        bunch_fname = 'simulations_PyPARIS/'+dd+'/bunch_evolution_00.h5'
        bmon = mfm.monitorh5_to_obj(bunch_fname)
        slice_fname = 'simulations_PyPARIS/'+dd+'/slice_evolution_00.h5'
        smon = mfm.monitorh5_to_obj(slice_fname, key='Slices')
        
        mean_x_from_slice = \
            np.sum(smon.mean_x * smon.n_macroparticles_per_slice, axis=0) \
            /np.sum(smon.n_macroparticles_per_slice, axis=0)

        mean_x_from_slice[bmon.macroparticlenumber<1] = 0.    

        assert(np.max(mean_x_from_slice - bmon.mean_x) <1e7)
        success = True
    except:
        success = False

    lsuccess.append(success)


n_success = np.sum(lsuccess)
print('Successful: %d/%d'%(n_success, len(dirs)))

with open('check.txt', 'w') as fid:
    fid.write('Successful: %d/%d\n'%(n_success, len(dirs)))



import os
import shutil as sht
import numpy as np

import replaceline as rl


tag_prefix = 'blkd2_'

# Parameter of bunch and machine of interest
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
betay_vect = [50., 100., 150., 200., 300., 400., 500., 600.]

fraction_device_quad_vect = [0.26]

n_slices_vect = [250]

# Multigrid Parameters
PyPICmulti = 'ShortleyWeller_WithTelescopicGrids'
PyPICsingle = 'FiniteDifferences_ShortleyWeller'
PyPICmode_vect= [PyPICmulti]
PyPICmode_tag_vect= ['Tblocked']

Dh_sc_ext_vect = [0.4e-3]
N_min_Dh_main_vect = [-1]
f_telescope_vect = [0.3]
target_size_internal_grid_sigma_vect = [10]
target_Dh_internal_grid_sigma_vect = [-2]
N_nodes_discard_vect = [8.]

n_cores = 8
ask_for_n_times = 1

parallel_mode = 'multiproc'
cluster = 'cnaf_acc'


if cluster == 'lxplus':
    cluster_specific = {}
    cluster_specific['queue'] = 'spacecharge'
    cluster_specific['setup_env_source'] = 'setup_env_lxplus; export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/contrib/gcc/4.8.1/x86_64-slc6-gcc48-opt/lib64; source /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/virtualenvs/py2.7/bin/activate'
    #~ cluster_specific['setup_env_source'] = 'setup_env_lxplus'
    cluster_specific['mpiex'] = 'to_be_installed'
elif cluster == 'cnaf':
    cluster_specific = {}
    cluster_specific['queue'] = 'hpc_56inf'
    cluster_specific['setup_env_source'] = 'setup_env_cnaf'
    cluster_specific['mpiex'] = 'mpiexec'
elif cluster == 'cnaf_acc':
    cluster_specific = {}
    cluster_specific['queue'] = 'hpc_acc'
    cluster_specific['setup_env_source'] = 'setup_env_cnaf'
    cluster_specific['mpiex'] = 'mpiexec'
elif 'None':
    cluster_specific = {}
    cluster_specific['queue'] = 'None'
    cluster_specific['setup_env_source'] = ''
    cluster_specific['mpiex'] = ''


exec_string = {}
exec_string['multiproc'] = 'python ../../../PyPARIS/multiprocexec.py -n %d'
exec_string['mpi'] = cluster_specific['mpiex'] + ' -n %d ../../../PyPARIS/withmpi.py'
#~ exec_string['multiproc'] = 'python /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/PyPARIS/multiprocexec.py -n %d'
#~ exec_string['mpi'] = cluster_specific['mpiex'] + ' -n %d /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/PyPARIS/withmpi.py'


current_dir = os.getcwd()
study_folder =  current_dir.split('/config')[0]

scan_folder = study_folder+'/simulations_PyPARIS'

#debug
#sht.rmtree(scan_folder)

os.mkdir(scan_folder)

launch_file_lines = []
launch_file_lines +=['#!/bin/bash\n']

onoff = {False: 'OFF', True: 'ON'}
prog_num = 0

for PyPICmode, PyPICmode_tag, Dh_sc_ext, N_min_Dh_main, f_telescope, target_size_internal_grid_sigma, target_Dh_internal_grid_sigma, N_nodes_discard in zip(PyPICmode_vect, PyPICmode_tag_vect, Dh_sc_ext_vect, N_min_Dh_main_vect, f_telescope_vect, target_size_internal_grid_sigma_vect, target_Dh_internal_grid_sigma_vect, N_nodes_discard_vect):
	
	for betax, betay in zip(betax_vect, betay_vect):
		for fraction_device_quad in fraction_device_quad_vect:
			for n_slices in n_slices_vect:
				
				prog_num +=1

				current_sim_ident= 'transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)                       
				sim_tag = tag_prefix+'%04d'%prog_num


				print (sim_tag, current_sim_ident)
				current_sim_folder = scan_folder+'/'+current_sim_ident
				os.mkdir(current_sim_folder)

				os.system('cp -r sim_prototype/* %s'%current_sim_folder)
				
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'PyPICmode = ', 
									newline = 'PyPICmode = \'%s\''%PyPICmode)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'N_min_Dh_main = ', 
									newline = 'N_min_Dh_main = %.1f'%N_min_Dh_main)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'Dh_sc_ext = ', 
									newline = 'Dh_sc_ext = %.6f'%Dh_sc_ext)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'f_telescope = ', 
									newline = 'f_telescope = %.1f'%f_telescope)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'target_size_internal_grid_sigma = ', 
									newline = 'target_size_internal_grid_sigma = %.1f'%target_size_internal_grid_sigma)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'target_Dh_internal_grid_sigma = ', 
									newline = 'target_Dh_internal_grid_sigma = %.1f'%target_Dh_internal_grid_sigma)
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'N_nodes_discard = ', 
									newline = 'N_nodes_discard = %.1f'%N_nodes_discard)	
				
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'beta_x = ', 
									newline = 'beta_x = %.1f'%betax)									
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'beta_y = ', 
									newline = 'beta_y = %.1f'%betay)
									
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'fraction_device_quad = ', 
									newline = 'fraction_device_quad = %.2f'%fraction_device_quad)
									
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'n_slices = ', 
									newline = 'n_slices = %d'%n_slices) 					
				

				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -J',
					 newline = '#BSUB -J %s\n'%sim_tag)	
					 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -n',
					 newline = '#BSUB -n %d\n'%(n_cores*ask_for_n_times))	

				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
						 findln = '#BSUB -R',
						 newline = '#BSUB -R span[ptile=%d]\n'%(n_cores*ask_for_n_times))
						 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -q',
					 newline = '#BSUB -q %s\n'%cluster_specific['queue'])	   
						 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = 'CURRDIR=',
					 newline = 'CURRDIR=%s\n'%current_sim_folder)
					 
					 
				#~ rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
						 #~ findln = 'source ',
						 #~ newline = 'source ./%s\n'%cluster_specific['setup_env_source'])
				  
				  
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
						 findln = 'stdbuf -oL ',
						 newline = 'stdbuf -oL '+ exec_string[parallel_mode]%n_cores+\
						 ' sim_class=Simulation.Simulation >> opic.txt 2>> epic.txt\n')
				
				launch_file_lines += ['cd ' + current_sim_folder+'\n',
							'bsub < job.cmd\n',
							'cd ..\n']

				with open(current_sim_folder+'/launch_this', 'w') as fid:
					fid.writelines(['#!/bin/bash\n','bsub < job.cmd\n'])

				with open(current_sim_folder+'/opic.txt', 'w') as fid:
					fid.writelines([''])

				with open(current_sim_folder+'/epic.txt', 'w') as fid:
					fid.writelines([''])

                                

with open(study_folder+'/run_PyPARIS', 'w') as fid:
	fid.writelines(launch_file_lines)
os.chmod(study_folder+'/run_PyPARIS',0o755)

import htcondor_config as htcc
htcc.htcondor_config(scan_folder, time_requirement_days=2., runfilename='../run_PyPARIS_htcondor', 
                    n_cores=n_cores, job_filename = 'job.cmd', htcondor_subfile='htcondor_PyPARIS.sub',
                    listfolderfile = 'list_sim_folders_PyPARIS.txt')





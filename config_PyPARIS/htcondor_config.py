import os


def htcondor_config(scan_folder, time_requirement_days, job_filename = 'job.job', 
                        runfilename='../run_htcondor', n_cores=1, htcondor_subfile='htcondor.sub',
                        listfolderfile = 'list_sim_folders.txt'):
    
    list_folders= os.listdir(scan_folder)
    with open('../%s'%listfolderfile, 'w') as fid:
        for folder in list_folders:
            if os.path.isfile(scan_folder+'/'+folder+'/'+job_filename):
                print(folder, file=fid)

    with open('../'+htcondor_subfile, 'w') as fid:
        print("universe = vanilla", file=fid)
        print("executable = "+ scan_folder+"/$(dirname)/"+job_filename, file=fid)
        print('arguments = ""', file=fid)
        print("output = "+ scan_folder+'/$(dirname)/htcondor.out', file=fid)
        print("error = "+scan_folder+"/$(dirname)/htcondor.err", file=fid)
        print("log = "+scan_folder+"/$(dirname)/htcondor.log", file=fid)
        print('transfer_output_files = ""', file=fid)
        print("+MaxRuntime = %d"%(time_requirement_days*24*3600), file=fid)
        print("requestCpus = %d"%(n_cores), file=fid)
        print("max_retries = 0", file=fid)
        print("queue dirname from %s"%listfolderfile, file=fid)
    
    with open(runfilename, 'w') as fid:
        print('condor_submit %s'%htcondor_subfile, file=fid)
        print('condor_q --nobatch', file=fid)
    os.chmod(runfilename,0o755)

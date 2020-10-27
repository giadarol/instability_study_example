#!/bin/bash

#BSUB -J blkd_0001
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -N
#BSUB -B
#BSUB -q hpc_acc
#B -a openmpi
#BSUB -n 16
#BSUB -R span[ptile=16]

CURRDIR=TBD
cd $CURRDIR
pwd

source ../../../miniconda3/bin/activate
which python

export PYFRIENDSPATH=../../../
export PYTHONPATH=$PYTHONPATH:$PYFRIENDSPATH

cd ../../PyPARIS_sim_class
echo "Version:"          >  ../SimClass_git_info.txt
cat __version__.py       >> ../SimClass_git_info.txt
echo " "                 >> ../SimClass_git_info.txt
echo "git status:"       >> ../SimClass_git_info.txt
git status               >> ../SimClass_git_info.txt
echo "git log -n 1:"     >> ../SimClass_git_info.txt
git log -n 1             >> ../SimClass_git_info.txt

cd $CURRDIR
cp ../../PyPARIS_sim_class/Simulation.py .

stdbuf -oL python -m PyPARIS.multiprocexec -n 16 sim_class=Simulation.Simulation >> opic.txt 2>> epic.txt

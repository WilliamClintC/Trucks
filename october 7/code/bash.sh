#!/bin/bash -l

#$ -P trucks          # Specify the SCC project name you want to use
#$ -l h_rt=12:00:00   # Specify the hard time limit for the job
#$ -N Wills_job     # Give job a name
#$ -j y               # Merge the error and output streams into a single file
#$ -m beas            # Send email when the job starts/finishes/aborts
#$ -t 1-57          # Submit an array job with 1 tasks 
#$ -pe omp 1        # Request 1 core for my job

# clear modules loaded in user's .bashrc
module purge

# Load the required modules
module load python3/3.10.12 

source /restricted/projectnb/trucks/venvs/wills_env/bin/activate


python sectioner.py $SGE_TASK_ID

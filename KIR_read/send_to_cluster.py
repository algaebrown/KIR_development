def new_slurm_script(script_name, cpus_per_task='1', mem_per_cpu='5G', array_t='1-9000', array_tc='250'):



    
    with open(script_name, 'w') as f:
        f.write('''
#! /bin/bash
        
#SBATCH --job-name={0}
#SBATCH --output={0}.out
#SBATCH --error={0}.error
#SBATCH --cpus-per-task={1}
#SBATCH --mem-per-cpu={2}
#SBATCH --array={3}%{4}

'''.format(script_name, cpus_per_task, mem_per_cpu, array_t, array_tc))


def map_slurm_task_id(script_name, file_list, var_name):

    # generate file list with ' '
    file_list_str = ' '.join(file_list)


    with open(script_name, 'a') as f:
        f.write('''
{0}s=({1})
{0}=${{{0}s[$SLURM_ARRAY_TASK_ID -1]}}
'''.format(var_name, file_list_str))

def slurm_bedtools(short_id_list, script_name):

    new_slurm_script(script_name)
    map_slurm_task_id(script_name, short_id_list, 'short_id')

    with open(script_name, 'a') as f:
        f.write('''
bash /cellar/users/hsher/KIR_development/KIR_read/run_bedtool.sh ${0}


'''.format('short_id'))

    
        
    

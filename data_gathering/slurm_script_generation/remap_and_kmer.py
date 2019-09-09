from slurm import new_slurm_script, map_slurm_task_id

def remap(script_name,
          sample_list,
          sample_name,
          samtools_path = '/cellar/users/hcarter/programs/samtools-1.2/samtools',
          
):

    # initialize
    new_slurm_script(script_name, mem_per_cpu = '8G', array_tc = '30')

    # the params

    # use SAMTOOLS to pull KIR region
    with open(script_name, 'a') as f:
        f.write("""
{0} 

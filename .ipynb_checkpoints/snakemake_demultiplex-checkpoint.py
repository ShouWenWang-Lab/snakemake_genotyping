import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

#configfile: "config.yaml"  # command line way to set it: --configfile 'path/to/config'
#workdir: config['data_dir'] # set working directory, a command-line way to set it: --directory 'path/to/your/dir'
config['data_dir']=str(os.getcwd())
script_dir=config['script_dir']
recompute=config['recompute']
N_donor=config['N_donor']

##################
## preprocessing
################## 

SampleList=config['SampleList']
print(f'SampleList: {SampleList}')

# remove the flag file of the workflow if the sbatch is not actually run to finish
valid_SampleList=os.listdir('count')
for sample in SampleList:
    if sample not in valid_SampleList:
        raise ValueError(f"{sample} is not a valid sample. Should be among {valid_SampleList}")
        
        
##################
## start the rules
################## 
rule all:
    input: 
        expand("count/{sample}/outs/cell_demultiplex/run_vireo.done",sample=SampleList),
        
rule run_demultiplex:
    input:
        in_dir="count/{sample}/outs/cell_genotyping/run_cellsnp.done"
    output:
        touch("count/{sample}/outs/cell_demultiplex/run_vireo.done"),
    run:
        out_dir=f"count/{wildcards.sample}/outs/cell_demultiplex"
        os.makedirs(out_dir,exist_ok=True)
        input_dir=f'count/{wildcards.sample}/outs/cell_genotyping'
        command=f"sh {script_dir}/genetic_demultiplexing.sh {input_dir} {N_donor} {out_dir}"
        time=config['demultiplex']['max_run_time']
        mem=config['demultiplex']['requested_memory']
        cores=config['demultiplex']['cores']
        mode=config['demultiplex']['sbatch_mode']
        job_name=f'vireo_{wildcards.sample}'
        if config['sbatch']==0:
            print("Run on terminal directly")
            os.system(command)
        else:
            os.system(f"python {script_dir}/run_sbatch.py --sbatch_mode {mode} --job_name {job_name} --cores {cores} --mem {mem} --time {time} --command '{command}' ") # we use ' in '{command}' to avoid bash expansion
            
            
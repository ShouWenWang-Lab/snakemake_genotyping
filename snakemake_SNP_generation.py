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
SNP_feature_dir=config['SNP_feature_dir']

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
        expand("count/{sample}/outs/cell_genotyping/run_cellsnp.done",sample=SampleList),
        
rule run_cellsnp:
    input:
        file_1="count/{sample}/outs/possorted_genome_bam.bam",
        file_2="count/{sample}/outs/possorted_genome_bam.bam.bai",
        file_3="count/{sample}/outs/filtered_feature_bc_matrix/barcodes.tsv.gz",
    output:
        touch("count/{sample}/outs/cell_genotyping/run_cellsnp.done"),
    run:
        os.system(f'gzip -d -c  {input.file_3}  > count/{wildcards.sample}/outs/filtered_feature_bc_matrix/barcodes.tsv')
        out_dir=f"count/{wildcards.sample}/outs/cell_genotyping"
        os.makedirs(out_dir,exist_ok=True)
        input_dir='count'
        command=f"sh {script_dir}/generate_snp_count_matrices.sh {input_dir} {wildcards.sample} {SNP_feature_dir}"
        time=config['SNP']['max_run_time']
        mem=config['SNP']['requested_memory']
        cores=config['SNP']['cores']
        mode=config['SNP']['sbatch_mode']
        job_name=f'snp_{wildcards.sample}'
        if config['sbatch']==0:
            print("Run on terminal directly")
            os.system(command)
        else:
            os.system(f"python {script_dir}/run_sbatch.py --sbatch_mode {mode} --job_name {job_name} --cores {cores} --mem {mem} --time {time} --command '{command}' ") # we use ' in '{command}' to avoid bash expansion
            
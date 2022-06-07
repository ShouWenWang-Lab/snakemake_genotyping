# snakemake_genotyping
As it stands now, it will only work for people using HMS-o2. 

## Preparation
1, First, you need to prepare the environment `snakemake`
```bash
conda install -n base -c conda-forge mamba --yes
conda activate base
mamba create -c conda-forge -c bioconda -n snakemake snakemake
conda activate snakemake
pip install --user ipykernel
pip install jupyterlab umi_tools seaborn papermill biopython
python -m ipykernel install --user --name=snakemake
```

2, Then, start the environment
```bash
conda activate snakemake
```

3, We assume that the RNA-seq data is output by the 10X software cellranger. Now, go to the data folder (at the same level as the *count* folder), create a config.yaml file here: 

```yaml
script_dir: '/n/groups/klein/shouwen/lili_project/packages/snakemake_genotyping/source'
SampleList: ['Undifferentiated'] #'Differentiated-2','Differentiated-3'] #,] # 'Differentiated-1'] #,] # the fastq files should be named as f'{Sample}_S1_L001_R1_001.fastq.gz'
sbatch : 1 # 1, run sbatch job;  0, run in the interactive mode. If set to be 1, expect error from file latency, as the sbatch job would take a while to finish
SNP:
    max_run_time : 36 # finished around 5 hours for AFe2 (default 8)
    requested_memory : '40G' # checked that 5G is enough for  AFe2 (default 5G)
    cores: 8
    sbatch_mode: 'medium' # short, or medium
demultiplex:
    max_run_time : 4 
    requested_memory : '15G' 
    cores: 8
    sbatch_mode: 'short'
RNA:
    protocol: '10X'
    max_run_time : 12 # last time used 7.3 hours
    requested_memory : '50G' # last time used 15G for 10X, for 50G should be safe.
    cores: 10  # CPU per task
    sbatch_mode: 'short'
    reference: 'GRCh38' # ['mm10' or 'GRCh38'] for 10X
fastq_dir: 'fastq/Klein_Novartis' #relative path to current dir
recompute : 0
N_donor: 10
SNP_feature_dir: '/n/groups/klein/shouwen/lili_project/Katie_lung/SNP_reference/genome1K.phase3.SNP_AF5e4.chr1toX.hg38.vcf.gz' #'/n/groups/klein/shouwen/lili_project/Katie_lung/SNP_reference/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf.gz'
```

## Run snakemake
Go to the root directory of a 10X data folder, and run snakemake. Usually, the snakemake pipeline submit jobs to o2 (if `sbatch=1` in the config.yaml file), and this could take a while to finish. Please talk to Shouwen for more details. 

If the RNA count matrix is not generated, run
```bash
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_multiomics/snakefile_RNA.py --configfile config.yaml  --config script_dir=/n/groups/klein/shouwen/lili_project/packages/snakemake_multiomics/source --cores 1 
```

Then, generate the SNP matrix with
```bash
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_genotyping/snakemake_SNP_generation.py --configfile config.yaml  --cores 4 
```

Finally, demultiplex the cells with
```bash
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_genotyping/snakemake_demultiplex.py --configfile config.yaml  --cores 4 
```


## Example data directory and config.yaml files
An real example is here `/n/groups/klein/shouwen/lili_project/Katie_lung/DATA/20220403`
```bash
cd /n/groups/klein/shouwen/lili_project/Katie_lung/DATA/20220403
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_multiomics/snakefile_RNA.py --configfile config.yaml  --config script_dir=/n/groups/klein/shouwen/lili_project/packages/snakemake_multiomics/source --cores 1 
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_genotyping/snakemake_SNP_generation.py --configfile config.yaml  --cores 4 
snakemake   -s /n/groups/klein/shouwen/lili_project/packages/snakemake_genotyping/snakemake_demultiplex.py --configfile config.yaml  --cores 4 
```
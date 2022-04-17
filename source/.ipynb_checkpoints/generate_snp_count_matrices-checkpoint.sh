
# cellsnp-lite
# See documentation here: https://cellsnp-lite.readthedocs.io/en/latest/manual.html, https://github.com/single-cell-genetics/cellsnp-lite

module purge
module load gcc

#source /home/ng136/miniconda3/etc/profile.d/conda.sh
#conda activate snakemake

data_path=$1
sample_name=$2
SNP_feature_dir=$3

data_folder=$data_path/$sample_name/outs


# Inputs
BAM_PATH="$data_folder/possorted_genome_bam.bam"
WHITELIST="$data_folder/filtered_feature_bc_matrix/barcodes.tsv"
OUTFOLDER="$data_folder/cell_genotyping/"


mkdir -p $data_folder/log
mkdir -p $OUTFOLDER

echo Processing $data_folder
N_CELLS=$(cat ${WHITELIST} | wc -l)
echo Cell_number ${N_CELLS}

cellsnp-lite -s $BAM_PATH -b $WHITELIST -O $OUTFOLDER -R $SNP_feature_dir -p 20 --minMAF 0.1 --minCOUNT 20 --gzip --genotype






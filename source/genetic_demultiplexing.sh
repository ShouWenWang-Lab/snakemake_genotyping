
# VIREO
# See documentation here: https://vireosnp.readthedocs.io/en/latest/manual.html

module purge
module load gcc


CELLSNP_OUTPUT=$1
N_DONORS=$2
VIREO_OUTPUT=$3


# # Inputs
# CELLSNP_OUTPUT="/home/ng136/nico/hca/magenta_data/210921_A00794_0494_BHNCMWDSX2_SUB11348/count/Nico_10X_SCC_${i}/outs/cell_genotyping/"
# VIREO_OUTPUT="/home/ng136/nico/hca/magenta_data/210921_A00794_0494_BHNCMWDSX2_SUB11348/count/Nico_10X_SCC_${i}/outs/snp_demux/"


#echo Processing Nico_10X_SCC_${i} \(${N_DONORS} donors\)

vireo -c $CELLSNP_OUTPUT -N $N_DONORS -o $VIREO_OUTPUT



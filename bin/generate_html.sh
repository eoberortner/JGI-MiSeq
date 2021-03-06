#!/bin/sh

usage() {
    echo "Usage: postprocessing.sh LIBRARY_NAME REF_FASTA"
}

if [ "$#" -ne 2 ]; then
    usage
fi

## LOAD MODULES
export _JAVA_OPTIONS="-Xmx2G"
module load oracle-jdk

module load python
module load biopython

HOME_DIR=/global/homes/s/synbio
SEQUENCING_DIR=${HOME_DIR}/sequencing

LIB_DIR=${SEQUENCING_DIR}/lib
PYTHON_DIR=${SEQUENCING_DIR}/python

export PATH=$PATH:${LIB_DIR}/dnassemble-jgi/bin/

LIBRARY_DIR=/global/scratch2/sd/synbio/sequencing/illumina
LIBRARY_NAME=$1

if ! [ -d ${LIBRARY_DIR}/${LIBRARY_NAME} ]; then
    echo "${LIBRARY_DIR}/${LIBRARY_NAME} does not exist."
    usage
fi

REF_FASTA=$2
REF_SEQ=${LIBRARY_DIR}/${LIBRARY_NAME}/${REF_FASTA}

if ! [ -f ${REF_SEQ} ]; then
    echo "${REF_SEQ} does not exist."
    usage
fi

URL_PATH=http://synbio.jgi-psf.org:8077/analysis

## generate HTML
python ${PYTHON_DIR}/summarize_analysis.py --fspath ${LIBRARY_DIR} --urlpath ${URL_PATH} < ${LIBRARY_DIR}/${LIBRARY_NAME}/config.xml

##
## WEB
##

## copy files to web-documents
WEB_DIR=/global/dna/shared/synbio/PacBioAnalysis/

if [ -d ${WEB_DIR}/${LIBRARY_NAME} ]; then
    rm -Rf ${WEB_DIR}/${LIBRARY_NAME}
fi
mkdir ${WEB_DIR}/${LIBRARY_NAME}

cp ${LIBRARY_DIR}/${LIBRARY_NAME}/index.html ${WEB_DIR}/${LIBRARY_NAME}/index.html
cp -r ${LIBRARY_DIR}/${LIBRARY_NAME}/ref ${WEB_DIR}/${LIBRARY_NAME}/ref
cp -r ${LIBRARY_DIR}/${LIBRARY_NAME}/results ${WEB_DIR}/${LIBRARY_NAME}/results
cp -r ${LIBRARY_DIR}/${LIBRARY_NAME}/config.xml ${WEB_DIR}/${LIBRARY_NAME}/config.xml


## TODO:
## for every library, copy the aligned_reads.bam, aligned_reads.bam.bai, call_summary.txt, callable.bed, snps.gatk.vcf, and snps.gatk.vcf.idx
## into the $WEB_DIR

for POOL_NAME in `ls -d *_*_*`;
do
    mkdir ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}
    mkdir ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir

    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/aligned_reads.bam ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/aligned_reads.bam 
    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/aligned_reads.bam.bai ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/aligned_reads.bam.bai

    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/call_summary.txt ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/call_summary.txt
    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/callable.bed ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/callable.bed
    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/snps.gatk.vcf ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/snps.gatk.vcf
    cp ${LIBRARY_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/snps.gatk.vcf.idx ${WEB_DIR}/${LIBRARY_NAME}/${POOL_NAME}/bwa_dir/snps.gatk.vcf.idx 
done


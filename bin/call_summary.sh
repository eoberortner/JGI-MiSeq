#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "No POOL_NAME specified!"
    exit
fi
POOL_NAME=$1

python ${PYTHON_DIR}/make_calls_gatk.py --reffile ${REF_SEQ} --vcffile ${POOL_NAME}/bwa_dir/snps.gatk.vcf --covfile ${POOL_NAME}/bwa_dir/covdepth > ${POOL_NAME}/bwa_dir/call_summary.txt

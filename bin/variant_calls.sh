#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "No POOL_NAME specified!"
    exit
fi
POOL_NAME=$1
java -jar ${LIB_DIR}/GenomeAnalysisTK.jar -T HaplotypeCaller -R ${REF_SEQ} -I ${POOL_NAME}/bwa_dir/aligned_reads.bam -o ${POOL_NAME}/bwa_dir/snps.gatk.vcf

#!/bin/sh

export _JAVA_OPTIONS="-Xmx2G"
module load oracle-jdk

if [ "$#" -ne 1 ]; then
    echo "No POOL_NAME specified!" 
    exit
fi
POOL_NAME=$1

java -jar ${LIB_DIR}/GenomeAnalysisTK.jar -T CallableLoci -R ${REF_SEQ} -I ${POOL_NAME}/bwa_dir/aligned_reads.bam -summary ${POOL_NAME}/call_summary.txt -o ${POOL_NAME}/bwa_dir/callable.bed

module unload oracle-jdk

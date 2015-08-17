#!/bin/sh

export _JAVA_OPTIONS="-Xmx2G"
module load oracle-jdk

if [ "$#" -ne 1 ]; then
    echo "No POOL_NAME specified!"
    exit
fi
POOL_NAME=$1

java -jar ${LIB_DIR}/GenomeAnalysisTK.jar -T DepthOfCoverage -R ${REF_SEQ} -I ${POOL_NAME}/bwa_dir/${POOL_NAME}.bam -o ${POOL_NAME}/bwa_dir/covdepth

module unload oracle-jdk

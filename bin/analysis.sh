#!/bin/sh

usage() {
    echo "Usage: postprocessing.sh LIBRARY_NAME REF_FASTA"
}

if [ "$#" -ne 2 ]; then
    usage
    exit
fi

BIN_DIR=/global/homes/s/synbio/sequencing/bin

source ${BIN_DIR}/setup_env $1 $2
export PATH=$BIN_DIR:$PATH

while IFS= read -r line; do

    stringarray=($line)
    POOL_NAME=${stringarray[0]}
    echo "POOL_NAME: ${POOL_NAME}"

    if [ -f ${POOL_NAME}/bwa_dir/${POOL_NAME}.bam ]; then
        if [ -f ${POOL_NAME}/bwa_dir/aligned_reads.bam ]; then
            echo "${POOL_NAME}/bwa_dir/aligned_reads.bam exists! deleting it!"
            rm -f ${POOL_NAME}/bwa_dir/aligned_reads.bam
        fi
        cp ${POOL_NAME}/bwa_dir/${POOL_NAME}.bam ${POOL_NAME}/bwa_dir/aligned_reads.bam
    fi    

    if [ -f ${POOL_NAME}/bwa_dir/${POOL_NAME}.bam.bai ]; then
        if [ -f ${POOL_NAME}/bwa_dir/aligned_reads.bam.bai ]; then
            echo "${POOL_NAME}/bwa_dir/aligned_reads.bam.bai exists! deleting it!"
            rm -f ${POOL_NAME}/bwa_dir/aligned_reads.bam.bai
        fi
        cp ${POOL_NAME}/bwa_dir/${POOL_NAME}.bam.bai ${POOL_NAME}/bwa_dir/aligned_reads.bam.bai
    fi    

    ## DEPTH OF COVERAGE
    COVERAGE_JOB_ID=`qsub -pe pe_8 16 -l ram.c=2G -V -m e -cwd -o ${OUTPUT_DIR} -e ${OUTPUT_DIR} -M eoberortner@lbl.gov ${BIN_DIR}/depth_of_coverage.sh ${POOL_NAME} | cut -d ' ' -f 3`
    echo "POOL_NAME: ${POOL_NAME} --> depth of coverage: ${COVERAGE_JOB_ID}"

    ## VCF
    VARIANT_CALLS_JOB_ID=`qsub -hold_jid ${COVERAGE_JOB_ID} -pe pe_8 16 -l ram.c=2G -V -m e -cwd -o ${OUTPUT_DIR} -e ${OUTPUT_DIR} -M eoberortner@lbl.gov ${BIN_DIR}/variant_calls.sh ${POOL_NAME} | cut -d ' ' -f 3`
    echo "POOL_NAME: ${POOL_NAME} --> variant calls: ${VARIANT_CALLS_JOB_IB} (waiting for depth of coverage: ${COVERAGE_JOB_ID})"

    ## CALL SUMMARY
    CALL_SUMMARY_JOB_ID=`qsub -hold_jid ${VARIANT_CALLS_JOB_ID} -pe pe_8 16 -l ram.c=2G -V -m e -cwd -o ${OUTPUT_DIR} -e ${OUTPUT_DIR} -M eoberortner@lbl.gov ${BIN_DIR}/call_summary.sh ${POOL_NAME} | cut -d ' ' -f 3`
    echo "POOL_NAME: ${POOL_NAME} --> call summary: ${CALL_SUMMARY_JOB_IB} (waiting for variant calls: ${VARIANT_CALLS_JOB_ID})"
    
    ## CALLABLE
    CALLABLE_JOB_ID=`qsub -hold_jid ${CALL_SUMMARY_JOB_ID} -pe pe_8 16 -l ram.c=2G -V -m e -cwd -o ${OUTPUT_DIR} -e ${OUTPUT_DIR} -M eoberortner@lbl.gov ${BIN_DIR}/callable.sh ${POOL_NAME} | cut -d ' ' -f 3`
    echo "POOL_NAME: ${POOL_NAME} --> callables: ${CALLABLE_JOB_ID} (waiting for call summary: ${CALL_SUMMARY_JOB_ID})"
    
done < libraries.info

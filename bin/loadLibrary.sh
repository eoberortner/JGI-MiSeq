#!/bin/sh

usage() {
    echo "Usage: loadLibrary.sh LIBRARY_NAME REFERENCE_SEQUENCES"
}

if [ "$#" -ne 2 ]; then
    usage
    exit
fi

BIN_DIR=/global/homes/s/synbio/sequencing/bin

## setup environment
source ${BIN_DIR}/env.reseq.sh
source ${BIN_DIR}/setup_env $1 $2

echo ${PYTHON_DIR}

## retrieve names of the sublibraries 
## from the RQC API
python ${PYTHON_DIR}/get_RQC_library_info.py $1

## load libraries
get_dw_info libs2info < sub.libraries.info > pre.libraries.info

## load the libraries fastq files 
## from JAMO
jamo_temp_libinfo_fix pre.libraries.info > libraries.info

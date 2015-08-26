'''
Created on Jul 28, 2015

@author: Ernst Oberortner
'''

import argparse, sys
import subprocess
from rest.RQCInvoker import RQCInvoker
from rest.SDMInvoker import SDMInvoker
import generate_config_xml
import os

BASE_DIR = '/Users/eoberortner/Projects/JGI/Illumina/git/JGI-MiSeq/data/libraries/'
#BASE_DIR = '/global/scratch2/sd/synbio/sequencing/illumina/'

def processArguments(arguments):
    
    ##print 'here are the arguments {}'.format(arguments)
    
    return ('AHPZC', 'ref/427_5415poolsRef.fasta')
#    return ('AHPZB', 'ref/427_5415poolsRef.fasta')
#    return ('AOSPB', 'ref/B64_RBS_Nextera_ref.fasta')
#    return ('ANZPH', 'ref/references.fasta')
#    return ('AAONP', 'ref/references.fasta')
    
DATE = '082015'
    
if __name__ == '__main__':
    
    ##
    ## STEP 1: PROCESS INPUT ARGUMENTS  (TODO)
    ##
    ## Usage: MiSeqPipeline library_name reference_sequences_file
    ##
    libraryName, reference_file = processArguments(sys.argv)
    reference_file_path = '{}/{}_{}/{}'.format(BASE_DIR, DATE, libraryName, reference_file)
    print '{} --> {}'.format(libraryName, reference_file_path)
    
    ##
    ## STEP 2: LIBRARY INFORMATION (RQC) 
    ## 
    ## retrieve the library's information (including its sub-libraries)
    ## from the RQC API
    ##
    subLibrariesInfo = RQCInvoker.loadLibraryInfo(libraryName)
    if subLibrariesInfo is None:
        print '{} is an invalid library!'.format(libraryName)
        sys.exit()

    subLibraryNames = RQCInvoker.getSubLibraryNames(libraryName)
    if subLibraryNames is None:
        print '{} is an invalid library!'.format(libraryName)
        sys.exit()
    
    ##
    ## STEP 3: PREPARE REFERENCE SEQUENCES 
    ##
    
    ## prep_ref -index ref/<reference-sequences>.fasta
#     subprocess.call(["../bin/prep_ref", '-index', reference_file_path])
    
    ## create sequence dictionary
    ## java -jar picard.jar CreateSequenceDictionary
    
    ##
    ## STEP 3: ALIGNMENT (TODO)
    ##
    ## for every sub-library, we align the references sequences
    ## with the sequences in the .fastq files
    ##
    
    
    ##
    ## STEP 4: ANALYSIS
    ##
    ## depth of coverage, variants, ...
    
    ##
    ## STEP 5: OUTPUT HTML
    ## 
    ## generate config.xml and provide it as input to summarize_analysis.py script
    subLibraryNames.sort()

    print subLibraryNames
    
    generate_config_xml.generateConfigXML(BASE_DIR, '{}_{}'.format(DATE, libraryName), subLibraryNames)
     
    pass
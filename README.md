# JGI-MiSeq

An automated pipeline for NERSC to convert raw Illumina MiSeq reads into an informative HTML representation.

## Step I: Setup Environment
```
source bin/env.reseq.sh
```

## Step II: Load Library Information

First, create a directory for the library and change into the directory.

```
mkdir <library-name>
cd <library-name>
```

One library consists of 8 or 16 sub-libraries (i.e. pools). That is, the sequence information
of all sub-libraries must be loaded. 

```
get_dw_info libs2info <lib1> ... <libN> > pre.libraries.info
```

Example: The AAONP library consists of the following sub-libraries: AAHBP, AAHBS, AAHBO, AAHBH, AAHBN, AAHBG, AAHBB, AAHBC
```
get_dw_info libs2info AAHBP AAHBS AAHBO AAHBH AAHBN AAHBG AAHBB AAHBC > pre.libraries.info
```

The ```pre.library.info``` file contains information about the location of the sequencing data produced by 
the MiSeq machine. On NERSC, this information is stored in the JAMO database. Hence, the data 
must be retrieved from the database using the following command:
```
jamo_temp_libinfo_fix pre.libraries.info > libraries.info
```

## Step III: Prepare Reference Sequences

In the library's directory, create a sub-directory in that all files of the reference sequences are stored.

```
mkdir ref
```

Then, place the reference sequences (as a FASTA format file) into the ref/ directory.

Example:
```
cp /path/to/<reference-sequences>.fasta ref/

```

Lastly, execute a script that generates relevant files (.dict, .fasta.fai) of the reference sequences.
```
prep_ref -index ref/<reference-sequences>.fasta
```


## Step IV: Sequence Alignment

In this step, the raw reads are aligned with the reference sequences. 

First, generate a directory structure for each sub-library. The ```beta_prep_setup_dirs``` receives the 
information about the sub-libraries from the ```libraries.info``` file.

```
beta_prep_setup_dirs -ref <reference-sequences>.fasta -rna -c libraries.info
```

Next, we split the raw reads into chunks of reads/read pairs using the ```beta_slice_fq``` script.
 
```
beta_slice_fq -config libraries.info
```

The ```beta_slice_fq``` script submits jobs and, hence, we need to wait until all jobs were executed properly. 
On NERSC, the ```qstat``` command enables to check the status of the submitted jobs.

Lastly, the sequenced sequences are aligend with the reference sequences and the .bam files, which contain 
the aligned reads (in binary format) are generated. 
 
```
beta_run_alignments -c libraries.info
```

Again, the ```beta_run_alignments``` script submits jobs and we need to wait until all jobs were executed 
before proceeding.

## Step V: Perform Analysis

When having the aligned reads (encoded in .bam files) for each sub-library, we need to analyze the 
sequence alignments and the depth of coverage. Based on the results, we make the variant calls, 
e.g. errors or mutations.
 
```
analysis.sh <library-name> <reference-sequences>.fasta
```
 
Example:
```
analysis.sh AAONP ref/references.fasta
```
 
## Step VI: Generate HTML Representation

In the final step, we generate an HTML representation of the sequencing results. We created a script that 
combines multiple steps to generate the HTML page and the sequencing results. 

```
generate_html.sh <library-name> <reference-sequences>.fasta
```

Example:
```
generate_html.sh AAONP ref/my_references.fasta
```

The ```postprocessing.sh``` script utilizes Java (>1.7), Python (2.7), and BROAD's Genome Analysis Toolkit (GATK) (https://www.broadinstitute.org/gatk/).
Currently, the ```postprocessing.sh``` script is implemented for NERSC and utilizes NERSC's module system (```module load```). 

The resulting HTML pages also provide links the XML files that can be nicely viewed in the Integrative Genomics Viewer (IGV), developed by the BROAD institute (https://www.broadinstitute.org/software/igv/). 
IGV must be downloaded and installed locally.


## NOTE!

Currently, the MiSeq pipeline is implemented for JGI's NERSC system. In order to execute the pipeline on a general UNIX system, various modifications must be performed (e.g. directory names, path information) and 
dependencies must be installed (e.g biopython, GATK, SAMtools). 

The ```lib/``` and ```python/``` directories contain the pipeline's dependencies, helping to deploy the pipeline on a general UNIX system more easily.

Please contact eoberortner@lbl.gov for further information and in case of questions!
   

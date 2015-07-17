# JGI-MiSeq
An automated pipeline to convert MiSeq reads into an informative HTML representation.

## Step I: setup environment
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

Example: The AAONP library consists of the AAHBP, AAHBS, AAHBO, AAHBH, AAHBN, AAHBG, AAHBB, AAHBC
```
get_dw_info libs2info AAHBP AAHBS AAHBO AAHBH AAHBN AAHBG AAHBB AAHBC > pre.libraries.info
```

The pre.library.info file contains information about the location of the sequencing data produced by 
the MiSeq machine. On NERSC, this information is stored in the JAMO database. Hence, the data 
must be retrieved from the database using the following command:
```
jamo_temp_libinfo_fix pre.libraries.info > libraries.info
```

## Step III: reference sequence(s)

In the library's directory, create a sub-directory in that all files of the reference sequences are stored.

```
mkdir ref
```

Then, place the reference sequences (as a FASTA format file) into the ref/ directory.

Example:
```
cp /path/to/<reference-sequences>.fasta ref/

```

Lastly, execute a script that generates relevant files (.dict, .fasta.fai) of the reference sequence
```
prep_ref -index ref/<reference-sequences>.fasta
```


## Step IV: Sequence Alignment

In this step, the sequenced sequences are aligned with the reference sequences.
 

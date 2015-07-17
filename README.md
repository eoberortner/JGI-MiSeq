# JGI-MiSeq
An automated pipeline to convert MiSeq reads into an informative HTML representation.

## Step I: setup environment
```
source bin/env.reseq.sh
```

## Step II: reference sequence(s)

First, create a directory in that all files of the reference sequences are located.

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



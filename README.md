# BASTA
BAsic Sequence Taxonomy Annotation

As the name implies, BASTA assigns taxonomies to sequences or groups of sequences based on the Last Common Ancestor (LCA) of best blast or diamond hits. Taxonomies are inferred from NCBI taxonomies based on a 7 level taxonomy. 

For detailed usage and installation instrauctions please visit https://github.com/timkahlke/BASTA/wiki


# Requirements

BASTA uses levelDB (https://github.com/google/leveldb) and the python wrapper Plyvel as a local database to hold NCBI mappings and taxonomies. Additionally, BASTA requires the non-standrad python packages

* gzip
* hashlib

To generate Krona plots from BASTA taxonomies Krona (https://github.com/marbl/Krona/wiki/KronaTools) has to be installed, too.

For a detailed installation guide please visit https://github.com/timkahlke/BASTA/wiki

# Quick start

## Inital Setup 

```
# set up NCBI taxonomy database
./bin/basta taxonomy

# download and set up genbank and uniprot mappings 
# NOTE: this might not be needed for you. See Wiki for details
./bin/basta download gb
./bin/basta download prot
```

## Running BASTA

```
# Infer one LCA for each query sequence of blast against uniprot
./bin/basta sequence BLAST_OUTPUT_FILE BASTA_OUTPUT_FILE prot

# Infer one LCA for the complete blast output file
./bin/basta single BLAST_OUTPUT_FILE prot

# Infer one LCA for each blast output file in a given directory
./bin/basta multiple BLAST_OUTPUT_DIRECTORY BASTA_OUTPUT_FILE prot
```

# Last Common Ancestor algorithm
BASTA supports two algorithms: all and majority

## All
If this method is used BASTA reads a given number of best hits for each query sequence and returns the LCA of all sequences (unknown taxonomic levels in database hits are ignored).

Additionally, if the *lazy* option is used, the user defined minimum number *n* of hits that is needed to estimate taxonomies will be discarded for sequences with a total hit number <n. Set values for e-value, identity, alignment length etc still apply.


## Majority
In this case BASTA determines the LCA based on the LCA of the majority of given best hits. Example: if maximum best hit number is set to 5 and 3 best hits are Bacteria and 2 best hits are Archaea, BASTA returns Bacteria as LCA.



# Additional scripts

## basta2krona.py

This creates a krona plot (html file) that can be opened in your browser from a basta annotation output file.

```
./scripts/basta2krona BASTA_OUTPUT_FILE KRONA_HTML_FILE
```


## filter_fasta.py

This script can be used to filter a given fasta file based on BASTA annotations.

```
./scripts/filter_fasta.py [options] FASTA_FILE FILTERED_OUTPUT_FILE NAME_OF_TAXON BASTA_FILE
```

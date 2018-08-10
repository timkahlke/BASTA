# BASTA
BAsic Sequence Taxonomy Annotation

As the name implies, BASTA assigns taxonomies to sequences or groups of sequences based on the Last Common Ancestor (LCA) of a number of best hits. BASTA can be customised to run on any kind of tabular output (default = blast -outfmt 6) as long as the input file provides values for e-value, percent identity and alignment length. Taxonomies are inferred from NCBI taxonomies based on a 7 level taxonomy.

For detailed usage and installation instructions please visit https://github.com/timkahlke/BASTA/wiki

### Citing BASTA
Release v1.2 can be cited as "Kahlke, T. (2018, January 9). Basta 1.2 - Basic Sequence Taxonomy Annotation (Version 1.2). Zenodo. https://doi.org/10.5281/zenodo.1137870"


# Requirements

BASTA and its dependencies can be completely installed using the [conda](https://conda.io/docs/) package manager. For installation without conda see installation instructions on the wiki (https://github.com/timkahlke/BASTA/wiki).

Installation using conda:

```
conda install -c bioconda -c bnoon -c timkahlke basta
```
The above command will install the required dependencies leveldb and wget as well as the required python libraries.

BASTA installation has been tested for MacOSX 10.11 and Ubuntu 14.01 and 16.01 using miniconda2.


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

## Conda default data directory
Per default the taxonomy data as well as mapping databasese are stored in $HOME/.basta.

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
BASTA supports taxonomic estimation based on a percentage of best hits using the -p flag.

## 100% = all
If set to 100% (default) BASTA reads a given number of best hits for each query sequence and returns the LCA of all sequences.

## 51 - 99% = majority classification
If set to a value between 51 and 99 BASTA returns the taxonomy that is shared by at least the given percentage of hits. This gives the user the potential to build a majority taxonomy instead of including all best hits in the BASTA result.


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

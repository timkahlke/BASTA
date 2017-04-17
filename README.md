# BASTA
Basic Annotation of Sequence Taxonomy

As the name implies, BASTA assigns taxonomies to sequences or groups of sequences based on the Last Common Ancestor (LCA) of best blast or diamond hits. Taxonomies are inferred from NCBI taxonomies.


# Requirements

## LevelDB
BASTA uses levelDB (https://github.com/google/leveldb) and the python wrapper Plyvel as a local database to hold NCBI mappings and taxonomies.

### LevelDB install Ubuntu

sudo apt-get update
sudo apt-get install python-leveldb
pip install Plyvel



### LevelDB install MacOSX
Easiest install is through homebrew (https://brew.sh/) and pip. 

brew install leveldb
pip install Plyvel

#### Note
Often MacOSX can't find the leveldb header files. If so try:

pip install --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" Plyvel


## Additional Python packages
* gzip
* hashlib
* argparse


# Introduction

Given a blast or diamond output file (tabular output) BASTA tries to infer taxonomies  
* for each sequence in the given blast/diamond output files 
* for the complete file based on all hits of all sequences 
* for each blast/diamond output file in a directory of files

BASTA taxonomies are based on NCBI databases, e.g., Genbank, NT, Uniprot, PDB, WGS, EST or GSS. BASTA provides methods to download the NCBI taxonomy as well as mapping files for accession numbers of each database to taxonIDs.

# Last Common Ancestor algorithm
BASTA supports two algorithms: all and majority

## All
If this method is used BASTA reads a given number of best hits for each query sequence and returns the LCA of all sequences (unknown taxonomic levels in database hits are ignored).

## Majority
In this case BASTA determines the LCA based on the LCA of the majority of given best hits. Example: if maximum best hit number is set to 5 and 3 best hits are Bacteria and 2 best hits are Archaea, BASTA returns Bacteria as LCA.

# Set up and Usage

## Download and process NCBI taxonomy
BASTA is working on the NCBI taxonomy. To download and process the NCBI files use

*./bin/basta taxonomy*

This command will download the NCBI taxonomy dump, create a 7 level taxonomy file (complete_taxa.gz) and import it into a levelDB database (complete_taxa.db)


## Download and or create mapping database
Depending on the database you used to search your query sequences against BASTA will need mapping files to infer the correct taxonID for your hit sequences. To download and process mapping files use

*./bin/basta download MAPPING_FILE_TYPE*

where MAPPING_FILE_TYPE can be gb (GenBank, RefSeq, NT ...), prot (Uniprot), pbd, wgs, est and gss.
This will download the required mapping files and create a levelDB mapping database for further use

**NOTE** The mapping files are several GB, i.e., download might take a while. Otherwise you can download the mapping files manually and use the *./bin/basta create_db* command to process them.


## BASTA Quick Intro
A complete list of command and parameters can be listed using *./bin/basta -h* and *./bin/basta/ COMMAND -h*.


### Get taxonomy for each sequence

*./bin/basta sequence BLAST_OUTPUT_FILE BASTA_OUTPUT_FILE MAPPING_TYPE*

MAPPING_TYPE can be gb (NT,GenBank,RefSeq), prot (Uniprot), pdb, wgs, est and gss.


### One taxonomy for the whole file
*./bin/basta single BLAST_OUTPUT_FILE MAPPING_TYPE*

Final taxonomy will be written to STDOUT


### One taxon for each blast/diamond file in a directory
*./bin/basta multiple DIRECTORY_OF_BLAST_OUTPUT_FILES BASTA_OUTPUT_FILE MAPPING_TYPE*











# BASTA - BAsic Sequence Taxonomy Annotation
As the name implies, BASTA assigns taxonomies to sequences or groups of 
sequences based on the Last Common Ancestor (LCA) of best blast or diamond hits
similar to MEGAN's LCA algorithm. Taxonomies are inferred from NCBI taxonomies 
of the best matching hits based on a 7 level taxonomy.

Basta has been tested on MacOSX and Ubuntu systems but should be compatible with
any Unix/linux based operating systems.


1. Install
For a more detailed install guide please visit
https://github.com/timkahlke/BASTA/wiki/1.-Installation. 


1.1 Requirements
In the current version BASTA uses levelDB to store NCBI accession_numer-to-
taxonomy_id mappings as well as the 7 level taxonomy for each NCBI taxonID.

Python packages required (non levelDB related):

* gzip
* hashlib


1.1 Installation of levelDB
LevelDB can eb isntalled using the latest github release candidate
(https://github.com/google/leveldb).


# Install under Ubuntu
LevelDB and the python package Plyvel can be installed using aptitude and pip
by typing

sudo apt-get update
sudo apt-get install python-leveldb
pip install Plyvel


# Installation under MacOSX
The easiest way to set up leveDB is using homebrew (https://brew.sh/):

brew install leveldb
pip install Plyvel

NOTE: Should your install of plyvel fail try to explicitely set the paths to 
the levelDB files:

pip install --global-option=build_ext --global-option="-I/usr/local/include" \
--global-option="-L/usr/local/lib" Plyvel


1.2 Initial set up and download of a taxonomy levelDB

To work properly BASTA needs to download the NCBI taxonomy files and create a 
levelDB database for each NCBI taxonID.

A detailed Guide and description can be found at 
https://github.com/timkahlke/BASTA/wiki/2.-Initial-Setup

To download and process the required files type
./bin/basta taxonomy 

This will download the needed taxonomy files (default ../taxonomy) and create 
a leveDB database 'complete_taxa.db'


## Download and set up of mapping levelDB

Depending on the database you search your query sequences against you will need
to also download and process specific mapping files. 

To download and process the required files use 

./bin/basta download MAPPING_FILE_TYPE

Currently supported MAPPING_FILE_TYPES are:
* gb - Genbank mappings (includes RefSeq,GenBank,NT ...)
* prot - Uniprot to taxonID mappings
* pdb - Protein structure ID to taxonID mappings
* wgs - NCBI whole genome sequence mappings
* est - NCBI EST database mappings
* gss - NCBI gss database mappings

NOTE: Some mapping files such as the genbank and uniprot mapping files are
      several GB in size and might take a while to download. Alternatively,
      in case the files are already locally available, they can be manually
      processed using BASTA's create_db command (use ./bin/basta create_db -h
      for a list of available parameters)


### BASTA taxonomy assignment

For a more detailed guide on BASTA usage please visit:
https://github.com/timkahlke/BASTA/wiki/3.-BASTA-Usage

BASTA taxonomies are based on best blast/diamond hits to NCBI databases.
It supports three different modes:

1. Per sequence assignment
This can be used to infer the LCA of each sequence with at least given number of
hits to any sequence in a given NCBI database.

2. Single output file assignment
This can be used to, e.g., infer the taxonomy of a metagenome contig based on 
the best hits of each predicted gene on the contig.

3. Per output file assignment
The same as 2 but allows to create a taxonomy for each blast/diamond output file
in a given directory. This can be useful to, e.g., try to infer basic taoxnomies
for a list of metagenome bins where each blast/diamond output file contains best
hits of each bin-contig or all genes of each bin-contig.



### Helper scripts

To visualise BASTA results with Krona kronatools 
(https://github.com/marbl/Krona/wiki/KronaTools) has to be installed.



### EXAMPLE WORKFLOW

# Assign taxonomy for each sequence based on the best 10 blast hits against 
# NCBI's NT database

1. Blast you sequences against NCBI NT but store output in tabular format (-outfmt 6)

2. Download the gb mapping files 
    ./bin/basta download gb

3. assign taxonomy to each sequence
    ./bin/basta sequence BLAST_OUTPUT_FILE TAXONOMY_OUTPUT_FILE gb -m 10 -n 10

    This will create a taxonomy output file TAXONOMY_OUTPUT_FILE based on 
    sequences with at least 10 hits to database sequences (-n 10) and will 
    only take into account the first 10 hits in the output file (-m 10).

    Additional parameters such as evalue, alignment length and percent identity
    can alos be adjusted (see ./bin/basta sequence -h for a full list of options)

4.  Visualize basta results in krona plots








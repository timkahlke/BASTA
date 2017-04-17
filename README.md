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








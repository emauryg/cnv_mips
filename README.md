
## Call CNVs from MIPS data

This is a wrapper on the cnvkit software https://github.com/etal/cnvkit. 

To install follow the instructions below from the cnvkit github

### Using Conda 

`# Configure the sources where conda will find packages
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge`

`conda install cnvkit`

### Using pip
`pip install cnvkit`

Please read their github for other R and python dependencies. 

### Get the RefFlat file containing a gene annotation 

`wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refFlat.txt.gz`

Note that this refFlat file would be in hg19 format, so if your data is in other reference genome, then it might not work.


## Running the cnv calling with mips data
`python cnv_call_mips.py -bam_dir <bam_directory> -fasta_ref <fasta_path> -bait <bed_path> -out_dir <output_directory> -sample_table <table_with_mipID_and_subjectnames> -refFlat <path_refFlat.txt>`

In the above script `-refFlat` can be left out empty, and is optional. 
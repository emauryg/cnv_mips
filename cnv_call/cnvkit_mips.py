import copy
import time
import pandas as pd
import numpy as np 
import sys
import os
import glob



bam_dir = "/n/no_backup2/bch/lee/kimjh/MIPS/javier/test/bam/"
fasta_ref = "/n/data1/bch/genetics/lee/eam63/reference/Homo_sapiens_assembly19.fasta"
bait_bed = "/n/no_backup2/bch/lee/kimjh/MIPS/javier/test/bed/Cancer_v2.picked_mips.sorted_nochr.bed"
outdir = "example/"
sample_table_path = "./indivID_mapping.txt"


## Get the bam file paths and extract the mip id
## Note this part might be project specific since it depends on naming convention
f = glob.glob(bam_dir+"*.bam")
bam_names = list(map(lambda st: str.replace(st, bam_dir,""), f))
mip_name = list(map(lambda st: str.split(st,"_")[2],bam_names))
mip_name = list(map(lambda st: str.replace(st, "JS-",""), mip_name))

## generate dictionary mapping the mips name to the bam file location for easy access
mapping_mip_path = dict(zip(mip_name,f))


## Read in the table with mipID and subject name cols: mipID subject tissue ag, last are optional
sample_table = pd.read_csv(sample_table_path, sep="\t")
sample_table = sample_table.loc(sample_table.mipID.isin(mip_name)) ## sanity check 
subjects = sample_table.subject.unique()


## Iterate through subjects and use the other subjects as a panel of normals


for i in range(len(subjects)):
    case_mip_ids = sample_table.mipID[sample_table.subject==subjects[i]].values
    control_mip_ids = sample_table.mipID[sample_table.subject!=subjects[i]].values
    cases = list(mapping_mip_path.get(str(key)) for key in case_mip_ids)
    controls = list(mapping_mip_path.get(key) for key in control_mip_ids)
    cmd = "cnvkit.py batch {} --normal {} --targets {} --fasta {} --output-reference {} --output-dir {}".format(" ".join(cases), " ".join(controls), bait_bed, fasta_ref, "my_reference.cnn",outdir)
    os.system(cmd)


# tumor= f[0]
# normal= f[1:]

# ## NOTE: command works, need to remove the 4th column of the bed file since it's not informative
# cmd = "cnvkit.py batch {} --normal {} --targets {} --fasta {} --output-reference {} --output-dir {}".format(" ".join(cases), " ".join(controls), bait_bed, fasta_ref, "my_reference.cnn",outdir)
# os.system(cmd)
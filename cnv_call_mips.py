#!/usr/bin/env python

import argparse
import copy
import time
import pandas as pd
import numpy as np 
import sys
import os
import glob

# import cnv_call 

def parse_args():
    parser = argparse.ArgumentParser(description=" running features")
    
    parser.add_argument("-bam_dir", type=str, default="./",
        help="directory with the bam files")
    parser.add_argument('-fasta_ref', type=str, help="fasta file path")
    parser.add_argument('-bait', type=str, help="capture bait bed file")
    parser.add_argument('-out_dir', type=str,default="./cnvkit_output/" help="output directory")
    parser.add_argument('-sample_table',type=str, help="list that maps bam names to subject names")

def run_mips(args):


    # Testing inputs
    # bam_dir = "/n/no_backup2/bch/lee/kimjh/MIPS/javier/test/bam/"
    # fasta_ref = "/n/data1/bch/genetics/lee/eam63/reference/Homo_sapiens_assembly19.fasta"
    # bait_bed = "/n/no_backup2/bch/lee/kimjh/MIPS/javier/test/bed/Cancer_v2.picked_mips.sorted_nochr.bed"
    # outdir = "example/"
    # sample_table_path = "./indivID_mapping.txt"

    bam_dir = args.bam_dir
    fasta_ref = args.fasta_ref
    bait_bed = args.bait
    outdir = args.out_dir
    sample_table_path = args.sample_table


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
    sample_table = sample_table[sample_table.mipID.isin(mip_name)] ## sanity check 
    subjects = sample_table.subject.unique()


    ## Iterate through subjects and use the other subjects as a panel of normals


    for i in range(len(subjects)):
    case_mip_ids = sample_table.mipID[sample_table.subject==subjects[i]].values
    control_mip_ids = sample_table.mipID[sample_table.subject!=subjects[i]].values
    cases = list(mapping_mip_path.get(str(key)) for key in case_mip_ids)
    controls = list(mapping_mip_path.get(key) for key in control_mip_ids)
    cmd = "cnvkit.py batch {} --normal {} --targets {} --fasta {} --output-reference {} --output-dir {}".format(" ".join(cases), " ".join(controls), bait_bed, fasta_ref, "my_reference.cnn",outdir)
    os.system(cmd)

    mssg = "Processing completed!!"
    return(mssg) 


if __name__ == '__main__':
    args = parse_args()

    if args.bam_dir[-1] != "/":
        args.bam_dir += "/"
    if args.out_dir[-1] != "/":
        args.out_dir += "/"

    run_mips(args)


#!/usr/bin/python

import re
import sys

##########################################################################################
# Program: uncollapse_sequences.py
# Usage: From the collapsed sequence fasta file and the name file by running the script
# collapse_sequences.py, uncollapse the unique sequence into the original uncollapsed
# sequences
# Author: Wenjie Deng
# Date: 2021-08-14
#########################################################################################


usage = 'usage: python uncollapse_sequences.py infastafile namefile'

if len(sys.argv) < 3:
    sys.exit(usage)

infile = sys.argv[1]
namefile = sys.argv[2]
namematch = re.match(r'(.*).fasta$', infile)
if namematch:
    nametag = namematch.group(1)
    outfile = nametag + "_uncollapsed.fasta"
else:
    sys.exit("Not a correct fasta file extension, must be '.fasta'")

names = []
nameseq, uniqnamenames = ({} for i in range(2))
seqname = ""
uniqcount, seqcount = 0, 0
with open(infile, "r") as fp:
    for line in fp:
        line = line.strip()
        linematch = re.match(r'^>(\S+)', line)
        if linematch:
            uniqcount += 1
            seqname = linematch.group(1)
            names.append(seqname)
            nameseq[seqname] = ""
        else:
            nameseq[seqname] += line.upper()

with open(namefile, "r") as namefp:
    for line in namefp:
        line = line.strip()
        [uniqname, allname] = line.split("\t")
        uniqnamenames[uniqname] = allname.split(",")

with open(outfile, "w") as outfp:
    for name in names:
        if uniqnamenames.get(name):
            namematch = re.search('_(\d+)$', name)
            if namematch:
                duplicates = namematch.group(1)
                arraylen = len(uniqnamenames[name])
                if (int(duplicates) == arraylen):
                    for originalname in uniqnamenames[name]:
                        seqcount += 1
                        outfp.write(">" + originalname + "\n" + nameseq[name] + "\n")
                else:
                    sys.exit("duplicates: {} does not equal to array length: {}".format(duplicates, arraylen))
        else:
            seqcount += 1
            outfp.write(">" + name + "\n" + nameseq[name] + "\n")

print("processed {} unique sequences, {} uncollapsed sequences.".format(uniqcount, seqcount))

#!/usr/bin/python

################################################################################
# Program: collapse_sequences_by_groups.py
# Purpose: collapse group of sequences to unique sequences, output unique
# sequence file and corresponding naming file
# Author: Wenjie Deng
# Date: 2021-08-17
################################################################################

import sys
import re

usage = "usage: python collapse_sequences_by_groups.py infastafile"

if len(sys.argv) < 2:
    sys.exit(usage)

infile = sys.argv[1]
outfile, seqname, namefile = '', '', ''
count = 0
idseqnames, nameseq, seqCount, idseqcount, uniqDup = ({} for i in range(5))
namematch = re.search('^(.*).fasta$', infile)
if namematch:
    name = namematch.group(1)
    outfile = name+"_collapsed_by_TP.fasta"
    namefile = name+"_collapsed_by_TP_name.txt"
else:
    print('The input file {} must have file extension of ".fasta"'.format(infile))
    sys.exit(1)

with open(infile, "r") as ifp:
    for line in ifp:
        line = line.strip()
        linematch = re.search('^>(\S+)', line)
        if linematch:
            seqname = linematch.group(1)
            namematch = re.search('^(.*?)_(\d+)_(.*?)_(.*?)_', seqname)
            if namematch:
                fields = seqname.split("_")
                id = fields[0]+"_"+fields[1]+"_"+fields[2]+"_"+fields[3]
                if idseqnames.get(id) is None:
                    idseqnames[id] = []
                idseqnames[id].append(seqname)
                count += 1
                nameseq[seqname] = ""
            else:
                print('sequence name is not formatted: {} in {}'.format(seqname, infile))
                sys.exit(1)
        else:
            line = line.upper()
            nameseq[seqname] += line

for id in idseqnames:
    for name in idseqnames[id]:
        seq = nameseq[name]
        if seqCount.get(id) is None:
            seqCount[id] = {}
        if seqCount[id].get(seq) is None:
            seqCount[id][seq] = 0
        seqCount[id][seq] += 1
        if idseqcount.get(id) is None:
            idseqcount[id] = 0
        idseqcount[id] += 1
        if uniqDup.get(id) is None:
            uniqDup[id] = {}
        if uniqDup[id].get(seq) is None:
            uniqDup[id][seq] = []
        uniqDup[id][seq].append(name)

with open(outfile, "w") as ofp:
    with open(namefile, "w") as nfp:
        print('Total {} sequences in {}'.format(count, infile))
        for id in sorted(seqCount):
            uniqcount = 0
            for seq in sorted(seqCount[id], key=seqCount[id].get, reverse=True):
                uniqcount += 1
                name = id+"_"+str(uniqcount)+"_"+str(seqCount[id][seq])
                ofp.write(">"+name+"\n"+seq+"\n")
                nfp.write(name + "\t" + ','.join(uniqDup[id][seq]) + "\n")
            print('there are {} sequences, {} unique sequences in {}'.format(idseqcount[id], uniqcount, id))

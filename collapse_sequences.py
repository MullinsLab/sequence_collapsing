#!/usr/bin/python

import sys
import re

usage = 'usage: collapse_sequences.py infastafile'

if len(sys.argv) < 2:
    sys.exit(usage)

infile = sys.argv[1]
match = re.match(r'(.*).fasta$', infile)
if match:
    nametag = match.group(1)
    outfile = nametag + "_collapsed.fasta"
else:
    print('The input file {} must have file extension of ".fasta"'.format(infile))
    sys.exit(1)

names = []
seqname, seq = "", ""
count = 0
nameseq, seqcount, seqnames = ({} for i in range(3))
with open(infile, "r") as fp:
    for line in fp:
        linematch = re.match(r'^>(\S+)', line.strip())
        if linematch:
            count += 1
            seqname = linematch.group(1)
            names.append(seqname)
            nameseq[seqname] = ""
        else:
            nameseq[seqname] += line.strip()

for name in names:
    seq = nameseq[name]
    if seqcount.get(seq) is None:
        seqcount[seq] = 0
    seqcount[seq] += 1

    if seqnames.get(seq) is None:
        seqnames[seq] = []
    seqnames[seq].append(name)

uniqcount = 0
namefile = nametag + "_collapsed_name.txt"

with open(outfile, "w") as out:
    with open(namefile, "w") as fw:
        for seq in sorted(seqcount, key=seqcount.get, reverse=True):
            uniqcount += 1
            name = nametag + "_" + str(uniqcount) + "_" + str(seqcount[seq])
            out.write(">"+name+"\n")
            out.write(seq+"\n")
            fw.write(name+"\t"+','.join(seqnames[seq])+"\n")

print("processed {} sequences in {}, {} unique sequences".format(count, infile, uniqcount))
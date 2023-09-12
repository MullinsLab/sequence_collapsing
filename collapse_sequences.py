#!/usr/bin/python

# modified from the original script to output ordered collapsed sequences if they have the same abundance
# so each time running the script will always output the same order of the collapsed sequences
# added option -g to collapse sequences by group

import sys
import re
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infasta", help="input sequence fasta file")
    parser.add_argument("-g", "--group", help="flag for collapsing by group", action="store_true")
    args = parser.parse_args()
    infile = args.infasta
    gpflag = args.group
    outfile, seqname, namefile, id = '', '', '', ''
    count = 0
    idseqnames, nameseq, seqCount, idseqcount, uniqDup = ({} for i in range(5))
    match = re.match(r'(.*).fasta$', infile)
    if match:
        id = match.group(1)
        if gpflag is True:
            outfile = id + "_collapsed_byGp.fasta"
            namefile = id + "_collapsed_byGp_name.txt"
        else:
            outfile = id + "_collapsed.fasta"
            namefile = id + "_collapsed_name.txt"
    else:
        sys.exit("Not correct fasta file extension, must be '.fasta'")

    with open(infile, "r") as ifp:
        for line in ifp:
            line = line.strip()
            linematch = re.search('^>(\S+)', line)
            if linematch:
                seqname = linematch.group(1)
                if gpflag is True:
                    namematch = re.search('^(.*?)_(\d+)_(.*?)_(.*?)_', seqname)
                    if namematch:
                        fields = seqname.split("_")
                        id = fields[0]+"_"+fields[1]+"_"+fields[2]+"_"+fields[3]
                    else:
                        sys.exit("sequence name is not formatted: "+seqname+" in "+infile+"\n")
                if id not in idseqnames:
                    idseqnames[id] = []
                idseqnames[id].append(seqname)
                count += 1
                nameseq[seqname] = ""
            else:
                line = line.upper()
                nameseq[seqname] += line

    for id in idseqnames:
        for name in idseqnames[id]:
            seq = nameseq[name]
            if id not in seqCount:
                seqCount[id] = {}
            if seq not in seqCount[id]:
                seqCount[id][seq] = 0
            seqCount[id][seq] += 1
            if id not in idseqcount:
                idseqcount[id] = 0
            idseqcount[id] += 1
            if id not in uniqDup:
                uniqDup[id] = {}
            if seq not in uniqDup[id]:
                uniqDup[id][seq] = []
            uniqDup[id][seq].append(name)

    with open(outfile, "w") as ofp:
        with open(namefile, "w") as nfp:
            print("Total {} sequences in {}".format(count, infile))
            for id in sorted(seqCount):
                uniqcount = 0
                countseqs = {}
                for seq in seqCount[id]:
                    cnt = seqCount[id][seq]
                    if cnt not in countseqs:
                        countseqs[cnt] = []
                    countseqs[cnt].append(seq)

                counts = list(countseqs.keys())
                counts.sort(reverse=True)

                for cnt in (counts):
                    for seq in sorted(countseqs[cnt]):
                        uniqcount += 1
                        name = id+"_"+str(uniqcount)+"_"+str(seqCount[id][seq])
                        ofp.write(">"+name+"\n"+seq+"\n")
                        nfp.write(name + "\t" + ','.join(uniqDup[id][seq]) + "\n")
                print("There are {} sequences, {} unique sequences in {}".format(idseqcount[id], uniqcount, id))
            print("")

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
    parser.add_argument("-i", "--fieldIndex", help="collapsing by name field indexes (1 or 1,2)", default='all')
    args = parser.parse_args()
    infile = args.infasta
    fieldidx = args.fieldIndex
    print(f"fieldIndex: {fieldidx}")
    outfile, seqname, namefile, id = '', '', '', ''
    count = 0
    idseqnames, nameseq, seqCount, idseqcount, uniqDup = ({} for i in range(5))
    match = re.match(r'(.*).fasta$', infile)
    if match:
        id = match.group(1)
        if fieldidx == "all":
            outfile = f"{id}_collapsed.fasta"
            namefile = f"{id}_collapsed_name.txt"
        else:
            fidxs = fieldidx.split(",")
            for idx in fidxs:
                if re.match(r'\d+', idx) is None:
                    sys.exit(f"the field index must be integers separated by comma (,)")
                idxs = "field" + fieldidx.replace(",", "")
            outfile = f"{id}_collapsed_by_{idxs}.fasta"
            namefile = f"{id}_collapsed_by_{idxs}_name.txt"
    else:
        sys.exit("Not correct fasta file extension, must be '.fasta'")
    print(f"outfile: {outfile}")
    print(f"namefile: {namefile}")

    with open(infile, "r") as ifp:
        for line in ifp:
            line = line.strip()
            linematch = re.search(r'^>(\S+)', line)
            if linematch:
                seqname = linematch.group(1)
                if fieldidx != 'all':
                    fidxs = [int(i) for i in fieldidx.split(",")]
                    if max(fidxs) > len(seqname.split("_")):
                        sys.exit(f"the max index is greater then the length of name fields")
                    namefields = seqname.split("_")
                    id = "_".join([namefields[i-1] for i in fidxs])
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
            print(f"Total {count} sequences in {infile}")
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
                        name = f"{id}_{uniqcount}_{seqCount[id][seq]}"
                        ofp.write(f">{name}\n{seq}\n")
                        nfp.write(f"{name}\t{','.join(uniqDup[id][seq])}\n")
                print(f"There are {idseqcount[id]} sequences, {uniqcount} unique sequences in {id}")
            print("")

import gzip

#~ f = "TheBFG/data/merged/merged_final.gz"
f = "TheBFG/data/graph/merged_final.gz"

fobj = gzip.open(f, "rb")

#~ outfile = gzip.open("TheBFG/data/merged/freq.gz", "wb")
outfile = gzip.open("TheBFG/data/graph/freq.gz", "wb")

curr_lemma = ""

curr_s = 0

for line in fobj:

	linesplit = line.strip().split("\t")
	
	#~ lemma = linesplit[0]

	lemma = linesplit[0]+"\t"+linesplit[1]

	freq = int(linesplit[2])

	if lemma == curr_lemma:

		curr_s += freq

	else:
		
		if curr_s > 1:

			outfile.write(curr_lemma + "\t" + str(curr_s) + "\n")

		curr_lemma = lemma
		
		curr_s = freq

import sys
import gzip

# Own libraries:
import config


input_file_object = gzip.open(sys.argv[1], "rb")

threshold = 1000


fouts = {
		"J" : gzip.open("bfg_adj_" + str(threshold) + ".sorted.gz", "wb"), 
		"V" : gzip.open("bfg_verb_" + str(threshold) + ".sorted.gz", "wb"), 
		"R" : gzip.open("bfg_adv_" + str(threshold) + ".sorted.gz", "wb"), 
		"N" : gzip.open("bfg_noun_" + str(threshold) + ".sorted.gz", "wb")
		}


n = float("inf")

i = 0

line = input_file_object.readline()

while line and n > threshold:

	i += 1

	linesplit = line.strip().split("\t")

	lemmasplit = linesplit[0].split("/")

	
	lemma = lemmasplit[0]

	pos = lemmasplit[-1]

	n = int(linesplit[1])
	
	
	if not pos in ["NNP", "NNPS"] and n > threshold:

		fouts[pos[0]].write(linesplit[0]+"\n")

	if not i% 100000:

		print "[DEBUG], processing line", i


	line = input_file_object.readline()


"""
The purpose of this file is to attempt a first extraction of the graph. 
This will compute a (small) sample over the first 30 parts of the DepCC Corpus.

To know:
- Proper nouns and named entities are normalized to the named entity tag or a placeholder such as NNP(S)
- Among other lemmas, only those with a frequency > 1000 are taken into consideration
- When considering an hyperedge among nodes, it may happen that some of them are low frequency lemmas. 
We impose that at least half of the lemma +1 are among the selected ones. 
This implies that binary relations are considered only when both lemmas have frequency > threshold, ternary relations when at least 2 nodes have this property and so on...
- only sentences between 6 and 20 tokens are examined
"""

import gzip
import urllib
import os
import RelationsExtractor
import DepCCToken


_MAX_FREQ_LEMMA = 1000
_LOWFREQ_THRESHOLD = 0.51

_VOCAB_FOLDER = "../data/vocabulary/"
_OUTPUT_FOLDER = "../data/graph/"
_DATA_FOLDER = "../data/"

def extractset (filename):
	fobj = gzip.open(_VOCAB_FOLDER+filename, "rb")
	
	lines = fobj.read().splitlines()
	
	return set(lines)

def testlen (s):
	return len(s)>6 and len(s)<20

_VOCAB_LISTS = {x:extractset("bfg_"+x+"_"+str(_MAX_FREQ_LEMMA)+".sorted.gz") for x in ["N", "J", "V", "R"]}


#MAIN
basic_url = "http://ltdata1.informatik.uni-hamburg.de/depcc/corpus/parsed/part-m-"

testfile = urllib.URLopener()

for i in range(0, 31):
	k = str(i).zfill(5)
	url = basic_url+k+".gz"

	f = _DATA_FOLDER+k+".gz"
	print "[DEBUG] - file", f, "..."
	
	testfile.retrieve(url, f)

	print "[DEBUG] - downloaded file", f

	rex = RelationsExtractor.RelationsExtractor(testlen)
	
	rex.set_vocabulary(_VOCAB_LISTS)
		
	rex.parse_file(f, DepCCToken.DepCCToken)

	rex.dump_relations(gzip.open(_OUTPUT_FOLDER+k+".gz", "wb"))
	
	print "[DEBUG] - removing file"
	os.remove(f)

	
#~ rex = RelationsExtractor.RelationsExtractor(testlen)

#~ rex.set_vocabulary(_VOCAB_LISTS)
	
#~ rex.parse_file("../data/00000.gz", DepCCToken.DepCCToken)

#~ rex.dump_relations(gzip.open(_OUTPUT_FOLDER+"00000.gz", "wb"))

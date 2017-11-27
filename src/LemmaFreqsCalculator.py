import urllib
import os
import gzip
import CorpusReader
import collections
import heapq


def extract_lemmas(sentence, d):
	for line in sentence:
		linesplit = line.split("\t")
		
		pos = linesplit[3]
		
		if pos[0] in ["N", "V", "J", "R"] and any(c.isalpha() for c in linesplit[2]):
			d[linesplit[2].strip()+"/"+pos]+=1

basic_url = "http://ltdata1.informatik.uni-hamburg.de/depcc/corpus/parsed/part-m-"

testfile = urllib.URLopener()

for i in range(0, 19101):
#~ for i in range(0, 11):
	k = str(i).zfill(5)
	url = basic_url+k+".gz"

	f = "../data/"+k+".gz"
	print "[DEBUG] - file", f, "..."
	
	testfile.retrieve(url, f)

	print "[DEBUG] - downloaded file", f
	
	fobj = gzip.open(f, 'rb')
	
	print "[DEBUG] - lemmas extraction started"
	
	
	R = CorpusReader.CorpusReader(fobj)
	
	dict_file = collections.defaultdict(int)
	
	for x in R:
		extract_lemmas(x, dict_file)

	sortedlemmas = sorted(dict_file.items(), key=lambda x: x[0])
	
	
	fout = gzip.open("../data/"+k+".sorted.gz", 'wb')
	
	print "[DEBUG] - writing to file"
	for x, y in sortedlemmas:
		fout.write (x+"\t"+str(y)+"\n")
	fout.close()
	print "[DEBUG] - removing file"
	os.remove(f)
	
	
def keyfunc(string):
	strsplit = string.strip().split("\t")
	return int(strsplit[1])

def decorated_file(f, key):
    for line in f: 
        yield (key(line), line)


print "[DEBUG] - merge started"
filenames = os.listdir("../data/")

files = [gzip.open("../data/"+f, "rb") for f in  filenames]
outfile = gzip.open('../data/merged.gz', "wb")

for line in heapq.merge(*[decorated_file(f, keyfunc) for f in files]):
    outfile.write(line[1])
outfile.close()    
    
print "[DEBUG] - removing useless files"
for f in filenames:
	os.remove("../data/"+f)

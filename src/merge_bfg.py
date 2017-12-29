import heapq
import os
import gzip
import contextlib
from multiprocessing import Pool

#~ path = "TheBFG/data/10001-19100/"
#~ path = "TheBFG/data/00000-10000/"
#~ path = "TheBFG/data/merged/"
path = "TheBFG/data/graph/"

#~ def keyfunc(string):
	#~ strsplit = string.strip().split("\t")
	#~ return int(strsplit[1])

#~ def decorated_file(f, key):
    #~ for line in f: 
        #~ yield (key(line), line)


def f(files):
	
	
	openfiles = [gzip.open(path+f, "rb") for f in files]
	
	outfile = gzip.open(path+"merged"+str(i+499).zfill(5)+".gz", "wb")
	
	with contextlib.nested(*openfiles):
		outfile.writelines(heapq.merge(*openfiles))

	outfile.close()
	
#~ k = 500
#~ limits = range(0, len(filenames), k)
#~ arg_list = [[filenames[limits[i]:limits[i+1]]] for i in range(len(limits)-1)]
#~ arg_list[-1].extend(filenames[i+1:])
#~ print "last i", i

#~ print arg_list
#~ print len(arg_list)
#~ raw_input()

#~ p = Pool(processes=4)
#~ p.map(f, arg_list)

print "[DEBUG] - merge started"
filenames = os.listdir(path)
files = [gzip.open(path+f, "rb") for f in  filenames]

outfile = gzip.open(path+"merged_final.gz", "wb")

with contextlib.nested(*files):
	outfile.writelines(heapq.merge(*files))

outfile.close()

#~ i = 0
#~ while i<len(filenames):
	
	#~ print "[DEBUG] - opening files from", str(i).zfill(5), "to", str(i+999).zfill(5)
	#~ files = [gzip.open(path+f, "rb") for f in  filenames[i:i+1000]]

	#~ outfile = gzip.open(path+"merged"+str(i+999).zfill(5)+".gz", "wb")
	
	#~ with contextlib.nested(*files):
		#~ outfile.writelines(heapq.merge(*files))

	#~ for line in heapq.merge(*[decorated_file(f, keyfunc) for f in files]):
		#~ outfile.write(line[1])
	#~ outfile.close()
	
	#~ i+=1000

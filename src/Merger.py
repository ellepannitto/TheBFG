import os
import glob
import sys
import gzip
from multiprocessing import Process
from multiprocessing import Event
import time

import _utils

class Merger (Process):
	
	def __init__ (self, folder, pattern, event ):
		super (Merger,self).__init__ ()
		self.folder = folder
		self.pattern = pattern
		self.event = event
		print("Merger started", pattern, "...")
	
	def merge ( self, files_to_merge ):
		
		print ("[MERGER] started merging {} files".format(len (files_to_merge)))
		folder, pattern = self.folder, self.pattern
			
		while len(files_to_merge)>1:
			
			current_files_to_merge = files_to_merge[:100]
			current_fnout = folder + "merged" + str(i) + "."+pattern+".gz"
			i+=1
			_utils._merge_sorted_files([gzip.open(f, "rt") for f in current_files_to_merge], gzip.open(current_fnout, "wt"))
			
			file_to_sum = current_fnout
			fnout_sum = folder + "sorted."+str(i) + "." + pattern+".gz"
			
			_utils._sum(gzip.open(file_to_sum, "rt"), gzip.open(fnout_sum, "wt"))
			
			
			
			files_to_merge = files_to_merge[100:]
			files_to_merge.append(fnout_sum)
	
	
	def run (self):
		
		folder, pattern = self.folder, self.pattern
		i = 0
		
		while not self.event.is_set():
			time.sleep (1)
			print ("Merger active...")
			#~ files_to_merge = glob.glob(folder+"*"+pattern+"*")
			
			#~ if len (files_to_merge) > 5:
				#~ self.merge ( files_to_merge )
			
		#~ os.rename (parameters["output_folder"]+"tmp/sorted.voc.gz", parameters["output_folder"]+"sorted."+parameters["corpus"]+".voc.gz" )
		
	
		


if __name__ == "__main__":

	e = Event()
	mrg = Merger ( "ffff", "pppp", e )
	mrg.start ()
	
	print ("[MAIN] sleeping 5 seconds befofe terminating")
	time.sleep (5)
	e.set()
	mrg.join()
	
	'''#Part 6: remove temporary output files
	print("removing files")
	
	for f in os.listdir(parameters["output_folder"]+"tmp/"):
		os.remove(parameters["output_folder"]+"tmp/"+f) '''

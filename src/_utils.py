"""
This file contains a number of different function, not directly related to the process of extracting relations.
They are mainly used to process temporary output files.
"""
#~ from __future__ import print_function


import contextlib
import heapq
import random

def _merge_sorted_files(filehandlers, outfile):
	"""
	The function takes a list of sorted files and merges them in a new sorted one.

	Parameters:
	-----------
	filehandlers: list
		list of elements to merge, each element must be a File object.
		each file must be sorted
		
	outfile: File
		file where to write the merged file

	"""

	print("[DEBUG] - merge started")

	with contextlib.ExitStack() as stack:
		files = [stack.enter_context(fn) for fn in filehandlers]
		outfile.writelines(heapq.merge(*files))

	#~ with contextlib.nested(*filehandlers):
		#~ outfile.writelines(heapq.merge(*filehandlers))

	outfile.close()


def _sum (fin, fout, min_freq = 0):
	"""
	The function sums frequencies of lines with the same prefix.

	Parameters:
	-----------
	fin: File
		file taken as input
		the file must be in the following format:
			item1	n
			item1	m
			item2	k
		where n, m, k are integers
		
	fout: File
		file where to write the output
		
	min_freq: int
		integer representing the minimum frequency an item should have in order to be passed to output


	Example result:
		from file:
			item1	n
			item1	m
			item2	k
		the function outputs:
			item1	n+m
			item2	k
			
	#TODO:
	generalize position of frequencies
	generalize function to perform (?)
	"""
	curr_inst = ""
	curr_fr = 0

	for line in fin:

		linesplit = line.strip().rsplit("\t", 1)
		
		inst = linesplit[0]
		freq = int(linesplit[1])

		if inst == curr_inst:
			curr_fr += freq

		else:
			
			if curr_fr > min_freq:
				fout.write(curr_inst + "\t" + str(curr_fr) + "\n")

			curr_inst = inst
			
			curr_fr = freq
		
	fout.write(curr_inst + "\t" + str(curr_fr) + "\n")
	
def _sort (fin, fout):
	"""
	The function takes a file containing items with frequencies specified, and sorts it according to the frequency

	Parameters:
	-----------
	fin: File
		input file
		it must be in the following format:
			item1	fr1
			item2	fr2
			item3	fr3
		
	fout: File
		output file
		
	"""	

	lines = fin.readlines()
	lines = [x.rsplit("\t", 1) for x in lines]
		
	lines.sort(key = lambda x: int(x[1]), reverse = True)
	
	for line in lines:
		fout.write("\t".join(line))
		

def _random_pick(weighted_list):

    x = random.uniform(0, 1)
    cumulative_probability = 0.0

    for item, item_probability in weighted_list:
        cumulative_probability += item_probability
        if x < cumulative_probability: break
        
    return item

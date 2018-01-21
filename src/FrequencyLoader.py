"""
The file contains functions used to load data structures containing vocabulary items.
"""

def _set_from_file (fobj, frequency_threshold, sep = "\t", item_col = 0, freq_col = 1):
	"""
	The purpose of this function is to load vocabulary items from a file (fobj). Only items with frequency greater or equal to frequency_threshold are loaded.
	The function returns a set.
	
	Parameters:
	-----------
	fobj: File
		handler to file, containing vocabulary items.
		The file should be sorted by decreasing frequency
		
	frequency_threshold: int
		integer representing the minimum frequency accepted
		
	sep: string
		string separating columns in the input file.
		default: \t
	
	item_col: int
		index of the column where the vocabulary item is to be found
		default: 0
	
	freq_col: int
		index of the column where the frequency value is to be found
		default: 1
		
	Returns:
	-----------
	set
		set containing all selected strings
	
	"""
	
	ret = set()
	
	line = fobj.readline().strip().split(sep)	
	fr = int(line[freq_col])
	
	while len(line)>0 and fr >= frequency_threshold:
		it = line[item_col]
		fr = int(line[freq_col])
				
		ret.add(it)

		line = fobj.readline().strip().split(sep)
	
	return ret

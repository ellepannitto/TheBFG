class CorpusReader:
	'''
	  Iterates a corpus reading from a file, a pipe... and returning one sentences at time
	  CorpusIterator can be used as follows:
	  
	    fin = open ("input_file.txt")
		r = CorpusReader ( fin, delimiter = "#")
		for sentence in r:
			process (sentence)
		
	'''
	def __init__(self, fin, sentence_delimiter = "#"):
		'''
		  Initializes a new object, given the object to read, the first character of lines that separate sentences.
		'''
		self.input_file = fin
		self.delimiter = sentence_delimiter
		
		
	def __iter__ ( self ):
		return self
		
	def next ( self ):
		'''
		  Returns next sentence of the corpus, if any, else it raises StopIteration
		'''
		curr_sent = []

		line = self.input_file.readline()
		
		while line and not line[0] == self.delimiter and len( line.strip() ) :
			linestrip = line.strip()
			curr_sent.append(linestrip)
			line = self.input_file.readline()
			
		if len(line)>0:
			return curr_sent
		else:
			raise StopIteration

if __name__ == "__main__":
	R = CorpusReader(open("../corporasample/DepCCsample"))
	
	for x in R:
		print x
		raw_input()

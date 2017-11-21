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

			curr_sent.append(line.strip())

			line = self.input_file.readline()
			

		if len(line) > 0:

			return curr_sent

		else:

			raise StopIteration


if __name__ == "__main__":

	stop_keys = ("x", "X", "q", "Q")

	R = CorpusReader(open("../corporasample/DepCCsample"))
	
	i = 0

	for x in R:

		# if x is not empty
		if x: 
			
			i += 1
			print "\n\nSentence " + str(i) + ":\n---\n"
			print(x)
		
			y = raw_input("\n( X or Q to exit the loop )\n")

			if y in stop_keys: break







# Own libraries:
import config

class CorpusReader:
	'''
	  Iterates a corpus reading from a file, a pipe... 
	  and returns one sentence at time.

	  CorpusReader can be used as follows:
	  
	    input_file_object = open ("input_file.txt")

		corpus_reader = CorpusReader (input_file_object, sentence_delimiter = "#")

		for sentence in corpus_reader:

			process (sentence)
		
	'''
	def __init__(self, input_file_object, sentence_delimiter = "#"):
		'''
		  Initializes a new object, given the object to read, 
		  the first character of lines that separate sentences.
		'''
		self.input_file_object = input_file_object

		self.sentence_delimiter = sentence_delimiter
		
		
	def __iter__ ( self ):

		return self
		


	def next ( self ):
		'''
		  Returns next sentence of the corpus, if any. 
		  Else raises StopIteration
		'''
		current_sentence = []

		line = self.input_file_object.readline()


		while line and not line[0] == self.sentence_delimiter and len( line.strip() ) :

			clean_line = line.strip()

			current_sentence.append(clean_line)

			line = self.input_file_object.readline()
			

		if len(line) > 0:

			return current_sentence

		else:

			raise StopIteration


if __name__ == "__main__":

	input_file_object = open(config.DepCCsample)

	corpus_reader = CorpusReader(input_file_object)

	msg = "\n( To exit the loop: type any of [" + ', '.join(config.stop_keys) + "] + press ENTER )\n"
	
	sentence_id = 0

	for sentence in corpus_reader:

		# if sentence is not empty
		if sentence: 
			
			sentence_id += 1

			print "\n\nSentence " + str(sentence_id) + ":\n---\n"

			print(sentence)

			response = raw_input(msg)

			if response in config.stop_keys: break







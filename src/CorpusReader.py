# Own libraries:
import config

class CorpusReader:

	'''
		'CorpusReader' iterates a corpus
		reading from a file, from a pipe... 
		and returns one sentence at time.

		################################

		'CorpusReader' can be used as follows:

		input_file_object = open ("input_file.txt")

		corpus_reader = CorpusReader (input_file_object, sentence_delimiter = "#")

		for sentence in corpus_reader:

			process (sentence)

		################################

		Here are the two first sentences from the DepCC:

		# sent_id = http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html#1
		# text = Sangla Valley in Himachal Pradesh in India .
		0	Sangla	Sangla	NNP	NNP		1	nn	1:nn	B-Location
		1	Valley	Valley	NNP	NNP		1	ROOT	1:ROOT	I-Location
		2	in	in	IN	IN		1	prep	_	O
		3	Himachal	Himachal	NNP	NNP		4	nn	4:nn	O
		4	Pradesh	Pradesh	NNP	NNP		2	pobj	1:prep_in	O
		5	in	in	IN	IN		1	prep	_	O
		6	India	India	NNP	NNP		5	pobj	1:prep_in	O
		7	.	.	.	.		1	punct	1:punct	O

		# sent_id = http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html#2
		# text = Samgla is the best for the Apple .
		0	Samgla	Samgla	NNP	NNP		3	nsubj	3:nsubj	B-Person
		1	is	be	VBZ	VBZ		3	cop	3:cop	O
		2	the	the	DT	DT		3	det	3:det	O
		3	best	best	JJS	JJS		3	ROOT	3:ROOT	O
		4	for	for	IN	IN		3	prep	_	O
		5	the	the	DT	DT		6	det	6:det	O
		6	Apple	Apple	NNP	NNP		4	pobj	3:prep_for	O
		7	.	.	.	.		3	punct	3:punct	O
	'''




	def __init__(self, input_file_object, sentence_delimiter = config.corpus_sentence_delimiter):
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







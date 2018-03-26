from Token import *

"""
"""


class ukWacToken(Token):
	"""
	Subclass of class Token, represents an instance of token extracted from a DepCC line.
	for more information on depcc corpus please visit: https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/depcc.html
	
	Each line of depcc is composed of 10 columns, as follows::
	0) ID = word index
	1) FORM = word form
	2) LEMMA = lemma or stem of word form
	3) UPOSTAG = universal part-of-speech tag
	4) XPOSTAG = language-specific part-of-speech tag
	5) FEATS = list of morphological features
	6) HEAD = head of the current word, which is either a value of ID or zero
	7) DEPREL = universal dependency relation to the 'HEAD'
	8) DEPS = enhanced dependency graph in the form of head-deprel pairs
	9) NER = named entity tag
	
	
	The token will have the following attributes (see class Token for documentation):
		id_ord, lemma, pos, pord, rel, enhanced_rel, enhanced_pord, ne
	"""
	
	def __init__(self, tok):
		"""
		initializes an object of class Token and sets all relevant properties
		
		Parameters:
		-----------
		tok: string
			string of depcc corpus, representing a token
			the string must be made up of 10 columns divided by tab (\t)
			
		
		EXAMPLE
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
		There are 8 tokens from 0 to 7, one token per line.
		The second token has the following features: 
		ID = 1, LEMMA = Valley, UPOSTAG = NNP, HEAD = 1, DEPREL = ROOT, DEPS = 1:ROOT, NER = I-Location
		The third token has the following features:
		ID = 2, LEMMA = in, UPOSTAG = IN, HEAD = 1, DEPREL = prep, DEPS = _, NER = O
		The fifth token has the following features:
		ID = 4, LEMMA = Pradesh, UPOSTAG = NNP, HEAD = 2, DEPREL = pobj, DEPS = 1:prep_in, NER = O
		"""	

		super(ukWacToken, self).__init__()
		
		split_tok = tok.split("\t")
		
		# ID : word index		
		self.id_ord = int(split_tok[3])

		# LEMMA : lemma or stem of word form
		self.lemma = split_tok[1].strip()
		
		# UPOSTAG : universal part-of-speech tag
		self.pos = split_tok[2].strip()
		
		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = int(split_tok[4])
		
		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = split_tok[5].strip()
		
		#~ # NER : named entity tag
		#~ self.ne = split_tok[9].strip()


		#~ # DEPS : enhanced dependency graph in the form of head-deprel pairs
		#~ enhanced = split_tok[8].split(":")

			
		#~ if not enhanced[0] == "_":
			#~ enhanced_pord = int(enhanced[0])
			#~ enhanced_rel = enhanced[1].strip()
			
			#~ # We copy the information, only if there is something new.
			#~ if enhanced_pord == self.pord:				
				#~ self.rel = enhanced_rel
				
			#~ elif not enhanced_rel == self.rel:
				#~ self.enhanced_pord = enhanced_pord
				#~ self.enhanced_rel = enhanced_rel
	
	def __repr__ (self):
		return self.lemma+"\t"+self.pos+"\t"+str(self.pord)+"\t"+self.rel

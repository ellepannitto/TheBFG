from Token import *

"""
"""


class WikipediaToken(Token):
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

		1 Swedenborg swedenborg NN PERSON nsubj=2,nsubj=9
		2 studied study VBD O ROOT=0
		3 physics physics NNS O dobj=2
		4 , , , O punct=3
		5 mechanics mechanic NNS O dobj=2,conj:and=3
		6 and and CC O cc=3
		7 philosophy philosophy NN O dobj=2,conj:and=3
		8 and and CC O cc=2
		9 read read VB O conj:and=2
		10 and and CC O cc=9
		11 wrote write VBD O conj:and=2,conj:and=9
		12 poetry poetry NN O dobj=9
		13 . . . O punct=2

		"""
		super(WikipediaToken, self).__init__()
		
		split_tok = tok.split()
		
		# ID : word index		
		self.id_ord = int(split_tok[0])

		# LEMMA : lemma or stem of word form
		self.lemma = split_tok[2].strip()
		
		# UPOSTAG : universal part-of-speech tag
		self.pos = split_tok[3].strip()
		
		rels = split_tok[5].strip().split(",")
		
		first_rel = rels[0].split("=")
		
		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = int(first_rel[1])
		
		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = "_".join(first_rel[0].split(":"))
		
		# NER : named entity tag
		self.ne = "B-"+split_tok[4].strip()
		
		if len(rels) > 2:
			print("più di 2 rels")
			print (rels)
		elif len(rels)>1:
			enhanced = rels[1].split("=")
			enhanced_pord = int(enhanced[1])
			enhanced_rel = "_".join(enhanced[0].split(":"))
			
			self.enhanced_pord = enhanced_pord
			self.enhanced_rel = enhanced_rel

	
	def __repr__ (self):
		return self.lemma+"\t"+self.pos+"\t"+str(self.pord)+"\t"+self.rel

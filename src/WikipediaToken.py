import math

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
		
		rels = list(set(split_tok[5].strip().split(",")))
		
		rels_splitted = [x.split("=") for x in rels]
		
		
		rels = []
		for x in rels_splitted:
			
			try:
				x_rel = x[0]
				x_int = int(x[1])
				
				if x_rel == "compound:prt":
					x_rel = "prt"
				else:
					
					#~ pass
					x_rel = x_rel.split(":")[0]
					#~ print ("sono qui")
					
				rels.append((x_rel, x_int))
					
			except:
				#~ print(e)
				print("error during relation parsing {}".format(x))
				#~ input()
		
		rels = sorted(rels, key = lambda x: math.fabs(x[1] - self.id_ord))
		

		if len(rels)>0:
			first_rel = rels[0]
		else:
			first_rel = ("dep", self.id_ord)

		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = first_rel[1]
		
		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = "_".join(first_rel[0].split(":"))	
		
			
		# NER : named entity tag
		self.ne = "B-"+split_tok[4].strip()
		
		if len(rels)>1:
			second_rel = rels[1]

			enhanced_pord = second_rel[1]
			enhanced_rel = "_".join(second_rel[0].split(":"))
				
			self.enhanced_pord = enhanced_pord
			self.enhanced_rel = enhanced_rel
		
		if len(rels) > 2:
			self.other_rels = rels[2:]
			#~ print(self.id_ord)
			#~ print("più di 2 rels")
			#~ print (rels)

	
	def __repr__ (self):
		return self.lemma+"\t"+self.pos+"\t"+str(self.pord)+"\t"+self.rel

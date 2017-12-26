# Own libraries:

from Token import *
import config

"""

Each token (or 'word') is associated to 10 attributes from 0 to 9:

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

We use ID.
We use LEMMA and ignore FORM.
We use UPOSTAG and ignore XPOSTAG.
We ignore FEATS.

We use HEAD, DEPREL, DEPS and NER.


EXAMPLE


Let's take as an example the first sentence of the DepCC corpus:

Sangla Valley in Himachal Pradesh in India .


It is actually a nominal phrase.



In the corpus it looks like this:

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



We see that 'Valley' is the ROOT of the phrase.


Looking at the DEPREL feature, the dependency structure is:

prep(Valley-1, in-2)
pobj(in-2, Pradesh-4)


We can add an enhanced relationship:

1:prep_in(in-2, Pradesh-4)


In this enhanced relationship,

enhanced_pord = 1
enhanced_rel = prep_in


Which corresponds to:

prep_in(Valley-1, Pradesh-4)


"""


# retrieving the positions of the columns
id_ord_p = config.DepCC_line_map.index("ID")
lemma_p = config.DepCC_line_map.index("LEMMA")
POS_p = config.DepCC_line_map.index("UPOSTAG")
pord_p = config.DepCC_line_map.index("HEAD")
rel_p = config.DepCC_line_map.index("DEPREL")
enhanced_p = config.DepCC_line_map.index("DEPS")
ne_p = config.DepCC_line_map.index("NER")

class DepCCToken(Token):
	"""
	  Subclass of class Token, represents an instance of token extracted from a DepCC line. 
	"""
	
	def __init__(self, tok):
		

		super(DepCCToken, self).__init__()
		
		

		split_tok = tok.split("\t")
		


		# ID : word index
		self.id_ord = int(split_tok[id_ord_p])

		# LEMMA : lemma or stem of word form
		self.lemma = split_tok[lemma_p].strip()

		# UPOSTAG : universal part-of-speech tag
		self.POS = split_tok[POS_p].strip()

		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = int(split_tok[pord_p])

		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = split_tok[rel_p].strip()
		
		# NER : named entity tag
		self.ne = split_tok[ne_p].strip()






		# processing the enhanced relationship
		####################################################

		# DEPS : enhanced dependency graph in the form of head-deprel pairs
		enhanced = split_tok[enhanced_p].split(":")

			
		if not enhanced[0] == "_":

			# For instance: 

			# if enhanced = 1:prep_in
			# enhanced_pord = 1
			# enhanced_rel = prep_in

			enhanced_pord = int(enhanced[0])

			enhanced_rel = enhanced[1].strip()
			
			# We copy the information, only if there is something new.

			if not (enhanced_pord == self.pord and enhanced_rel == self.rel):

				self.enhanced_pord = enhanced_pord

				self.enhanced_rel = enhanced_rel
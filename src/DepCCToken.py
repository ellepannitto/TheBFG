# Own libraries:

from Token import *
import config


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
		
		self.id_ord = int(split_tok[id_ord_p])

		self.lemma = split_tok[lemma_p].strip()

		self.POS = split_tok[POS_p].strip()

		self.pord = int(split_tok[pord_p])

		self.rel = split_tok[rel_p].strip()
		
		self.ne = split_tok[ne_p].strip()
		
		
		enhanced = split_tok[enhanced_p].split(":")

			
		if not enhanced[0] =="_":

			enhanced_pord = int(enhanced[0])

			enhanced_rel = enhanced[1].strip()
			

			if not (enhanced_pord == self.pord and enhanced_rel == self.rel):

				self.enhanced_pord = enhanced_pord

				self.enhanced_rel = enhanced_rel		
		
		

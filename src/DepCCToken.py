from Token import *

class DepCCToken(Token):
	"""
	  Subclass of class Token, represents an instance of token extracted from a DepCC line. 
	"""
	
	def __init__(self, tok):
		
		super(DepCCToken, self).__init__()
		
		
		split_tok = tok.split("\t")
		
		self.id_ord = int(split_tok[0])
		self.lemma = split_tok[2].strip()
		self.pos = split_tok[3].strip()
		self.pord = int(split_tok[6])
		self.rel = split_tok[7].strip()
		
		self.ne = split_tok[9].strip()
		
		
		enhanced = split_tok[8].split(":")
			
		if not enhanced[0] =="_":
			enhanced_pord = int(enhanced[0])
			enhanced_rel = enhanced[1].strip()
			
			if not (enhanced_pord == self.pord and enhanced_rel == self.rel):
				self.enhanced_pord = enhanced_pord
				self.enhanced_rel = enhanced_rel		
		
		

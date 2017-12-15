class Token(object):
	"""
	  Represents a Token, formed by relevant attributes. 
	"""
	def __init__(self):
		self.id_ord = -1
		self.lemma = ""
		self.pos = ""
		self.pord = -1
		self.rel = ""
		self.enhanced_pord = -1
		self.enhanced_rel = ""
		self.ne = "O"
		
	def normalize(self):
		"""
		This function is meant to do a series of operations, only some of them being already implemented.
		
		- Transforms passive relations into active relations (nsubjpass -> dobj, csubjpass -> ccomp)
		
		Patrick: could you please an example for each case?

		- Adds PoS or NE Class to lemma

		Patrick: could you please an example for each case?



		
		Other things that could be implemented here:
		- filter lemmas on frequency
		- add placeholders...
		"""
		
		splitne = self.ne.split("-")
		if len(self.ne)>1:
			self.ne = splitne[1]

		# Patrick: could you please an example ?
		# If it's B-Location or I-Location, we just keep Location :) If there's no "-", it's just "O" so we keep "O", but we're not using it anyway

		

		#~ if not self.ne == "O":
			#~ self.lemma = self.lemma+"/"+self.ne
		#~ else:
			#~ self.lemma = self.lemma+"/"+self.pos

		# In order to remove proper nouns from the graph, but keep information about them (such as "ProperNoun subject of running" for example), I'm updating things this way:
		#- proper nouns are in general replaced with a special string such as _NNP_
		#- if the lemma is a recognized named entity, we replace it with _Location_ for example, so that we know it's a location, which is more specific than _NNP_
		
		if self.pos in ["NNP", "NNPS"] and self.ne == "O":
			self.lemma = "_"+self.pos+"_"
		elif not self.ne == "O":
			self.lemma = "_"+self.ne+"_"
			
		self.lemma = self.lemma+"/"+self.pos


		if self.rel == "nsubjpass":
			self.rel = "dobj"

		if self.rel == "csubjpass":
			self.rel = "ccomp"
		
		if self.enhanced_rel == "nsubjpass":
			self.enhanced_rel = "dobj"
		if self.enhanced_rel == "csubjpass":
			self.enhanced_rel = "ccomp"


	def add_part (self, prt):
		"""
		Expands lemma by adding prt

		Patrick: could you please give an example?
		"""
		
		self.lemma = self.lemma+"_"+prt
		
		
		

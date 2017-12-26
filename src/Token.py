class Token(object):
	"""
	  Represents a Token, formed by its relevant attributes. 


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


	"""

	# initialization
	#####################

	def __init__(self):

		# ID : word index
		self.id_ord = -1 

		# LEMMA : lemma or stem of word form
		self.lemma = ""

		# UPOSTAG : universal part-of-speech tag
		self.POS = ""

		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = -1

		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = ""


		# DEPS : enhanced dependency graph in the form of head-deprel pairs
		# where 
		# enhanced_pord is the HEAD
		# enhanced_rel is DEPREL
		self.enhanced_pord = -1
		self.enhanced_rel = ""


		# NER : named entity tag
		self.ne = "O"
		


	# normalization of the Token
	###############################

	def normalize(self, vocab_dict):
		"""
		This function is meant to do a series of operations.

		Only some of them are currently implemented.


		
		- Transforms passive relations into active relations (nsubjpass -> dobj, csubjpass -> ccomp)
		
		Patrick: could you please an example for each case?




		- Adds PoS or NE Class to lemma

		Patrick: could you please an example for each case?



		
		Other things that could be implemented here:
		- filter lemmas on frequency
		- add placeholders...
		"""
		
		splitne = self.ne.split("-")

		if len(self.ne) >1 :
			
			self.ne = splitne[1]


		# Patrick: could you please an example ?




		# If it's B-Location or I-Location, 
		# we just keep Location :) 
		# If there's no "-", it's just "O" so we keep "O", but we're not using it anyway

		

		#~ if not self.ne == "O":
			#~ self.lemma = self.lemma+"/"+self.ne

		#~ else:
			#~ self.lemma = self.lemma+"/"+self.POS



		# In order to remove proper nouns from the graph,
		#  but keep information about them 
		# (such as "ProperNoun subject of running" for example), 
		# I'm updating things this way:
		# - proper nouns are in general replaced with a special string such as _NNP_
		# - if the lemma is a recognized named entity, 
		# we replace it with _Location_ for example, so that we know it's a location, which is more specific than _NNP_

		
		if self.POS in ["NNP", "NNPS"] and self.ne == "O":

			self.lemma = "_" + self.POS + "_"



		elif not self.ne == "O":

			self.lemma = "_" + self.ne + "_"



		elif self.POS[0] in vocab_dict:

			#~ print self.lemma, self.POS



			if not self.lemma + "/" + self.POS in vocab_dict[self.POS[0]]:
				#~ print self.lemma+"/"+self.POS
				#~ print vocab_dict[self.POS[0]]
				#~ raw_input()

				self.lemma = "*"
			

		# Associate the lemma to its POS...
		self.lemma = self.lemma + "/" + self.POS



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
		
		self.lemma = self.lemma + "_" + prt
		
		
		

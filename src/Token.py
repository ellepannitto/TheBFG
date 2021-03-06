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



		Other things that could be implemented here:

		- filter lemmas on frequency

		- add placeholders...


		Processing of NER : named entity tag
		#################################### 

		Possible values:

		B-Location
		I-Location
		...

		We keep just the first value it the string is at least 2 characters long

		So:

		B-Location -> B
		I-Location -> I
		...

		Note: this might be a useless feature.

		"""
		
		splitne = self.ne.split("-")

		if len(self.ne) > 1 :
			
			self.ne = splitne[0]  # This sould be 0 right?
			#self.ne = splitne[1]



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
			





		# Associate the lemma to its POS.
		# -------------------------------------

		self.lemma = self.lemma + "/" + self.POS









		"""
		Transforms passive relations into active relations (I)
		-----------------------------------------------------

		nsubjpass -> dobj
		-----------------
		
		Passive nominal subject (nsubjpass) -> direct object (dobj)
		Dole was defeated by Clinton -> Clinton defeated Dole
		nsubjpass(defeated, Dole) -> dobj(defeated, Dole)


		"""

		if self.rel == "nsubjpass":

			self.rel = "dobj"

		
		if self.enhanced_rel == "nsubjpass":

			self.enhanced_rel = "dobj"








		"""		

		Transforms passive relations into active relations (II)
		-------------------------------------------------------

		csubjpass -> ccomp
		------------------
		
		Clausal passive subject (csubjpass) -> Clausal complement (ccomp)
		That she lied was suspected by everyone -> Everyone suspected that she lied.
		csubjpass(suspected, lied) -> ccomp(suspected, lied)
		
		"""

		if self.rel == "csubjpass":

			self.rel = "ccomp"


		if self.enhanced_rel == "csubjpass":

			self.enhanced_rel = "ccomp"









	def add_part (self, prt):
		"""
		Expands lemma by adding prt

		prt: phrasal verb particle

		Example : 

		They shut down the station
		prt(shut, down)

		if lemma = 'shut', and prt = 'down', 
		lemma becomes 'shut down'
		
		"""
		
		self.lemma = self.lemma + "_" + prt
		
		
		

class Token(object):
	"""
	  Represents a Token, formed by its relevant attributes. 
	  These are:
	  
	  - id_ord: id of token, place of token in sentence, default -1
	  - lemma: lemma or stem of word form, default ""
	  - pos: coarse grained part of speech tag of token, default ""
	  - pord: syntactic head of token, default -1
	  - rel: dependency relation of token, default ""
	  - enhanced_rel: enhanced dependency relation of token, default ""
	  - enhanced_pord: head of token, concerning enhanced relation, default -1
	  - ne: named entity tag in BIO notation, default "O"
	"""

	# initialization
	def __init__(self):
		"""
		initialzies the token with default values
		"""

		# ID : word index
		self.id_ord = -1 
	
		self.part_added = False
		
		# LEMMA : lemma or stem of word form
		self.lemma = ""

		# UPOSTAG : universal part-of-speech tag
		self.pos = ""

		# HEAD : head of the current word, which is either a value of ID or zero
		self.pord = -1

		# DEPREL : universal dependency relation to the 'HEAD'
		self.rel = ""


		# DEPS : enhanced dependency graph in the form of head-deprel pairs where 
		# enhanced_pord is the HEAD
		# enhanced_rel is DEPREL
		self.enhanced_pord = -1
		self.enhanced_rel = ""


		# NER : named entity tag
		self.ne = "O"
		


	# normalization of the Token
	def normalize(self, vocab_dict):
		"""
		This function is meant to do a series of operations of normalization on properties of the token.
		
		Parameters:
		-----------
		vocab_dict: dict
			dictionary of the format {cpos: set}
			where cpos is a standard coarse part of speech tag (such as N for noun, V for verb...) and set is a set of accepted lemmas


		Operations performed:
		- replacement of named entities:
			when the token is tagged as part of a named entity, its lemma it's replaced by the NE tag.
			for example, if the token is tagged as B-Organization, its lemma becomes _Organization_
			
		- replacement of proper nouns:
			proper noun lemmas are discarded and replaced with a placeholder (_NNP_)
			
		- replacement of non-accepted lemmas:
			lemmas which are not in the vocabulary dictionary are replaced by a wildcard (*)
		
		- normalization of passive relations:
			passive dependency relations are turned into the active form, following this schema:
				nsubjpass -> dobj
				csubjpass -> ccomp
			
		"""
			
		splitne = self.ne.split("-")

		if len(self.ne) > 1 :
			self.ne = splitne[1]
		
		search_lemma = self.lemma.split("_",1)[0] if self.part_added else self.lemma
	
		#if the token is a proper noun and not tagged as named entity
		if self.pos in ["NNP", "NNPS"] and self.ne == "O":
			self.lemma = "_" + self.pos + "_"
		#if the token is tagged as a named entity
		elif not self.ne == "O":
			self.lemma = "_" + self.ne + "_"
		#if the lemma is not among the accepted ones
		elif self.pos[0] in vocab_dict:
			if not search_lemma + "/" + self.pos[0] in vocab_dict[self.pos[0]]:
				self.lemma = "*"
			

		# Associate the lemma to its coarse-grained PoS.
		self.lemma = self.lemma + "/" + self.pos[0]



		
		#passive relations are turned into active forms
		if self.rel == "nsubjpass":
			self.rel = "dobj"
		if self.enhanced_rel == "nsubjpass":
			self.enhanced_rel = "dobj"

		if self.rel == "csubjpass":
			self.rel = "ccomp"
		if self.enhanced_rel == "csubjpass":
			self.enhanced_rel = "ccomp"
		
		#~ print (self.enhanced_rel)

		splitrel = self.rel.split("_")
		#~ if self.rel[:5]=="prep_":
		if len(splitrel)>1:
			#~ print("prep_ :"+self.rel)
			#~ splitrel = self.rel.split("_")
			if not all(c.isalpha() for c in splitrel[1]):
				self.rel = splitrel[0]
			#~ print(self.rel)
			#~ input()
			
		splitrel = self.enhanced_rel.split("_")
		#~ if self.enhanced_rel[:5]=="prep_":
		if len(splitrel)>1:
			#~ print("prep_ :"+self.enhanced_rel)
			#~ splitrel = self.enhanced_rel.split("_")
			if not all(c.isalpha() for c in splitrel[1]):
				self.enhanced_rel = splitrel[0]
			#~ print(self.enhanced_rel)
			#~ input()	


	def add_part (self, prt):
		"""
		Expands lemma by adding an extra part to it. The lemma and the new part are joined together with an underscore -> [lemma]_[prt]
		It is mainly used to add particles of phrasal verbs.
		
		Parameters:
		-----------
		prt: string
			string to add to the lemma


		Example : 

		They shut down the station
		phrasal_verb(shut, down)

		if lemma = 'shut', and prt = 'down', 
		lemma becomes 'shut_down'
		
		"""
		
		self.lemma = self.lemma + "_" + prt
		self.part_added = True

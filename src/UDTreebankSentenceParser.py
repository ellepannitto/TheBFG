import math

import Sentence 

class UDTreebankSentenceParser:
	"""
	The purpose of the class is to parse a raw portion of DepCC corpus and extract necessary information in order to build ad object of class Sentence.

	for more information on depcc corpus please visit: https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/depcc.html
	"""
	
	def __init__ (self, parameters):
		"""
		initializes an object of class DepCCSentenceParser
		
		Parameters:
		-----------
		parameters: dict
			dictionary of configuration parameters
			the dictionary must contain the following indexes:
				- token_class -> class that will be used to parse each token
				- vocab_list -> list of interesting vocabulary items to keep (others will be replaced by a wildcard)
				- head_cpos -> list of coarse-grained PoS tags which are suitable to be heads of subtrees
				- max_distance -> max distance allowed for relations, between a token and its head 
				
		#TODO: check for parameters
		"""
		self.TokenClass = parameters["token_class"]
		self.vocabulary = parameters["vocab_list"]
		self.head_CPoS = parameters["head_cpos"]
		self.max_distance = parameters["max_distance"]
	
	def parse_sent (self, raw_sentence):
		"""
		Parses a sentence from a list of raw strings extracted from DepCC corpus.
		
		Parameters:
		-----------
		raw_sentence: list
			list of strings, each representing a line of a portion taken from DepCC corpus
			
			
		Returns:
		--------
		Sentence
			object of class Sentence, see documentation for more details
			
		#TODO:
		add ignored relations
		"""

		map_ne = {}
		sentence = {}
		for token in raw_sentence:
			token = self.TokenClass(token)
			sentence[token.id_ord] = token


			#this line is meant to merge particles with verbs, so phrasal verbs are reconstructed.
			#TODO: fix other cases of particles (id < head)
			if token.rel == "prt":
				if token.pord in sentence:
					sentence[token.pord].add_part(token.lemma)
				else:
					print "DEBUG - head of particle not in sentence"
					print raw_sentence
					print token.pord



		#normalize each token (see normalizing function in class token)
		for id_ord in sentence:
			token = sentence[id_ord]
			token.normalize(self.vocabulary)
		
		#this part computes a set of dependencies for each node (so that we know all the children of a certain node), 
		#and selects the root of the sentence (element labeled as ROOT, if suitable to be a head)
		deps  = {}
		root = None
		for id_ord in sentence:
			token = sentence[id_ord]
			if not token.pord in deps:
				deps[token.pord] = []
				
			if not token.pord == id_ord and math.fabs(token.pord - id_ord) <= self.max_distance:
				deps[token.pord].append((id_ord, token.rel))
			
			if token.enhanced_pord>0:
				if not token.enhanced_pord in deps:
					deps[token.enhanced_pord] = []	
				deps[token.enhanced_pord].append((id_ord, token.enhanced_rel))	
			
			if token.rel == "root" and token.pos[0] in self.head_CPoS:
				root = id_ord
		
		
		return Sentence.Sentence ( sentence, root, deps )

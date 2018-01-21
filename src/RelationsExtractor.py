import os
import itertools
from collections import *
import gzip
from tests import *

import CorpusReader as Reader
import DepCCToken

class RelationsExtractor:
	"""
	the extractor keeps relations in a variable called items, of type dict:
		items = {string(nodes): {string(deprels): frequency } }
	"""
	
	def __init__(self, parameters):
		"""
		initializes an object of class RelationsExtractor
		
		Parameters:
		-----------
		parameters: dict
			dictionary of configuration parameters
			the dictionary must contain the following indexes:
				- lexical_cpos -> list of coarse-grained PoS tags which are considered as nodes
				- head_cpos -> list of coarse-grained PoS tags which are suitable to be heads of subtrees
				- ignored_deprels -> list of dependency relations that are not considered during the process (#TODO: move this to sentence parser)
				- max_wildcards -> maximum number of wildcards allowed in an extracted structure
								
		#TODO: check for parameters 
		"""
		
		
		self.lexical_cpos = parameters["lexical_cpos"]
		self.head_cpos = parameters["head_cpos"]
		self.ignored_deprels = parameters["ignored_deprels"]
		self.max_wildcards = parameters["max_wildcards"]
		
		
		self.items = defaultdict(lambda: defaultdict(int))
		
		
		
		#TODO: remove this things after some changes to the code
		# - relations I'm not considering at all: "abbrev", "appos", "attr", "aux", "auxpass", "cc", "complm", "cop", "dep", "det", "mark", "nn", "null", "number", "parataxis", "predet", "pred", "prep", "punct", "rel"
		# - relations I'm not considering since they're considered elsewhere: "nsubjpass", "csubjpass", "pobj", "pcomp", "ROOT"
		# - relations I would like to consider somehow: "expl", "num"+"measure", "neg", "poss", "possessive", "preconj", "prt", "quantmod"(?), "tmod"
		
		#relations we're taking into consideration. Ignore the "lambda: True" thing, it is just in case we need different functions depending on the kind of relation
		#~ self.switch_relations = {
			#~ "acomp" : lambda: True, 
			#~ "advcl" : lambda: True, 
			#~ "advmod":lambda: True, 
			#~ "amod": lambda: True, 
			#~ "ccomp": lambda: True, 
			#~ "conj": lambda: True,
			#~ "csubj": lambda: True,
			#~ "dobj": lambda: True,
			#~ "infmod": lambda: True,
			#~ "iobj": lambda: True,
			#~ "nsubj": lambda: True,
			#~ "partmod": lambda: True,
			#~ "purpcl": lambda: True,
			#~ "rcmod": lambda: True,
			#~ "xcomp": lambda: True
		#~ }
				
	def process (self, sentence):
		"""
		This is the core function of the extraction process. Given a sentence in the shape of an object of class Sentence (see documentation), it extract all relevant structures. The class counts occurrences of extracted structures.
		
		Parameters:
		-----------
		sentence: Sentence
			object of class Sentence, containing the sentence to parse
			
		
		How relations are extracted (example, see also [] for documentation:
		--------------------------------------------------------------------
		
		- Some lexical items of the sentece are considered heads, each of them defines a group
		- For each head h:
			group(h) = dependants of h
		- groups = group(h) for each h head
		
		- For each group g
			subsets(g) = all possible subsets involving the head and its dependants
			Each subset corresponds to a relation WITHIN a group. 
			The relation is named on the basis of the syntactical dependence linking the elements in the subset.

		- For all groups g1, g2
			generic_associations(g1, g2) = (e1, e2) such that they don't belong to the same group
			These are relations BETWEEN groups. We only consider the pairs formed by two items belonging to different groups. These relations are not named since there usually is not syntactic dependence between their elements.
		
		Example sentence:
		-----------------

		*The tall student reads the black book while the teacher speaks about history*

		From the example sentence, we can extract 4 heads, and so 4 groups are formed:

			Group1: head = read, dependants = {student, book, speak}
			Group2: head = student, dependants = {tall}
			Group3: head = book, dependants = {black}
			Group4: head = speak, dependants = {teacher, history}


		
		"""		
		root = sentence.root
		deps = sentence.deps
		sentence = sentence.token_list

		
		dati_supp = []
		groups = []
		
		#The idea is that the queue contains the root at the begininng, and navigates the dependencies starting from there.
		if root:
			Q = [root]

			while Q:
				x = Q.pop()
				
				curr_el = sentence[x]
				group = [(curr_el.lemma, "ROOT")]
				dati_supp.append([curr_el.lemma])
				
				curr_deps = []
				if x in deps:
					curr_deps = deps[x]			

				for i, r in curr_deps:
					target = sentence[i]
					if target.pos[0] in self.lexical_cpos and target.rel not in self.ignored_deprels:
						group.append((target.lemma, r))
						dati_supp[-1].append(target.lemma)
							
					if target.pos[0] in self.head_cpos:
						Q.append(i)
				
				groups.append(group)
		

		dati = {}
		for i, d in enumerate(dati_supp):
			for el in d:
				if not el in dati:
					dati[el] = []
				dati[el].append(i)
		
		for i, g in enumerate(groups):			
			for n in range(2, len(g)+1):
				
				subsets = set(itertools.combinations(g, n))
				
				for s in subsets:
					s = sorted(s, key = lambda x:x[0])
					
					elements = [e[0] for e in s]
					elements_0 = [e[0] for e in elements]
					labels = [e[1] for e in s]
				
				

				if elements_0.count("*")<= self.max_wildcards:
					self.items[" ".join(elements)]["|".join(labels)]+=1
			
			
			#GENERIC ASSOCIATIONS
			for j, h in enumerate(groups):
				
				if j>i:
					
					for a in g:
						for b in h:
							
							#~ #a nel gruppo i, b nel gruppo j
							if not i in dati[b[0]]:
								self.items[" ".join([min(a[0], b[0]), max(a[0], b[0])])]["genassoc"]+=1

	def dump_relations(self, fobj):
		"""
		The functions writes processed items in a file
		
		Parameters:
		-----------
		fout: File
			output file
			
		the output is formatted as follows
		node_1 node_2 ... node_k [tab] deprel_1|deprel_2|...|deprel_k [tab] frequency
		nodes are sorted alphabetically within the relation, deprels are sorted according to nodes
		
		"""
		
		rels = self.items
		
		for elements, labels in sorted(rels.items()):
			node = elements
			
			for lab_group in sorted(labels):
				label = lab_group
				
				fobj.write(node + "\t" + label + "\t" + str(labels[lab_group]) + "\n")			

if __name__ == "__main__":
	pass
	#TODO: add test

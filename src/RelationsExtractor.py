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
		
		self.vocabulary = defaultdict(int)
		self.structures = defaultdict(int)
		
		
		
				
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
		#~ print ("{}: started processing {}".format(os.getpid(),sentence))

		root = sentence.root
		deps = sentence.deps
		sentence = sentence.token_list


		groups = []
		

		visited = defaultdict(bool)
		added_to_voc = defaultdict(bool)
		
		#The idea is that the queue contains the root at the begininng, and navigates the dependencies starting from there.
		if root:
			Q = [root]
			
			self.vocabulary[sentence[root].lemma]+=1
			visited[root]=True
			added_to_voc[root]=True
			
			#~ print ("{}: before while".format(os.getpid()))

			while Q:
					
				x = Q.pop()
				
				curr_el = sentence[x]
				
				group = [(curr_el.lemma, "ROOT")]
				
				
				curr_deps = []
				if x in deps:
					curr_deps = deps[x]			

				for i, r in curr_deps:
					target = sentence[i]
					
					if not added_to_voc[i]:
						added_to_voc[i] = True
						self.vocabulary[target.lemma]+=1
					
					if target.pos[0] in self.lexical_cpos and not r in self.ignored_deprels:
						group.append((target.lemma, r))
							
					if target.pos[0] in self.head_cpos and not visited[i]:
						Q.append(i)
						visited[i]=True
				
				groups.append(group)
				
			#~ print ("{}: after while".format(os.getpid()))

			#~ for el, tok in sentence.items():
				#~ if tok.pos[0] in self.lexical_cpos:
					#~ self.vocabulary[tok.lemma]+=1
						
			
			#~ print ("{}: before enumerate(groups)".format(os.getpid()))

			for i, g in enumerate(groups):		
				e_0 = [x[0][0] for x in g]
				#~ print(e_0)
				if not all(x in ["*", "_"] for x in e_0):
					#~ print("{}/{}: {}".format(i,len(groups),g))
					#~ input()

						for n in range(1, len(g)+1):
							
							subsets = set(itertools.combinations(g, n))
							
							for s in subsets:
								
								s = sorted(s, key = lambda x:x[0])
								
								elements = [e[0] for e in s]
								elements_0 = [e[0] for e in elements]
								labels = [e[1] for e in s]
							
								if elements_0.count("*")<= self.max_wildcards and elements_0.count("_") <= self.max_wildcards:
															
									self.items[" ".join(elements)]["|".join(labels)]+=1
									
									#add structure
									sorted_labels = sorted(labels)
									self.structures["|".join(sorted_labels)]+=1
				else:
					pass
					#~ print(str(i)+"/"+str(len(groups))+": gruppo escluso senza item lessicali, "+str(len(g)))
			
			#~ print ("{}: after enumerate(groups)".format(os.getpid()))

	def dump_relations(self, fobj_deprel):
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
				fobj_deprel.write(node + "\t" + label + "\t" + str(labels[lab_group]) + "\n")
	
	
	def dump_vocabulary(self, fobj):
		
		to_write = self.vocabulary
		
		for lemma, freq in sorted(to_write.items()):
			
			fobj.write(lemma + "\t" + str(freq) + "\n")

	def dump_structures(self, fobj):
		
		to_write = self.structures
		
		for struct, freq in sorted(to_write.items()):

			fobj.write(struct + "\t" + str(freq) + "\n")
		

		

if __name__ == "__main__":
	pass
	#TODO: add test

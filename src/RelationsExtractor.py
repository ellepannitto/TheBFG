import os
import itertools
from collections import *
import gzip

# Own libraries:
import CorpusReader as Reader
import DepCCToken
import config



def print_for_debug(sentence, rels):
	print "[DEBUG] - sentence:"
	print "\n".join(sentence)
		
	#~ numbers = set()
	#~ for x, y, z in rels:
		#~ numbers.add(x)
		#~ numbers.add(y)
		
	#~ print
	#~ print "[DEBUG] - interesting portion of sentence:"
	#~ for x in sorted(numbers):
		#~ print sentence[x]
	#~ print
	
	print "[DEBUG] - relations"
	#~ for x in sorted(rels, key=lambda a: a[1]):
	for x in sorted(rels):
		print x, rels[x]
	print
	
	#~ raw_input()




# This functions just checks whether a sentence is enough and not too long, 
# as parsing errors are more frequent in longer sentences, 
# and sentences that are too short may be incomplete 
# or contain mistakes of some kind.

def test_sentence_length (sentence):

	sentence_length = len(sentence)

	return sentence_length >= config.min_sentence_length and sentence_length <= config.max_sentence_length




class RelationsExtractor:
	"""
	
	"""
	
	def __init__(self, testfunction):
		"""
		Initializes an extractor, given a test function. 
		The function is meant to filter sentences on some criteria we can choose, as the corpus might be very noisy.
		"""
		
		self.test = testfunction
		
		self.items = defaultdict(list)
		
		
		# Relations I'm not considering at all: 
		# "abbrev", "appos", "attr", "aux", "auxpass", "cc", "complm", "cop", "dep", "det", "mark", "nn", "null", 
		# "number", "parataxis", "predet", "pred", "prep", "punct", "rel"
		
		# Relations I'm not considering since they're considered elsewhere: 
		# "nsubjpass", "csubjpass", "pobj", "pcomp", "ROOT"

		# Relations I would like to consider somehow: 
		# "expl", "num"+"measure", "neg", "poss", "possessive", "preconj", "prt", "quantmod"(?), "tmod"
		
		# Relations we're taking into consideration. 
		# Ignore the "lambda: True" thing.
		# It is just in case we need different functions depending on the kind of relation.

		"""


		"""




		self.switch_relations = {
			"acomp" : lambda: True, # adjectival complement
			"advcl" : lambda: True, # adverbial clause modifier 
			"advmod":lambda: True, # adverbial modifier
			"amod": lambda: True, # attributive adjectival modifier
			"ccomp": lambda: True, # clausal complement with internal subject
			"conj": lambda: True, # conjunct
			"csubj": lambda: True, # clausal subject
			"dobj": lambda: True, # direct object
			"infmod": lambda: True, # infinitival modifier 
			"iobj": lambda: True, # indirect object 
			"nsubj": lambda: True, # nominal subject
			"partmod": lambda: True, # participial modifier
			"purpcl": lambda: True, # purpose clause modifier
			"rcmod": lambda: True, # relative clause modifier
			"xcomp": lambda: True # clausal complement with external subject
		}
		
	



	def set_vocabulary(self, vocab_dict):

		self.vocabulary = vocab_dict
	





	def parse_file(self, f, TokenClass):
		"""
		Parses a file given a class to represent tokens.
		The function iterates on the sentences and processes each sentence to obtain relations. 
		"""
		#As for now, the function also prints the whole sentence and the list of extracted n-uples.
		
		#~ newfile = open(f)
		newfile = gzip.open(f, "rb")

		self.reader = Reader.CorpusReader(newfile)
		
		#~ fout = gzip.open("../data/graph/"+os.path.basename(f)+".out.gz", "wb")
		
		n = 0
		
		for sentence in self.reader:

			n += 1

			if self.test(sentence):

				parsed_sent = self.parse_sent (sentence, TokenClass)
				#~ rels = self.process(parsed_sent)
				self.process(parsed_sent)
			
			if not n%10000:

				print "leggo frase", n	

			#~ else:#DEBUG
				#~ print "[DEBUG] - ignoring sentence here"
							
		#~ print_to_save(fout, self.items)

		
		#~ fout.close()		








	def parse_sent (self, raw_sentence, TokenClass):
		"""
		Parses a sentence from a raw string and given a class to build each token
		"""
		
		
		#preprocess steps to add eventually:
		# - normalize proper nouns to placeholder
		# - normalize other categories to placeholders (quantities, numbers, pronouns(!)...)
		# - filter lemmas on frequency
		
		B_ne = -1
		map_ne = {}
		sentence = {}

		for token in raw_sentence:

			token = TokenClass(token)
			sentence[token.id_ord] = token


			#this line is meant to merge particles with verbs, so phrasal verbs are reconstructed.
			if token.rel == "prt":

				if token.pord in sentence:

					sentence[token.pord].add_part(token.lemma)

				else:

					print "DEBUG - head of particle not in sentence"
					print raw_sentence
					print token.pord


			# You can ignore this part for now, I was just trying to collpse NEs into single nodes, but it seems a bit harder than expected
			
			#~ if token.ne[0] == "B":
				#~ B_ne = token.id_ord
				#~ map_ne[token.id_ord] = [B_ne]
			#~ if token.ne[0] == "I":
				#~ map_ne[B_ne].append(token.id_ord)	
			#~ if token.rel == "nn":
				#~ if not token.pord in map_ne:
					#~ map_ne[token.pord] = []
				#~ map_ne[token.pord].append(token.id_ord)
				
			#~ if token.rel == "nn" and not token.enhanced_rel == "":	
				#~ print "problema!"
				#~ raw_input()
		#~ for beginner, parts in map_ne.items():
			
			#~ h = []
			#~ for p in parts:
				#~ father = sentence[p].pord
				#~ if not father in parts or father == p:
					#~ h.append(p)
			#~ if len(h)>1:
				#~ print h
				#~ raw_input()

		#normalize each token (see normalizing function in class token)
		for id_ord in sentence:

			token = sentence[id_ord]

			token.normalize(self.vocabulary)
				
		#postprocess steps:
		# - collapse named entities to single token
		# - collapse frequent expressions (noun + preposition for example...) to single token
		# - check for light verbs or other kind of phenomena
		# - how do we treat negation/polarity in general?
		
		#I would like to perform a series of tests before going on with the process:
		# - is the sentence long enough? (e.g. len >5)
		# - is the sentence not too long (in order to avoid too many parsing errors)? (e.g. len <20)
		# - does the sentence contain strange symbols or strange strings? (such as unsplit sentences)
		# - is there at least a verb in the sentence?			
		# - is the sentence a question?
		
		
		# to handle:
		# - conjunctions (maybe nothing to be handled
		# - add subjects for xcomp (?)
		
		return sentence
				





	def process (self, sentence):
		"""
		This is the core function of the whole script. Given a sentence in the following shape: s = {id_1: Token1, id_2:Token2...}, returns a set of items (n-uples) formed by two ore more ids of items in relation with each other, and a label to represent the relation.
		"""

		# this first part computes a set of dependencies for each node (so that we know all the children of a certain node), and chooses the root of the sentence (this is just the element labeled as ROOT for now, but we might need more refined solutions for different corpora...)
		
		deps  = {}
		root = None

		for id_ord in sentence:

			token = sentence[id_ord]


			if not token.pord in deps:

				deps[token.pord] = []

				
			deps[token.pord].append((id_ord, token.rel))


			if token.enhanced_pord > 0:


				if not token.enhanced_pord in deps:

					deps[token.enhanced_pord] = []


				deps[token.enhanced_pord].append((id_ord, token.enhanced_rel))	

			
			if token.rel == "ROOT" and token.POS[0] in ["V", "N", "J"]:

				root = id_ord
		
		#here a sort of queue is implemented (I'm not using any pre-defined class since in the end it was easier to use lists. If things get more complicated I'm going to define a dedicated queue class.
		#The idea is that the queue contains the root at the begininng, and navigated the dependencies starting from there.
		#items is a set that contains all the tuples representing relations, they should be formed by a series of ids and the edge label as last element. As for now they're only pairs in the form (id_head, id_dependant, relation_label), because we have not yet defined the algorithm.
		
		#As for now it works like this:
		# - consider the head H and it's dependants D
		# - for each dependants d in D:
		#   - if the relation rel is interesting add (H, d, rel) to the interesting items
		#   - if it is a noun or a verb, add d to the queue Q
		#   - add its dependants to the current dependencies D, with extendend relation (e.g. if I'm looking at a 


		groups = []		

		if root:

			Q = [root]

			while Q:

				x = Q.pop()
				
				curr_el = sentence[x]

				group = [(curr_el.lemma, "ROOT")]
				
				curr_deps = []

				if x in deps:

					curr_deps = [(i, j) for i, j in deps[x] if not i == x]			

				for i, r in curr_deps:

					target = sentence[i]

					#~ if target.POS[0] in ["V", "N", "J", "R"] and target.lemma in _SELECTEDLEMMAS:

					if target.POS[0] in ["V", "N", "J", "R"] and target.rel not in ["cop", "prt", "nn", "aux", "auxpass"]:

						group.append((target.lemma, r))

					elif i in deps:

						curr_deps.extend(deps[i])
						
					if target.POS[0] in ["V", "N", "J"]:

						Q.append(i)

				groups.append(group)
		
		for i in range(len(groups)):

			g1 = groups[i]
			
			for n in range(2, len(g1)+1):
				
				subsets = set(itertools.combinations(g1, n))
				
				for s in subsets:

					s = sorted(s, key = lambda x:x[0])
					
					elements = [e[0] for e in s]

					elements_0 = [e[0] for e in elements]

					labels = [e[1] for e in s]
				
				#~ print elements
				#~ print elements_0

				#if (elements_0.count("*") + elements_0.count("_")) * 1.0 / len(elements) <= config.low_frequency_threshold:
				if elements_0.count("_") > elements_0.count("*"):

					#~ print elements
					#~ print elements_0
					#~ print (elements_0.count("*")+elements_0.count("_"))*1.0/len(elements)
					#~ raw_input()	

					self.items[tuple(elements)].append(tuple(labels))
			
			
			#GENERIC ASSOCIATIONS
			#~ for j in range(i, len(groups)):
				#~ g2 = groups[j]
				
				#~ for x in g1:
					#~ for y in g2:
						#~ if not x[0] == y[0] and not x[0][0]=="_" and not y[0][0]=="_":
							#~ self.items[tuple(sorted([x[0], y[0]]))].append(tuple(["genassoc"]))

		#~ return items


	def dump_relations(self, fobj):
	
		for elements, labels in sorted(self.items.items()):
			#~ print elements
			#~ print labels
			#e = " ".join(elements)
			counter = Counter(labels)
			
			for l in counter:

				n = counter[l]
				
				if len(l)>1:
					
					new = zip(elements, l)
					
					nodes = " ".join([x[0] for x in new])

					edge = "|".join([x[1] for x in new])
					
				else:

					nodes = " ".join(elements)

					edge = l[0]
					
				#~ print nodes, "\t", edge	
				fobj.write(nodes + "\t" + edge + "\t" + str(n) + "\n")	
				#~ raw_input()
				#~ fobj.write(e+"\t"+"|".join(l)+"\n")





if __name__ == "__main__":
	
	rex = RelationsExtractor(test_sentence_length)
	
	#~ rex.parse_file("../corporasample/DepCCsample", DepCCToken.DepCCToken)

	rex.parse_file(config.first_DepCC_file, DepCCToken.DepCCToken)

import CorpusReader as Reader
import DepCCToken

class RelationsExtractor:
	"""
	
	"""
	
	def __init__(self, testfunction):
		"""
		Initializes an extractor, given a test function. The function is meant to filter sentences on some criteria we can choose, as the corpus might be very noisy.
		"""
		
		self.test = testfunction
		
		# - relations I'm not considering at all: "abbrev", "appos", "attr", "aux", "auxpass", "cc", "complm", "cop", "dep", "det", "mark", "nn", "null", "number", "parataxis", "predet", "pred", "prep", "punct", "rel"
		# - relations I'm not considering since they're considered elsewhere: "nsubjpass", "csubjpass", "pobj", "pcomp", "ROOT"
		# - relations I would like to consider somehow: "expl", "num"+"measure", "neg", "poss", "possessive", "preconj", "prt", "quantmod"(?), "tmod"
		
		#relations we're taking into consideration. Ignore the "lambda: True" thing, it is just in case we need different functions depending on the kind of relation
		self.switch_relations = {
			"acomp" : lambda: True, 
			"advcl" : lambda: True, 
			"advmod":lambda: True, 
			"amod": lambda: True, 
			"ccomp": lambda: True, 
			"conj": lambda: True,
			"csubj": lambda: True,
			"dobj": lambda: True,
			"infmod": lambda: True,
			"iobj": lambda: True,
			"nsubj": lambda: True,
			"partmod": lambda: True,
			"purpcl": lambda: True,
			"rcmod": lambda: True,
			"xcomp": lambda: True
		}
		
	
	def parse_file(self, f, TokenClass):
		"""
		Parses a file given a class to represent tokens.
		The function iterates on the sentences and processes each sentence to obtain relations. 
		"""
		#As for now, the function also prints the whole sentence and the list of extracted n-uples.
		
		newfile = open(f)
		self.reader = Reader.CorpusReader(newfile)
		
		for sentence in self.reader:
			if self.test(sentence):
				parsed_sent = self.parse_sent (sentence, TokenClass)
				
				rels = self.process(parsed_sent)
				
				
				print "\n".join(sentence)
				for x in rels:
					print x
					
				numbers = set()
				for x, y, z in rels:
					numbers.add(x)
					numbers.add(y)
					
				print
				for x in sorted(numbers):
					print sentence[x]
				print
				#~ raw_input()
				
				

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
			print token
			token = TokenClass(token)
			sentence[token.id_ord] = token


			#this line is meant to merge particles with verbs, so phrasal verbs are reconstructed.
			if token.rel == "prt":
				sentence[token.pord].add_part(token.lemma)


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
			token.normalize()
				
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

			if token.enhanced_pord>0:
				if not token.enhanced_pord in deps:
					deps[token.enhanced_pord] = []	
				deps[token.enhanced_pord].append((id_ord, token.enhanced_rel))	
			
			if token.rel == "ROOT":
				root = id_ord
		
		
		items = set()
		Q = [root]
		while Q:
			curr_el = sentence[Q[0]]
			
			curr_deps = []
			if Q[0] in deps:
				curr_deps = [(x, y) for x, y in deps[Q[0]] if not x == Q[0]]
			
			print "[DEBUG] Queue:", Q
			print "[DEBUG] current element:", curr_el.lemma
			print "[DEBUG] current dependencies:", curr_deps
			
			for i, r in curr_deps:
				print "[DEBUG] looking at relation:", i, r
				if i in deps:
					print "[DEBUG] dependencies of element", i, ":", deps[i]
				else:
					print "[DEBUG] dependencies of element", i, ": []"
				target = sentence[i]
				
				if r in self.switch_relations or "prep_" in r:
					items.add ((Q[0], i, r))
					if target.pos[0] in ["N", "V"]:
						Q.append(i)
				else:
					if i in deps:
						curr_deps.extend(deps[i])	
				
						
				print "[DEBUG] current dependencies:", curr_deps
				print "[DEBUG] current items:", items
				raw_input()
				
			Q = Q[1:]
			raw_input()

		return sorted(items)
	

if __name__ == "__main__":
	
	
	#this functions just checks whether a sentence is enough and not too long, as parsing errors are more frequent in longer sentences, and sentences shorter than 6 may well be incomplete sentences or mistakes of some kind
	def testlen (s):
		return len(s)>6 and len(s)<20



	rex = RelationsExtractor(testlen)
	
	rex.parse_file("../corporasample/DepCCsample", DepCCToken.DepCCToken)

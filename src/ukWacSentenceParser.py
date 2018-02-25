import Sentence

class ukWacSentenceParser:
	
	def __init__(self, parameters):
		
		self.TokenClass = parameters["token_class"]
		self.vocabulary = parameters["vocab_list"]
		self.head_CPoS = parameters["head_cpos"]
		self.lexical_CPoS = parameters["lexical_cpos"]
		self.max_distance = parameters["max_distance"]	
	
	def parse_sent (self, raw_sentence):

		sentence = {}
		for token in raw_sentence:
			token = self.TokenClass(token)
			sentence[token.id_ord] = token
			if token.rel == "PRT":
				if token.pord in sentence:
					sentence[token.pord].add_part(token.lemma)
					token.pord = 0
				else:
					print("DEBUG - head of particle not in sentence")
					print(raw_sentence)
					print(token.pord)
		
		deps = {}
		roots = []
	
		for id_ord, token in sentence.items():
			if not id_ord in deps:
				deps[id_ord] = []
			if not token.pord in deps:
				deps[token.pord] = []
			deps[token.pord].append(id_ord)
			if token.rel == "ROOT" and token.pos[0] in self.head_CPoS:
				roots.append(id_ord)
			
				
		new_deps = []
		Q = roots
		r = None
		while Q:
			r = Q[0]			
			current_id = Q[0]
			Q = Q[1:]
			
			
			current_token = sentence[current_id]
			current_deps = [x for x in deps[current_id]]

			for d in current_deps:
				t = sentence[d]
				
				if t.pos[0] in self.head_CPoS:
					Q.append(d)
					new_deps.append( (current_id, (d, t.rel)) )
				
				elif t.pos[0] in self.lexical_CPoS:
					new_deps.append( (current_id, (d, t.rel)) )
				
				else:
					current_deps.extend([x for x in deps[d]])
					
				
				
		
		new_deps_tmp = {x : [] for x, y in new_deps}
		for x, y in new_deps:
			new_deps_tmp[x].append(y)
		
		for x in new_deps_tmp:
			
			for y, rel in new_deps_tmp[x]:
				t = sentence[y]
				if not x == t.pord:
					#~ print("{} ---- {}".format(sentence[x], sentence[t.pord]))
					
					father = sentence[t.pord]
					if t.rel == "PMOD":
						t.rel+="_"+father.lemma
					t.pord = x
					#~ print("new token: {}".format(t))
#					print()
					#~ print("")
				#~ print (str(x)+"\t"+str(t.pord))
			
		#~ print("\n".join(raw_sentence))
		#~ print(new_deps_tmp)
		#~ input()
		
		return Sentence.Sentence(sentence, r, {x:[y[0] for y in new_deps_tmp[x]] for x in new_deps_tmp})
		
	
	
if __name__ == "__main__":
	
	import CorpusReader
	import ConfigReader
	import FrequencyLoader
	import tests
	#~ import codecs
	cnf = ConfigReader.ConfigMap("../data/confs/provaukwac.cnf")
	
	parameters = cnf.parse()
	_VOCAB_LISTS = {x:FrequencyLoader._set_from_file(open(parameters["vocabulary_folder"]+x+"_frequency."+parameters["corpus"]), parameters["min_frequency"]) for x in parameters["lexical_cpos"]}
	parameters["vocab_list"] = _VOCAB_LISTS

	cr = CorpusReader.CorpusReader(open("../../altri_corpora/ukwac1.head.xml", "r", encoding="ascii"), "<")
	filterer = tests.Filterer (parameters)
	
	sp = ukWacSentenceParser(parameters)
	for s in cr:
		if filterer.filter(s):
			parsed_sentence = sp.parse_sent(s)
			print(parsed_sentence)
			input()
		#~ print (s)
		#~ input()
	

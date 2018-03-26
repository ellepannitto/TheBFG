from py2neo import *
from functools import lru_cache
import math
import collections
import _utils
import gzip
import copy

class GraphQuery:
	def __init__(self, parameters):
		self.user = parameters["user"]
		self.lexical_cpos = parameters["lexical_cpos"]
		self.visited = set()
	
	def load_graph (self, user, pwd):
		self.graph = Graph('http://localhost:7474/db/data', user=user, password=pwd)	
		
	def sum_vocabulary (self):
		self.total_lemmas = {v:0 for v in self.lexical_cpos}
		self.number_lemmas = {v:0 for v in self.lexical_cpos}
		
		for pos in self.total_lemmas:
			nodeslist = self.graph.run("MATCH (a) WHERE a.user ='"+self.user+"' and a.pos = '"+pos+"' return a order by a.frequency desc")
			
			while nodeslist.forward():
				curr_node = nodeslist.current()["a"]
				self.total_lemmas[pos]+=curr_node["frequency"]
				self.number_lemmas[pos]+=1

		self.len_corpus = sum([x[1] for x in self.total_lemmas.items()])
		#~ print(self.total_lemmas)
		#~ input()
	
	@lru_cache(maxsize=1024)
	def retrieve_connected (self, struct_id):
		nodes_connected_to_curr_struct = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND ID(n) = "+str(struct_id)+" return a, r, ID(n) as id_n")
		
		ret = []
		
		while nodes_connected_to_curr_struct.forward():
			curr = nodes_connected_to_curr_struct.current()
			ret.append(curr["a"])
		
		return ret

	@lru_cache(maxsize=1024)
	def retrieve_structures(self, node):
		
		lemma = node["lemma"]
		pos = node["pos"]
		tok = node
		f_tok = tok["frequency"]
		
		
		structlist = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND a.lemma = '"+lemma+"' and a.pos='"+pos+"' return n, ID(n) as id_n, r order by n.frequency desc")
		
		structs_weighted = []
		
		while structlist.forward():
			
			curr_struct = structlist.current()
			f_curr_struct = curr_struct["n"]["frequency"]
			curr_relation = curr_struct["r"]._Relationship__type
			
						
			nodes_connected_to_curr_struct = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND ID(n) = "+str(curr_struct["id_n"])+" and not a.lemma = '"+lemma+"' return a, r, ID(n) as id_n")
			
			list_to_query = []
			while nodes_connected_to_curr_struct.forward():
				current = nodes_connected_to_curr_struct.current()
				
				curr_node = (current["a"]["lemma"], current["a"]["pos"])
				node_relation = current["r"]._Relationship__type
				
				list_to_query.append((curr_node, node_relation))
				#~ print(list_to_query)
				#~ input()
			
			#TODO: handle named entities and such things
			if len(list_to_query) > 0:
				
				i=0
				list_match = []
				list_where = []
				for current, deprel_curr in list_to_query:
				
					lemma_curr = current[0]
					pos_curr = current[1]
					
					m = "(x"+str(i)+")-[:"+deprel_curr+"]-(s:Struct)"
					w = "x"+str(i)+".lemma = '"+lemma_curr+"'"
					w_pos = "x"+str(i)+".pos = '"+pos_curr+"'"
					
					list_match.append(m)
					list_where.append(w)
					list_where.append(w_pos)
					i+=1
				
				#~ query = "match (x)-[:"+curr_relation+"]-(s:Struct), "	
				query = "match "
				query += ", ".join(list_match)
				query += " with s, size(()-[]-(s:Struct)) as degree"
				query+=" where "
				query+=" and ".join(list_where)
				#~ query+=" and degree="+str(i+1)+" return x, s"
				query+=" and degree="+str(i)+" return s"
				
				#~ print(query)
				#~ input()
				
				new_structs = self.graph.run(query)
				
				list_to_delete_asap = []
				while new_structs.forward():
					list_to_delete_asap.append((new_structs.current()["s"], new_structs.current()["s"]["text"]))
				
				
				struct_bare = sorted(list_to_delete_asap, key = lambda x: len(x[1]))[0][0]
				#~ print (struct_bare)
				#~ input()
				
				#~ print("f_curr_struct {}, len_corpus {}, f_tok {}, struct_bare_f {}".format(f_curr_struct, self.len_corpus, f_tok, struct_bare["frequency"]))
				#~ input()
				
				#~ try:
				mi = f_curr_struct*math.log(self.len_corpus*f_curr_struct/(f_tok*struct_bare["frequency"]), 2)
				#~ except:
					#~ mi = 0
				
				structs_weighted.append((curr_struct, mi))
				
		sorted_structs_weighted = sorted(structs_weighted, key = lambda x: x[1], reverse = True)
		
		return sorted_structs_weighted
			
	def old_random_walk (self, start_lemma, start_pos, length):
		path = ""
		
		self.visited = set()
		
		curr_lemma = start_lemma
		curr_pos = start_pos
		
		i=0
		while length > 0:
			i+=1
			path+=curr_lemma+"/"+curr_pos+" "
			#~ print(curr)
			self.visited.add(curr_lemma+"/"+curr_pos)
			
			node = self.graph.run("MATCH (a) WHERE a.user ='"+self.user+"' and a.lemma='"+curr_lemma+"' and a.pos='"+curr_pos+"' return a order by a.frequency desc").evaluate()
			structs = self.retrieve_structures(node)
			#~ print (structs)
			new_lemmas = collections.defaultdict(int)

			for s in structs:
				lmi = s[1]
				if lmi > 0:
					#~ print (s)
					nodes = self.retrieve_connected(s[0]["id_n"])
					
					for n in nodes:
						lemma = n["lemma"]
						pos = n["pos"]
						if not lemma+"/"+pos in self.visited:
							new_lemmas[(lemma, pos)]+=lmi
			
			sum_lmis = sum([y for x, y in new_lemmas.items()])
			
			new_lemmas = {x: y/sum_lmis for x, y in new_lemmas.items()}
			
			sortedlist = sorted(new_lemmas.items(), key=lambda x: x[1], reverse=True)
			#~ print(sortedlist)
			#~ input()
			
			if len(sortedlist)>0:
				pick = _utils._random_pick(sortedlist)
				curr_lemma = pick[0]
				curr_pos = pick[1]
				length -=1
			else:
				length = 0
				
			
			
		if i>1:
			print(path)


	def random_walk (self, start_lemma, start_pos, length):
		path = ""
		
		self.visited = set()
		
		curr_lemma = start_lemma
		curr_pos = start_pos
		
		i=0
		while length > 0:
			i+=1
			path+=curr_lemma+"/"+curr_pos+" "
			#~ print(curr)
			self.visited.add(curr_lemma+"/"+curr_pos)

			structs = self.graph.run("MATCH (a:Lemma)-[r]-(s:Struct) WHERE a.user ='"+self.user+"' and a.lemma='"+curr_lemma+"' and a.pos='"+curr_pos+"' return s, r.MI, ID(s) as id_s order by r.MI desc")
			
			new_lemmas = collections.defaultdict(int)
			
			while structs.forward():
				s = structs.current()
				
				lmi = s["r.MI"]
				
				if lmi > 0:
					#~ print (s)
					nodes = self.retrieve_connected(s["id_s"])
					
					for n in nodes:
						lemma = n["lemma"]
						pos = n["pos"]
						if not lemma+"/"+pos in self.visited:
							new_lemmas[(lemma, pos)]+=lmi
			
			sum_lmis = sum([y for x, y in new_lemmas.items()])
			
			new_lemmas = {x: y/sum_lmis for x, y in new_lemmas.items()}
			
			sortedlist = sorted(new_lemmas.items(), key=lambda x: x[1], reverse=True)
			#~ print(sortedlist)
			#~ input()
			
			if len(sortedlist)>0:
				pick = _utils._random_pick(sortedlist)
				curr_lemma = pick[0]
				curr_pos = pick[1]
				length -=1
			else:
				length = 0
				
		if i>1:
			print(path)
				 		

if __name__=="__main__":
	import ConfigReader
	import sys
	
	cnf = ConfigReader.ConfigMap("../data/confs/prova0-2.cnf")
	parameters = cnf.parse()


	gq = GraphQuery(parameters)
	gq.load_graph("neo4j", sys.argv[1])
	gq.sum_vocabulary()

	#~ gq.create_matrix(gzip.open("../data/edges/matrice.gz", "wt"))

	#todo: 	avoid loops - done!
	#		consider PoS - done!
	#		consinder syntax
	#~ for l in ["book", "author", "computer"]:
	
	
	#~ lemmas = gq.graph.run("match (a:Lemma) with a, size((a)-[]-()) as degree where degree > 1 return a.lemma as lemma, a.pos as pos, a.frequency as freq, degree")
	
	#~ gq.random_walk("retweet", "V", 10)
	
	lemmas = gq.graph.run("match (a:Lemma) return a.lemma as lemma, a.pos as pos, a.frequency as freq")
	
	while lemmas.forward():
		l = lemmas.current()
		
		#~ print(l)
		
		lemma = l["lemma"]
		pos = l["pos"]
		f = l["freq"]
		#~ deg = l["degree"]
		
		#~ print("{} {} {}".format(lemma, pos, f))
		#~ print("effettuo "+str(int(math.log(f,2)))+" random walks lunghe "+str(deg))
		#~ input()
		
		for i in range(30+int(math.log(f,2))):
		#~ for i in range(1):
			gq.random_walk(lemma, pos, 20)
			#~ gq.random_walk(lemma, pos, 2)

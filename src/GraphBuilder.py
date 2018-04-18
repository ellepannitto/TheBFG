from py2neo import *
import gzip
from functools import lru_cache
import math
import re


class GraphBuilder:
	
	def __init__(self, parameters):
		
		self.user = parameters["user"]
		
		self.source_folder = parameters["output_folder"]
		self.corpus = parameters["corpus"]
		
		self.vocab_file = self.source_folder+"sorted."+self.corpus+".voc.gz"
		self.struct_file = self.source_folder+"sorted."+self.corpus+".struct.gz" 
		self.edges_file = self.source_folder+"sorted."+self.corpus+".edges.deprel.gz"
		
		self.lexical_cpos = parameters["lexical_cpos"]
		
		self.minimum_struct_frequency = parameters["min_struct"]
		
		self.ver = parameters["name"]
	
	@lru_cache(maxsize=8192)
	def get_node (self, lma, cpos):
		n = None
		try:
			n = self.graph.run("MATCH (a) WHERE a.user= '"+self.user+"' AND a.lemma = '"+lma+"' AND a.pos = '"+cpos+"' return a", lemma = lma).evaluate()
		except:
			print ("problema ricerca nodo: {}".format(lma))	
		return n	
		
	def remove_isolated(self):
		self.graph.run("match (n) where not (n)-[]-()  delete n")
		#TODO: remove nodes which have only generic associations
		
	def remove_onetoone(self):
		self.graph.run("match (a:Lemma)-[r]-(n:Struct) with r, a, size((a)-[]-()) as degree_a, n, size(()-[]-(n)) as degree_n where degree_a = 1 and degree_n = 1 delete r, a, n")
		#TODO: remove nodes which have only generic associations
		
	def reset_graph(self):
		self.graph.run("MATCH (a) WHERE a.user= '"+self.user+"' OPTIONAL MATCH (a)-[r]-() DELETE a,r")
	
	def load_graph (self, user, pwd):
		self.graph = Graph('http://localhost:7474/db/data', user=user, password=pwd)
		return self.graph
		
	def load_vertices (self):

		i = 0

		tx=None
		first=True
		with gzip.open(self.vocab_file, "rt") as f:
			
			for line in f:
				#~ if not i%1000000:
				if not i%10000:
					if not first:
						tx.commit()
					first = False
					tx = self.graph.begin()
					print(i)

				linesplit = line.strip().rsplit("\t")
					
				lemmasplit = linesplit[0].rsplit("/", 1)
				#~ lemma = lemmasplit[0]
				#~ lemma = re.escape(lemmasplit[0])
				lemma = lemmasplit[0]
				if "'" in lemma or '"' in lemma:
					lemma = re.escape(lemma)
					#~ print(lemma)
					#~ input()
				pos = lemmasplit[1]

				fr = int(linesplit[1])
				if pos in self.lexical_cpos and fr>self.minimum_struct_frequency:
					#~ print(lemma + " " + pos)
					#~ input()
					n = Node("Lemma", lemma = lemma, pos = pos[0], frequency = fr, user = "Ludovica", ver = self.ver)
					#~ print("created "+str(n))
					#~ self.total_nouns+=fr
					tx.create(n)
				i+=1

		#~ n = Node("Lemma", lemma = "*", pos = "N", frequency = 1000000, user = "Ludovica", ver = "prova1")
		#~ tx.create(n)
		#~ n = Node("Lemma", lemma = "*", pos = "J", frequency = 1000000, user = "Ludovica", ver = "prova1")
		#~ tx.create(n)
		#~ n = Node("Lemma", lemma = "*", pos = "V", frequency = 1000000, user = "Ludovica", ver = "prova1")
		#~ tx.create(n)
		tx.commit()		

		
	def load_edges_deprels (self):
		lineno = 0
		tx = self.graph.begin()
		#~ with gzip.open(self.edges_file, "rt") as f:
		with open(self.edges_file, "rt") as f:
			line = f.readline()
			linesplit = line.strip().split("\t")
				
			lemmi = linesplit[0].split()
			labels = linesplit[1].split("|")
			fr = int(linesplit[2])
			
			while fr > self.minimum_struct_frequency:
				lineno+=1
				if not lineno%10000:
					print(lineno)
					
				#~ try:
				#~ if any(x[0] not in ["_", "*"] for x in lemmi):
				args = {"user":self.user, "frequency":fr, "text": linesplit[0]+"---"+linesplit[1]}
				
				nodeslist = []
				for i, l in enumerate(lemmi):
					lsplit = l.rsplit("/", 1)
					pos = lsplit[1]
					
					l = lsplit[0]
					if "'" in l or '"' in l:
						l = re.escape(l)
					
					lab = labels[i]
					nodo = self.get_node(l, pos[0])
					if nodo:
						nodeslist.append((nodo, lab))
				
				
				nodo_sr = Node("Struct", **args)
				
				tx.create(nodo_sr)
				for nodo, lab in nodeslist:
					r = Relationship(nodo, lab, nodo_sr, user=self.user, MI = 0)
					tx.create(r)

				line = f.readline()				
				linesplit = line.strip().split("\t")
					
				lemmi = linesplit[0].split()
				labels = linesplit[1].split("|")
				fr = int(linesplit[2])

		tx.commit()

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
		
	def compute_lmi(self, structlist):
		
		struct_node = structlist[0]["n"]
		f_curr_struct = struct_node["frequency"]
		
		for n, curr_struct in enumerate(structlist):
			
			curr_relation = curr_struct["r"]._Relationship__type
			curr_relation_id = curr_struct["id_r"]
			f_tok = curr_struct["a"]["frequency"]
			#~ nodes_connected_to_curr_struct = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND ID(n) = "+str(curr_struct["id_n"])+" and not a.lemma = '"+lemma+"' return a, r, ID(n) as id_n")

			nodes_connected_to_curr_struct = structlist[:n]+structlist[n+1:]
			
			list_to_query = []
			for current in nodes_connected_to_curr_struct:
				
				curr_node = (current["a"]["lemma"], current["a"]["pos"])
				node_relation = current["r"]._Relationship__type
				
				list_to_query.append((curr_node, node_relation))

			
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
				
				#~ print (new_structs)
				list_to_delete_asap = []
				while new_structs.forward():
					new_structs_curr = new_structs.current()
					list_to_delete_asap.append((new_structs_curr["s"], new_structs_curr["s"]["text"]))
				
				#~ print (list_to_delete_asap)
				struct_bare = sorted(list_to_delete_asap, key = lambda x: len(x[1]))[0][0]
				
				mi = f_curr_struct*math.log(self.len_corpus*f_curr_struct/(f_tok*struct_bare["frequency"]), 2) 
				self.graph.run("Match ()-[r]-() where ID(r)="+str(curr_relation_id)+" set r.MI="+str(mi))
		
		
		
	def update_lmi(self):
		triplets = self.graph.run("MATCH (a:Lemma)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' return a, r, n, ID(n) as id_n, ID(r) as id_r order by n")
		
		triplets.forward()
		first_triple = triplets.current()
		#~ print (first_triple)
		
		#~ first_lemma = first_triple["a"]["lemma"]
		#~ first_pos = first_triple["a"]["pos"]
		first_struct = first_triple["id_n"]
		
		structlist = [first_triple]
			
		while triplets.forward():
			
			curr = triplets.current()
			#~ lemma = curr["a"]["lemma"]
			#~ pos = curr["a"]["pos"]
			id_n = curr["id_n"]
			
			if id_n == first_struct:
				structlist.append(curr)
			else:
				#~ print (structlist)
				#~ input()
				if len(structlist)>1:
					self.compute_lmi(structlist)
				
				first_struct = id_n
				
				#~ first_lemma = lemma
				#~ first_pos = pos
				structlist = [curr]
			
			#~ input()


if __name__ == "__main__":
	import ConfigReader
	import sys
	
	cnf = ConfigReader.ConfigMap(sys.argv[1])
	parameters = cnf.parse()
	
	graph = GraphBuilder(parameters)
	graph.load_graph(sys.argv[2], sys.argv[3])
	print ("graph reset")
	graph.reset_graph()
	print ("load vertices")
	graph.load_vertices()
	print ("load deprels")
	graph.load_edges_deprels()
	print ("remove isolated")
	graph.remove_isolated()
	print("remove one to one")
	graph.remove_onetoone()
	print ("sum voc")
	graph.sum_vocabulary()
	print ("update lmi")
	graph.update_lmi()

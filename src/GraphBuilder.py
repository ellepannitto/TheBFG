from py2neo import *
import gzip
from functools import lru_cache


class GraphBuilder:
	
	def __init__(self, parameters):
		
		self.user = parameters["user"]
		
		self.source_folder = parameters["output_folder"]
		self.corpus = parameters["corpus"]
		
		self.vocab_file = self.source_folder+"sorted."+self.corpus+".voc.gz"
		self.struct_file = self.source_folder+"sorted."+self.corpus+".struct.gz" 
		self.edges_file = self.source_folder+"sorted."+self.corpus+".edges.gz"
		
		self.lexical_cpos = parameters["lexical_cpos"]
		
		self.minimum_generic_frequency = parameters["min_generic"]
		self.minimum_struct_frequency = parameters["min_struct"]
	
	@lru_cache(maxsize=8192)
	def get_node (self, lma, cpos):
		n = self.graph.run("MATCH (a:"+cpos+") WHERE a.user= '"+self.user+"' AND a.lemma = '"+lma+"' return a", lemma = lma).evaluate()
		return n	
	
	def load_graph (self, user, pwd):
		self.graph = Graph('http://localhost:7474/db/data', user=user, password=pwd)

	def load_vertices (self):
		self.total_nouns = 0

		i = 0

		tx=None
		first=True
		with gzip.open(self.vocab_file, "rt") as f:
			
			for line in f:
				if not i%10000:
					if not first:
						tx.commit()
					first = False
					tx = self.graph.begin()
					print(i)
				
				if not (line[0] == "_" or line[0]=="*"):
					#~ print(line)
					linesplit = line.strip().rsplit("\t")
					
					lemmasplit = linesplit[0].rsplit("/", 1)
					lemma = lemmasplit[0]
					pos = lemmasplit[1]

					fr = int(linesplit[1])
					if pos in self.lexical_cpos:
						#~ print(lemma + " " + pos)
						#~ input()
						n = Node(pos, lemma = lemma, frequency = fr, user = "Ludovica", ver = "prova1")
						self.total_nouns+=fr
						tx.create(n)
				i+=1
		tx.commit()		
	
	def load_edges (self):
		lineno = 0
		tx = self.graph.begin()
		with gzip.open(self.edges_file, "rt") as f:
			for line in f:
				linesplit = line.strip().split("\t")
				
				lemmi = linesplit[0].split()
				labels = linesplit[1].split("|")
				fr = int(linesplit[2])
		
				lineno+=1
				if not lineno%1000:
					print(lineno)
		
#				if fr>2:
					
				try:
					if "genassoc" not in labels:
						if any(x[0] not in ["_", "*"] for x in lemmi) and fr > self.minimum_struct_frequency:
							args = {"user":self.user, "frequency":fr, "text": linesplit[0]+"---"+linesplit[1]}
							
							nodeslist = []
							for i, l in enumerate(lemmi):
								if l[0] in ["_", "*"]:
									args[labels[i]] = l
								
								else:
									lsplit = l.rsplit("/", 1)
									pos = lsplit[1]
									
									l = lsplit[0]
									lab = labels[i]
									nodo = self.get_node(l, pos)
									nodeslist.append((nodo, lab))
							
							
							nodo_sr = Node("Struct", **args)
							
							tx.create(nodo_sr)
							for nodo, lab in nodeslist:
								r = Relationship(nodo, lab, nodo_sr, user=self.user)
								tx.create(r)
								
					elif all (x[0] not in ["_", "*"] for x in lemmi) and fr > self.minimum_generic_frequency:
						

						lemma1split = lemmi[0].rsplit("/", 1)
						lemma2split = lemmi[1].rsplit("/", 1)
						
						
						node1 = self.get_node(lemma1split[0], lemma1split[1])
						node2 = self.get_node(lemma2split[0], lemma2split[1])
						genassoc = Relationship (node1, "generic", node2, user = self.user, frequency = fr)
						
						tx.create(genassoc)
							
				
				except Exception as e:
					print ("problema creazione nodo: {}".format(line))
					print(e)
					#~ print(node1)
					#~ print(node2)
					#~ input()

		tx.commit()
#		self.remove_isolated()
		
	def reset_graph(self):
		self.graph.run("MATCH (a) WHERE a.user= '"+self.user+"' OPTIONAL MATCH (a)-[r]-() DELETE a,r")


if __name__ == "__main__":
	import ConfigReader
	
	cnf = ConfigReader.ConfigMap("../data/confs/provaud.cnf")
	parameters = cnf.parse()
	
	gb = GraphBuilder(parameters)

from py2neo import *
import math

class GraphQuery:
	def __init__(self, parameters):
		self.user = parameters["user"]
		
		self.lexical_cpos = parameters["lexical_cpos"]
	
	def load_graph (self, user, pwd):
		self.graph = Graph('http://localhost:7474/db/data', user=user, password=pwd)	
		
	def sum_vocabulary (self):
		self.total_lemmas = {v:0 for v in self.lexical_cpos}
		self.number_lemmas = {v:0 for v in self.lexical_cpos}
		
		for pos in self.total_lemmas:
			nodeslist = self.graph.run("MATCH (a:"+pos+") WHERE a.user ='"+self.user+"' return a order by a.frequency desc")
			
			while nodeslist.forward():
				curr_node = nodeslist.current()["a"]
				self.total_lemmas[pos]+=curr_node["frequency"]
				self.number_lemmas[pos]+=1

		#~ print(self.total_lemmas)
		#~ input()
	
	def retrieve_structures(self, lemma):
		
		tok = self.graph.run("MATCH (a) WHERE a.user ='"+self.user+"' AND a.lemma = '"+lemma+"' return a").evaluate()
		
		f_tok = tok["frequency"]
		
		
		print(tok)
		print(f_tok)

		structlist = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND a.lemma = '"+lemma+"' return n, ID(n) as id_n, r order by n.frequency desc")
		
		structs_weighted = []
		
		while structlist.forward():
			
			curr_struct = structlist.current()
			
			f_curr_struct = curr_struct["n"]["frequency"]
			
			p_struct = 0


			#~ print (curr_struct)
			#~ print(f_curr_struct)
			
			curr_relation = curr_struct["r"]._Relationship__type
			
						
			nodes_connected_to_curr_struct = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND ID(n) = "+str(curr_struct["id_n"])+" and not a.lemma = '"+lemma+"' return a, r, ID(n) as id_n")
			
			list_to_query = []
			while nodes_connected_to_curr_struct.forward():
				curr_node = nodes_connected_to_curr_struct.current()["a"]["lemma"]
				node_relation = nodes_connected_to_curr_struct.current()["r"]._Relationship__type
				
				list_to_query.append((curr_node, node_relation))
				#~ print(curr_node)
				#~ print(node_relation)
			
			#~ print (lemma)
			#~ print(curr_relation)
			#~ print(list_to_query)
			
			#TODO: handle named entities and such things
			if len(list_to_query) > 0:
				
				i=0
				list_match = []
				list_where = []
				for lemma_curr, deprel_curr in list_to_query:
				
					m = "(x"+str(i)+")-[:"+deprel_curr+"]-(s:Struct)"
					w = "x"+str(i)+".lemma = '"+lemma_curr+"'"
					
					list_match.append(m)
					list_where.append(w)
					i+=1
				
				query = "match (x)-[:"+curr_relation+"]-(s:Struct), "	
				query += ", ".join(list_match)
				query += " with x, s, size(()-[]-(s:Struct)) as degree"
				query+=" where "
				query+=" and ".join(list_where)
				query+=" and degree="+str(i+1)+" return x, s"
				
				
				#~ print(query)
			
				new_structs = self.graph.run(query)
				print (lemma+"\t"+curr_struct["n"]["text"]+"\t"+str(f_tok)+"\t"+str(f_curr_struct))
				
				tot = 0
				while new_structs.forward():
					s = new_structs.current()["s"]
					x = new_structs.current()["x"]
					
					print ("\t"+s["text"]+"\t"+str(s["frequency"])+"\t"+x["lemma"]+"\t"+str(x["frequency"]))
					
					tot+=s["frequency"]/x["frequency"]
					#~ print(s)
					#~ print(x)
					#~ print(tot)
				
				#~ print("STRUTTURA:")
				#~ print(curr_struct)
				mi = f_curr_struct * math.log(f_curr_struct/(f_tok*tot), 2)
				#~ mi = math.log(f_curr_struct/(f_tok*tot), 2)
				#~ print(mi)
				print("\t"+str(mi))
				structs_weighted.append((curr_struct, mi))
				
				
			
			#~ print("")
			#~ input()

		sorted_structs_weighted = sorted(structs_weighted, key = lambda x: x[1], reverse = True)
		
		
		#~ for x, y in sorted_structs_weighted:
			#~ print("STRUTTURA:")
			#~ print(x["n"]["text"])
			#~ print("PESO:")
			#~ print(y)
			#~ print("")


if __name__=="__main__":
	import ConfigReader
	import sys
	
	cnf = ConfigReader.ConfigMap("../data/confs/prova0-2.cnf")
	parameters = cnf.parse()


	gq = GraphQuery(parameters)
	gq.load_graph("neo4j", sys.argv[1])
	gq.sum_vocabulary()
	gq.retrieve_structures(sys.argv[2])
	

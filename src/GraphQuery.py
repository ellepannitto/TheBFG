from py2neo import *

class GraphQuery:
	def __init__(self, parameters):
		self.user = parameters["user"]
	
	def load_graph (self, user, pwd):
		self.graph = Graph('http://localhost:7474/db/data', user=user, password=pwd)	
	
	def retrieve_structures(self, lemma):
		structlist = self.graph.run("MATCH (a)-[r]-(n:Struct) WHERE a.user ='"+self.user+"' AND a.lemma = '"+lemma+"' return n order by n.frequency desc")
		
		while structlist.forward():
			curr_struct = structlist.current()["n"]
			print(curr_struct)



if __name__=="__main__":
	import ConfigReader
	import sys
	
	cnf = ConfigReader.ConfigMap("../data/confs/provaud.cnf")
	parameters = cnf.parse()


	gq = GraphQuery(parameters)
	gq.load_graph("neo4j", sys.argv[1])
	gq.retrieve_structures("people")
	

class Sentence:
	"""
	The purpose of the class is to represent a portion of a dependency tree, composed by tokens and relations that hold among them.
	Each sentence is made up of:
	- a set of tokens, represented by an id and an object of class Token
	- the id of the root node of the tree
	- for each token, the list of id of its children in the dependency tree
	"""
	
	def __init__(self, token_list, root, deps):
		"""
		initializes a sentence given a list of tokens, its root and a representation for its inner dependency relations.
		
		Parameters:
		-----------
		token_list: dict
			dictionary containing token ids and objects of class Token, in the form {id_tok: <Token object>}
			See class Token for specifications.
			
		root: int
			id of root token of the sentence
		
		deps: dict
			dictionary of the form {id: [id_1, ..., id_k]}
			it maps each token id to its children in the dependency tree
		"""
		self.token_list = token_list
		self.root = root
		self.deps = deps
	
	def __repr__ (self):
		return "Sentence with tokens\n" +\
		       "{}\n".format ("\n".join([str(x) + "\t\t" + str(v) for x,v in self.token_list.items()]) ) +\
		       "         root={}\n".format(self.root) +\
		       "         deps={}\n".format(self.deps)

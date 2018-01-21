"""
"""
#TODO: change in kwargs
def test_length (sentence, param_list):
	"""
	Tests sentence length
	
	Parameters:
	-----------
	sentence: list
		list of lines from corpus
		
	param_list: list
		needed parameters
	
	Returns:
	--------
	bool
		true if sentence length is >= minimun and <= maximum
		false otherwise
		
	"""
	
	min_v = int(param_list[0])
	max_v = int(param_list[1])

	return len(sentence)>=min_v and len(sentence)<=max_v



map_fun = {"length": test_length}

class Filterer:
	"""
	The purpose of the Filterer class is to call the appropriate filter function passing the specified parameters
	"""
	
	def __init__ (self, parameters):
		"""
		initializes a filter
		
		Parameters:
		-----------
		parameters: dict
			dictionary of configuration parameters
			the dictionary must contain "sentencefilter_fun" index, it should be a list with len >=0
			parameters["sentencefilter_fun"][0] should contain the name of the filter function, while the rest of the list should contain appropriate parameters
			If non filter function is specified, the filter returns true for every instance.
		"""
		
		self.filter = lambda x: True
		
		if "sentencefilter_fun" in parameters:
			self.filter = lambda x: map_fun[parameters["sentencefilter_fun"][0]] ( x, parameters["sentencefilter_fun"][1:] )
		
		


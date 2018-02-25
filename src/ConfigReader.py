from __future__ import print_function
import os
import configparser

import DepCCSentenceParser, UDTreebankSentenceParser, ukWacSentenceParser
import DepCCToken, UDTreebankToken, ukWacToken

class ConfigMap:
	"""
	The class reads a configuration from file.
	It returns a map where indexes are lowercased strings from config file, and values are properly parsed from config file.
	"""
	
	def __init__ (self, cnf_file):
		"""
		Initializes a map to store parameters.
		
		Parameters:
		-----------
		cnf_file: string
			path of the file to open and read
			The file should be a standard configuration file accepted by ConfigParser class. It consists of sections, led by a [section] header (ignored by this class) and followed by name: value entries (name= value) is also accepted.
			Read more at https://docs.python.org/2/library/configparser.html
			
		At the moment, some values are casted to specific types or transformed, according to the following schema:
			first_id, last_id, workers_n, min_frequency, max_wildcards, max_distance -> int,
			delete_downloaded -> bool,
			lexical_cpos, head_cpos, sentencefilter_fun, ignored_deprels -> list
			
			
		TODO: write extensive parameters description
		
		"""
		
		self.parser = configparser.ConfigParser()
		self.parser.read(cnf_file)
		
		self.parse_value = {
			"first_id": int,
			"last_id": int,
			"delete_downloaded": lambda x: x=="True",
			"workers_n": int, 
			"min_frequency": int,
			"lexical_cpos": lambda x: x.split(","),
			"head_cpos": lambda x: x.split(","),
			"max_wildcards": int,
			"sentencefilter_fun": lambda x: x.split(","),
			"ignored_deprels": lambda x: x.split(","),
			"max_distance": int,
			"min_generic": int,
			"min_struct": int,
		}
		
		
		self.switch_tokenClass = {"depcc": DepCCToken.DepCCToken,
								"UD": UDTreebankToken.UDTreebankToken,
								"ukwac": ukWacToken.ukWacToken,}

		self.switch_sentenceClass = {"depcc": DepCCSentenceParser.DepCCSentenceParser,
									"UD": UDTreebankSentenceParser.UDTreebankSentenceParser,
									"ukwac": ukWacSentenceParser.ukWacSentenceParser,}
	
	def parse (self):
		"""
		Returns:
		--------
		dict
			a map of the parameters specified. 
			The dictionary is in the form:
				cnf parameter name (lowercased) -> parsed value specified in cnf file 
		
		"""
		
		d = {}
		
		for section in self.parser.sections():
			for option in self.parser.options(section):
				d[option] = self.parser.get(section, option)		
				if option in self.parse_value:
					d[option] = self.parse_value[option](d[option])
	
	
	
		d["token_class"] = self.switch_tokenClass[d["corpus"]]
		d["sentence_class"] = self.switch_sentenceClass[d["corpus"]]
		
		
		self.values = d
		return d
		





if __name__ == "__main__":
	

	config = ConfigMap("../data/confs/prova.cnf")

	parameters = config.parse()	
	print(parameters)

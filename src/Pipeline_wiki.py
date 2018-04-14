import os
import glob
import sys
import gzip
import urllib
from urllib import request
from multiprocessing import Pool

import ConfigReader
import tests
import CorpusReader
from FrequencyLoader import *
import FrequencyLoader
import DepCCToken
import RelationsExtractor
import _utils

def merge (folder, pattern):
	
	k = 400

	print("merge started", pattern, "...")
	
	files_to_merge = glob.glob(folder+"*"+pattern+"*")
	i = 0
	while len(files_to_merge)>1:
		
		current_files_to_merge = files_to_merge[:k]
		current_fnout = folder + "merged" + str(i) + "."+pattern+".gz"
		i+=1
		_utils._merge_sorted_files([gzip.open(f, "rt") for f in current_files_to_merge], gzip.open(current_fnout, "wt"))
		
		#~ for f in current_files_to_merge:
			#~ os.remove(f)
		
		files_to_merge = files_to_merge[k:]
		files_to_merge.append(current_fnout)


	print("sum started", pattern, "...")

	file_to_sum = current_fnout
	#~ fnout_sum = folder + "summed."+pattern+".gz"
	fnout_sum = folder + "sorted."+pattern+".gz"
	#~ fnout_sort = folder + "sorted."+pattern+".gz"

	_utils._sum(gzip.open(file_to_sum, "rt"), gzip.open(fnout_sum, "wt"))
	
	#~ print("sort started", pattern, "...")
	
	#~ _utils._sort(gzip.open(fnout_sum, "rt"), gzip.open(fnout_sort, "wt"))	

def process(partname_list):
	"""
	This function executes the core pipeline of the extraction process.
	
	Parameters:
	-----------
	partname : string
		basename of the file to process	
	
	"""
	
	partname = "_".join(partname_list[0].split("/")[-3:-1])
		
	#~ filename = parameters["corpus_folder"]+partname+".gz"
	#~ filename = partname	
	#~ partname = partname.split("/")[-1]
	#~ print ("---------------"+partname)
	#~ file_output_generic = parameters["output_folder"] + "tmp/" + partname + ".edges.generic.gz"
	file_output_deprel = parameters["output_folder"] + "tmp/" + partname + ".edges.deprel.gz"
	#provaprova
	file_output_vocabulary = parameters["output_folder"] + "tmp/" + partname + ".voc.gz"
	file_output_structures = parameters["output_folder"] + "tmp/" + partname + ".struct.gz"
	
	#~ fout_generic = gzip.open(file_output_generic, "wt")
	fout_deprel = gzip.open(file_output_deprel, "wt")
	
	fout_voc = gzip.open(file_output_vocabulary, "wt")
	fout_struct = gzip.open(file_output_structures, "wt")	
	
	print ("{}: started processing sublist {}".format(os.getpid(), partname))
	
	#TODO: check if global is needed
	parameters["vocab_list"] = _VOCAB_LISTS
	
	#~ try:
	rex = RelationsExtractor.RelationsExtractor(parameters)
	
	for filename in partname_list:

		#~ print ("{}: started processing file {}".format(os.getpid(), filename))
		
		cr = CorpusReader.CorpusReader(open(filename, "rt"))
		filterer = tests.Filterer (parameters)
		sp = parameters["sentence_class"] ( parameters )
		
		
		sentence_no = 0
		for sentence in cr:
			sentence_no +=1

			#~ if not sentence_no%100000:
				#~ print "processing sentence", sentence_no, "..."

			if filterer.filter ( sentence ) :
				
				parsed_sentence = sp.parse_sent( sentence )
				#~ print ("processing sentence: {}".format(parsed_sentence))
				rex.process(parsed_sentence)
				#~ print ("processed")
		
		#~ print ("{}: finished processing file {}".format(os.getpid(), filename))
	
	#~ rex.dump_relations(fout_generic, fout_deprel)
	rex.dump_relations(fout_deprel)

	rex.dump_vocabulary(fout_voc)
	rex.dump_structures(fout_struct)

	print ("{}: finished processing sublist {}".format(os.getpid(), partname))
	#~ input()


if __name__ == "__main__":


	#handling some possible errors...
	if len(sys.argv)<=1:
		message = "You need to specify a configuration file.\n" \
				"An example is located at ../data/confs/prova.cnf \n" \
				"Launch instructions: python Pipeline.py [cnf_filename]"
		
		sys.exit(message)


	if not os.path.isfile(sys.argv[1]):
		message = "The file "+sys.argv[1]+" does not exist.\n"\
				"Please specify the full path."
		
		sys.exit(message)


	
	cnf_filename = sys.argv[1]	


	#Part1: read configuration file and map parameters
	cnf = ConfigReader.ConfigMap(cnf_filename)
	parameters = cnf.parse()
	
	print("loaded parameters, recap:")
	for par in parameters:
		print(par, ":", parameters[par])


	#Part2: load vocabulary list
	_VOCAB_LISTS = {x:FrequencyLoader._set_from_file(open(parameters["vocabulary_folder"]+x+"_frequency."+parameters["corpus"]), parameters["min_frequency"]) for x in parameters["lexical_cpos"]}
	
	print("vocabulary loaded")
		
	#Part 3: initialize a pool of workers and begin extraction process -> the extraction is handled by the "process" function
	p = Pool(processes=parameters["workers_n"])
	
	#~ def generate_arg_list():
		#~ for root, dirs, filenames in os.walk(parameters["corpus_folder"]):

			#~ if len(filenames)>0:
				#~ sublist = [root+"/"+f for f in filenames]

				#~ print("{}: collecting files from {}...".format(os.getpid(),root))
				#~ yield sublist
		
	#~ p.map(process, generate_arg_list(), chunksize=10)
	
	arg_list = []
	for root, dirs, filenames in os.walk(parameters["corpus_folder"]):

		if len(filenames)>0:
			sublist = [root+"/"+f for f in filenames]

			print("collecting files from {}...".format(root))
			arg_list.append(sublist)
	
	
	p.map(process, arg_list)

	#~ for arg in arg_list:
		#~ process(arg)




	#Part4-5: sum and sort output
	merge (parameters["output_folder"]+"tmp/", "voc")
	merge (parameters["output_folder"]+"tmp/", "struct")
	#~ merge (parameters["output_folder"]+"tmp/", "edges.generic")
	merge (parameters["output_folder"]+"tmp/", "edges.deprel")

	os.rename (parameters["output_folder"]+"tmp/sorted.voc.gz", parameters["output_folder"]+"sorted."+parameters["corpus"]+".voc.gz" )
	os.rename (parameters["output_folder"]+"tmp/sorted.struct.gz", parameters["output_folder"]+"sorted."+parameters["corpus"]+".struct.gz" )
	#~ os.rename (parameters["output_folder"]+"tmp/sorted.edges.generic.gz", parameters["output_folder"]+"sorted."+parameters["corpus"]+".edges.generic.gz" )
	os.rename (parameters["output_folder"]+"tmp/sorted.edges.deprel.gz", parameters["output_folder"]+"sorted."+parameters["corpus"]+".edges.deprel.gz" )

	#Part 6: remove temporary output files
	print("removing files")
	
	for f in os.listdir(parameters["output_folder"]+"tmp/"):
		os.remove(parameters["output_folder"]+"tmp/"+f)

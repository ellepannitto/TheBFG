from __future__ import print_function
import os
import glob
import sys
import gzip
import urllib
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

	print("merge started", pattern, "...")
	
	files_to_merge = glob.glob(folder+"*"+pattern+"*")
	i = 0
	while len(files_to_merge)>1:
		
		current_files_to_merge = files_to_merge[:100]
		current_fnout = folder + "merged" + str(i) + "."+pattern+".gz"
		i+=1
		_utils._merge_sorted_files([gzip.open(f, "rt") for f in current_files_to_merge], gzip.open(current_fnout, "wt"))
		
		files_to_merge = files_to_merge[100:]
		files_to_merge.append(current_fnout)


	print("sum started", pattern, "...")

	file_to_sum = current_fnout
	fnout_sum = folder + "summed."+pattern+".gz"
	fnout_sort = folder + "sorted."+pattern+".gz"

	_utils._sum(gzip.open(file_to_sum, "rt"), gzip.open(fnout_sum, "wt"))
	
	print("sort started", pattern, "...")
	
	_utils._sort(gzip.open(fnout_sum, "rt"), gzip.open(fnout_sort, "wt"))	

def process(partname):
	"""
	This function executes the core pipeline of the extraction process.
	
	Parameters:
	-----------
	partname : string
		basename of the file to process	
	
	"""
		
	filename = parameters["corpus_folder"]+partname+".gz"
	file_output = parameters["output_folder"] + "tmp/" + partname + ".edges.gz"
	#provaprova
	file_output_vocabulary = parameters["output_folder"] + "tmp/" + partname + ".voc.gz"
	file_output_structures = parameters["output_folder"] + "tmp/" + partname + ".struct.gz"
	
	downloaded = False
	
	print ("started processing file {}".format(filename))

	if not os.path.exists(filename):
		downloaded = True
		
		file_url = parameters["basic_url"] + partname + ".gz"
		
		testfile = urllib.URLopener()
		testfile.retrieve(file_url, filename)
	
	#TODO: check if global is needed
	parameters["vocab_list"] = _VOCAB_LISTS
	
	try:
		cr = CorpusReader.CorpusReader(gzip.open(filename, "rt"))
		filterer = tests.Filterer (parameters)
		sp = parameters["sentence_class"] ( parameters )
		rex = RelationsExtractor.RelationsExtractor(parameters)
		
		fout = gzip.open(file_output, "wt")
		
		fout_voc = gzip.open(file_output_vocabulary, "wt")
		fout_struct = gzip.open(file_output_structures, "wt")
		
		sentence_no = 0
		for sentence in cr:
			sentence_no +=1

			#~ if not sentence_no%100000:
				#~ print "processing sentence", sentence_no, "..."

			if filterer.filter ( sentence ) :
				parsed_sentence = sp.parse_sent( sentence )
				rex.process(parsed_sentence)
		
		rex.dump_relations(fout)

		rex.dump_vocabulary(fout_voc)
		rex.dump_structures(fout_struct)
	except Exception as e:
		print(e)
		print("problems with file{}".format(filename))

	if downloaded and parameters["delete_downloaded"]:
		os.remove(parameters["corpus_folder"]+partname+".gz")

	print ("finished processing file {}".format(filename))


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
	arg_list = [str(i).zfill(5) for i in range(parameters["first_id"], parameters["last_id"])]
	p.map(process, arg_list)




	#Part4-5: sum and sort output
	merge (parameters["output_folder"]+"tmp/", "voc")
	merge (parameters["output_folder"]+"tmp/", "struct")
	merge (parameters["output_folder"]+"tmp/", "edges")

	os.rename (parameters["output_folder"]+"tmp/sorted.voc.gz", parameters["output_folder"]+"sorted.voc.gz" )
	os.rename (parameters["output_folder"]+"tmp/sorted.struct.gz", parameters["output_folder"]+"sorted.struct.gz" )
	os.rename (parameters["output_folder"]+"tmp/sorted.edges.gz", parameters["output_folder"]+"sorted.edges.gz" )

	#Part 6: remove temporary output files
	print("removing files")
	
	for f in os.listdir(parameters["output_folder"]+"tmp/"):
		os.remove(parameters["output_folder"]+"tmp/"+f)

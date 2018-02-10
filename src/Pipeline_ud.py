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


cnf = ConfigReader.ConfigMap("../data/confs/provaud.cnf")
parameters = cnf.parse()

_VOCAB_LISTS = {x:FrequencyLoader._set_from_file(open(parameters["vocabulary_folder"]+x+"_frequency."+parameters["corpus"]), parameters["min_frequency"]) for x in parameters["lexical_cpos"]}
parameters["vocab_list"] = _VOCAB_LISTS

cr = CorpusReader.CorpusReader(open("/home/ludovica/UD_English/en-ud-train.conllu"))
sp = parameters["sentence_class"] ( parameters )
rex = RelationsExtractor.RelationsExtractor(parameters)


file_output = parameters["output_folder"] +parameters["corpus"]+".edges.gz"
file_output_vocabulary = parameters["output_folder"] + parameters["corpus"]+".voc.gz"
file_output_structures = parameters["output_folder"] + parameters["corpus"]+".struct.gz"

fout = gzip.open(file_output, "wt")
fout_voc = gzip.open(file_output_vocabulary, "wt")
fout_struct = gzip.open(file_output_structures, "wt")

for sentence in cr:
	if len(sentence)>0:
		#~ print sentence
		#~ raw_input()
		#~ print "\n".join(sentence)

		parsed_sentence = sp.parse_sent( sentence )
		
		#~ print parsed_sentence.linear_repr()
		#~ raw_input()
#		print parsed_sentence
		rex.process(parsed_sentence)
		
		
rex.dump_relations(fout)
rex.dump_vocabulary(fout_voc)
rex.dump_structures(fout_struct)

fout.close()
fout_voc.close()
fout_struct.close()

_utils._sort(gzip.open(file_output, "rt"), gzip.open(parameters["output_folder"] + "sorted."+parameters["corpus"]+".edges.gz", "wt"))
_utils._sort(gzip.open(file_output_vocabulary, "rt"), gzip.open(parameters["output_folder"] + "sorted."+parameters["corpus"]+".voc.gz", "wt"))
_utils._sort(gzip.open(file_output_structures, "rt"), gzip.open(parameters["output_folder"] + "sorted."+parameters["corpus"]+".struct.gz", "wt"))

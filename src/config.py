"""
Configuration file.
"""



# I/O paths (folders, filenames, ...)
######################################

data_folder = "../data"


DepCC_folder = data_folder + "/DepCC"
temp_folder = data_folder + "/temp"
results_folder = data_folder + "/results"




sample_folder = "../corporasample"

DepCCsample = sample_folder + "/DepCCsample"

DepCC_basic_URL = "http://ltdata1.informatik.uni-hamburg.de/depcc/corpus/parsed/part-m-"







# lemma POS frequency calculation
##################################


#delete_downloaded_files = True
delete_downloaded_files = False



DEBUG = True
#DEBUG = False




# Other parameters
##################

stop_keys = ("x", "X", "q", "Q")



CoNLL_format = {
	"ID" : "word index",
	"FORM" : "word form",
	"LEMMA" : "lemma or stem of word form",
	"UPOSTAG" : "universal part-of-speech tag",
	"XPOSTAG" : "language-specific part-of-speech tag",
	"FEATS" : "list of morphological features",
	"HEAD" : "head of the current word, which is either a value of ID or zero",
	"DEPREL" : "universal dependency relation to the 'HEAD'",
	"DEPS" : "enhanced dependency graph in the form of head-deprel pairs",
	"NER" : "named entity tag"
	}

DepCC_line_map = CoNLL_format.keys()


# Source: https://arxiv.org/pdf/1710.01779.pdf





corpus_sentence_delimiter = "#"



# Range of ID of the files in the DepCC corpus
first_file_ID = 0
last_file_ID = 2


#last_file_ID = 19101





which_POS_as_heads = ["N", "V", "J", "R"]







# https://docs.python.org/2/library/multiprocessing.html

number_worker_processes = 8
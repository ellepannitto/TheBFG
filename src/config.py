"""
Configuration file.
"""



# I/O paths (folders, filenames, ...)
######################################

DepCC_basic_URL = "http://ltdata1.informatik.uni-hamburg.de/depcc/corpus/parsed/part-m-"


sample_folder = "../corporasample"
DepCCsample = sample_folder + "/DepCCsample"


data_folder = "../data"


DepCC_folder = data_folder + "/DepCC"


temp_folder = data_folder + "/temp"

results_folder = data_folder + "/results"

graph_folder = data_folder + "/graph"
vocabulary_folder = data_folder + "/vocabulary"




first_DepCC_file = DepCC_folder + "/" + "00000.gz"



# Important parameters at RUN time
####################################


#delete_downloaded_files = True
delete_downloaded_files = False


DEBUG = True
#DEBUG = False


# Range of ID of the files in the DepCC corpus
first_file_ID = 0
last_file_ID = 31
#last_file_ID = 19101












# Parameters that rarely change
####################################



stop_keys = ("x", "X", "q", "Q")



DepCC_line_map = [
	"ID", # 0) word index
	"FORM" , # 1) word form
	"LEMMA" , # 2) lemma or stem of word form
	"UPOSTAG" , # 3) universal part-of-speech tag
	"XPOSTAG" , # 4) language-specific part-of-speech tag
	"FEATS" , # 5) list of morphological features
	"HEAD" , # 6) head of the current word, which is either a value of ID or zero
	"DEPREL" , # 7) universal dependency relation to the 'HEAD'
	"DEPS" , # 8) enhanced dependency graph in the form of head-deprel pairs
	"NER" # 9) named entity tag
	]

# Source: https://arxiv.org/pdf/1710.01779.pdf


corpus_sentence_delimiter = "#"

which_POS_as_heads = ["N", "V", "J", "R"]



# https://docs.python.org/2/library/multiprocessing.html
number_worker_processes = 8


# minimal frequency for lemma
minimal_frequency_lemma = 1000

low_frequency_threshold = 0.51 


min_sentence_length = 7

max_sentence_length = 19



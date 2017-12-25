"""
The purpose of this file is to attempt a first extraction of the graph. 
This will compute a (small) sample over the first 30 parts of the DepCC Corpus.

To know:
- Proper nouns and named entities are normalized to the named entity tag or a placeholder such as NNP(S)
- Among other lemmas, only those with a frequency > 1000 are taken into consideration
- When considering an hyperedge among nodes, it may happen that some of them are low frequency lemmas. 
We impose that at least half of the lemma +1 are among the selected ones. 
This implies that binary relations are considered only when both lemmas have frequency > threshold, ternary relations when at least 2 nodes have this property and so on...
- only sentences between 6 and 20 tokens are examined
"""

import gzip
import urllib
import os


# Own libraries:
import RelationsExtractor
import DepCCToken
import config







# WARNING

if not config.delete_downloaded_files:

	print "WARNING. This script configuration does NOT delete downloaded files."

	print "If you want to proceed press ENTER."

	print "To exit, type any of [" + ', '.join(config.stop_keys) + "] + press ENTER )"

	response = raw_input()

	if response in config.stop_keys: sys.exit()





# list of vocabulary
#######################



def extract_set (filename):

	path = config.vocabulary_folder + "/" + filename

	fobj = gzip.open( path , "rb")
	
	lines = fobj.read().splitlines()
	
	return set(lines)


vocabulary_dict = {x : extract_set("bfg_" + x + "_" + str(config.minimal_frequency_lemma) + ".sorted.gz") for x in ["N", "J", "V", "R"]}



"""
The vocabulary files are :

data/vocabulary/bfg_J_1000.sorted.gz
data/vocabulary/bfg_J_3000.sorted.gz
data/vocabulary/bfg_N_1000.sorted.gz
data/vocabulary/bfg_N_3000.sorted.gz
data/vocabulary/bfg_R_1000.sorted.gz
data/vocabulary/bfg_R_3000.sorted.gz
data/vocabulary/bfg_V_1000.sorted.gz
data/vocabulary/bfg_V_3000.sorted.gz

Here are the first line for 'bfg_J_1000.sorted.gz':

other/JJ
more/JJR
new/JJ
first/JJ
good/JJ
many/JJ
such/JJ
last/JJ

"""






for file_ID in range(config.first_file_ID, config.last_file_ID):


	# define the needed input
	#########################

	proper_file_ID = str(file_ID).zfill(5)
	
	input_file_path = config.DepCC_folder + "/" + proper_file_ID + ".gz"

	if config.DEBUG : print "[config.DEBUG] - Input file: ", input_file_path 




	# if the input file does not exist,
	# it needs to be downloaded
	###########################

	if not os.path.exists( input_file_path ) :

		testfile = urllib.URLopener()

		URL = config.DepCC_basic_URL + proper_file_ID +".gz"

		# Download the file
		testfile.retrieve(url = URL, filename = input_file_path)

		# Close the connection
		testfile.close()

		if config.DEBUG : print "[config.DEBUG] - downloaded !"



	# extract relations
	###################

	# init 'RelationsExtractor'

	rex = RelationsExtractor.RelationsExtractor(RelationsExtractor.test_sentence_length)
	
	rex.set_vocabulary(vocabulary_dict)
		
	rex.parse_file(input_file_path, DepCCToken.DepCCToken)


	# output
	########

	output_path = config.graph_folder + "/" + proper_file_ID + ".gz"

	rex.dump_relations( gzip.open(output_path, "wb") )
	



	# Deletion of the temporary copy of the input files
	####################################################
	
	if config.delete_downloaded_files: 

		if config.DEBUG : print "[config.DEBUG] - removing file: " + input_file_path

		os.remove(input_file_path)






#~ rex = RelationsExtractor.RelationsExtractor(RelationsExtractor.test_sentence_length)

#~ rex.set_vocabulary(vocabulary_dict)
	
#~ rex.parse_file("../data/00000.gz", DepCCToken.DepCCToken)

#~ rex.dump_relations(gzip.open(_OUTPUT_FOLDER+"00000.gz", "wb"))

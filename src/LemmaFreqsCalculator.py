'''
	This script download gzip files from the DepCC corpus,
	count the lemma/POS combination in each of them,
	and merge the results.

	The resulting output is a gzip file where each line is of the type
	lemma/POS frequency

	Psychiatrica/NNP	12
	filibuster/NN	9
	teacher/NN	530
	Festival/NNP	199
	Festivals/NNP	3
	Festivals/NNPS	1
	Festivities/NNP	1
'''



# https://docs.python.org/2/library/os.html
import os

# https://docs.python.org/2/library/sys.html
import sys

# https://docs.python.org/2/library/gzip.html
import gzip

# https://docs.python.org/2/library/urllib.html
import urllib

# https://docs.python.org/2/library/collections.html
import collections

# https://docs.python.org/2/library/heapq.html
import heapq

# https://docs.python.org/2/library/multiprocessing.html
from multiprocessing import Pool

# Own libraries:
import CorpusReader
import config






# some parameters
#################

first_file_ID = config.first_file_ID

last_file_ID = config.last_file_ID


if len(sys.argv) > 2:

	first_file_ID = int(sys.argv[1])

	last_file_ID = int(sys.argv[2])


# retrieving the positions of the columns
lemma_p = config.DepCC_line_map.index("LEMMA") 
POS_p = config.DepCC_line_map.index("UPOSTAG") 



########################################
def count_lemma_POS_pairs(sentence, dict_file):

	for line in sentence:

		linesplit = line.split("\t")
		
		lemma = linesplit[lemma_p]

		POS = linesplit[POS_p]

		if POS[0] in config.which_POS_as_heads and any(character.isalpha() for character in lemma):

			key = lemma.strip() + "/" + POS

			dict_file[ key ] += 1




########################################
def file_lemma_POS_frequency_calculation(file_ID):

	# define the needed input
	#########################

	proper_file_ID = str(file_ID).zfill(5)

	input_file_path = config.DepCC_folder + "/" + proper_file_ID + ".gz"

	if config.DEBUG : print "[config.DEBUG] - Input file: ", input_file_path 



	# if the input file does not exist,
	# it needs to be downloaded
	#############################

	if not os.path.exists( input_file_path ) :

		testfile = urllib.URLopener()

		URL = config.DepCC_basic_URL + proper_file_ID +".gz"

		# Download the file
		testfile.retrieve(url = URL, filename = input_file_path)

		# Close the connection
		testfile.close()

		if config.DEBUG : print "[config.DEBUG] - downloaded !"


	# Unzip the file
	##################

	input_file_object = gzip.open(input_file_path, 'rb')




	# counting
	#############

	if config.DEBUG : print "[config.DEBUG] - lemmas/POS counting started for " + input_file_path

	corpus_reader = CorpusReader.CorpusReader(input_file_object)

	dict_file = collections.defaultdict(int)

	for sentence in corpus_reader:
		count_lemma_POS_pairs(sentence, dict_file)



	# sorting
	############

	sorted_lemma_POS_pairs = sorted(dict_file.items(), key = lambda x: x[0] )

	

	# saving the output
	####################

	output_file_path = config.temp_folder + "/" + proper_file_ID + ".sorted.gz"
	output_file_object = gzip.open( output_file_path, 'wb')

	if config.DEBUG : print "[config.DEBUG] - writing to file" + output_file_path

	for lemma_POS, frequency in sorted_lemma_POS_pairs:

		output_line = lemma_POS + "\t" + str(frequency) + "\n"
		output_file_object.write(output_line)
	
	output_file_object.close()



	
	# Deletion of the temporary copy of the input files
	####################################################

	if config.delete_downloaded_files: 

		if config.DEBUG : print "[config.DEBUG] - removing file: " + input_file_path

		os.remove(input_file_path)
	
	


########################################
def keyfunc(string):

	strsplit = string.strip().split("\t")

	return int(strsplit[1])




########################################
def decorated_file(filename, key):

    for line in filename: 

        yield (key(line), line)





# Calculation of the lemmas frequency for some files
#####################################################


# WARNING

if not config.delete_downloaded_files:

	print "WARNING. This script configuration does NOT delete downloaded files."

	print "If you want to proceed press ENTER."

	print "To exit, type any of [" + ', '.join(config.stop_keys) + "] + press ENTER )"

	response = raw_input()

	if response in config.stop_keys: sys.exit()






# Using a pool of workers (multiprocessing)

pool = Pool(processes = config.number_worker_processes)

#~ input_file_IDs = [i for i in range(0, 11) ]
input_file_IDs = [file_ID for file_ID in range(first_file_ID, last_file_ID)]

pool.map(file_lemma_POS_frequency_calculation, input_file_IDs)





# Merge

if config.DEBUG : print "[config.DEBUG] - start merge of files in : " + config.temp_folder

filenames = os.listdir( config.temp_folder + "/")

files = [gzip.open(config.temp_folder + "/" + filename, "rb") for filename in  filenames]

output_path = config.results_folder + "/univ_freq_merged.gz"


if os.path.exists(output_path):

	os.remove(output_path)


merged_output_file_object = gzip.open(output_path, "wb")

for line in heapq.merge(*[decorated_file(file, keyfunc) for file in files]):

    merged_output_file_object.write(line[1])

merged_output_file_object.close()    
    

print " --- Output saved in : " + output_path







############################

if config.DEBUG : print "[config.DEBUG] - removing useless files"

for filename in filenames:

	os.remove( config.temp_folder + "/" + filename)





print " --- Done ! "
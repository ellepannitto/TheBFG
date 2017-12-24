"""
Configuration file.
"""



# I/O paths (folders, filenames, ...)
######################################

data_folder = "../data"

DepCC_folder = data_folder + "/DepCC"

univariate_freq_folder = data_folder + "/univ_freq"

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






# Range of ID of the files in the DepCC corpus
first_file_ID = 0
last_file_ID = 2


#last_file_ID = 19101





which_POS_as_heads = ["N", "V", "J", "R"]







# https://docs.python.org/2/library/multiprocessing.html

number_worker_processes = 8
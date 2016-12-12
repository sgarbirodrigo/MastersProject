'''
Python 3.4.3
librosa 0.4.3
Tensorflow 0.6.0, upgraded to 0.12.0
'''

from os import path

from math import ceil

DATA_PATH = path.dirname(path.realpath(__file__)) + "/Data/AMTRecordings"


NR_OF_CLASSES = 7
INCLUDED_VESSELS = ["ferry", "nansen", "sejong", "speedboat", "svendborgmaersk", "tanker", "sub"]
# INCLUDED_VESSELS = ["speedboat", "tanker"]
# INCLUDED_VESSELS = ["ferry", "speedboat", "tanker", "sub"]
TEST_PERCENTAGE = 0.1
SAMPELING_RATE = 1000
NR_OF_FILES = 85
# 85 files in total
SAMPLES_PR_FILE = 100
SAMPLE_LENGTH = 0.5 # sec

# Only one of these can be true at once
# Describes what part of the dataset is being used as test data
USE_WHOLE_FILE_AS_TEST = True # TODO fix the other two options for recurrent networks
USE_END_OF_FILE_AS_TEST = False
USE_RANDOM_SAMPLES_AS_TEST = False

# Recurrent NN
RELATED_STEPS = 20

NOISE_ENABLED = False
NR_OF_NOISY_SAMPLES_PR_SAMPLE = 2

RESET_PICKLE = False
MOCK_DATA = False
USE_PRELOADED_DATA = True

# if NR_OF_CLASSES != len(INCLUDED_VESSELS):
#     raise ValueError

# if SAMPLES_PR_FILE * SAMPLE_LENGTH > 10:
#     raise ValueError

BATCH_SIZE = 5
EPOCS = ceil(NR_OF_FILES * SAMPLES_PR_FILE / BATCH_SIZE) # To ensure all samples being used in training
EPOCS = 50
LEARNING_RATE = 0.001
DROPOUT = 0.9
DROPOUT_ENABLED = True

ACTIVATION_FUNCTIONS = "1"
HIDDEN_LAYERS = "256"

import os
import sys
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.dataset_loader import DATASET_ROOTS  # Now it can find the src module

######### global settings  #########
GPU = True                                  # running on GPU is highly suggested
TEST_MODE = False                           # turning on the testmode means the code will run on a small dataset.
CLEAN = True                               # set to "True" if you want to clean the temporary large files after generating result
# using 'cvcl'
MODEL = 'resnext'                          # model arch: resnet18, alexnet, resnet50, densenet161
DATASET = 'imagenet'                       # model trained on: places365 or imagenet  #!this is irrelevant for cvcl
QUANTILE = 0.005      #0.005                      # the threshold used for activation
SEG_THRESHOLD = 0.04  #0.04                      # the threshold used for visualization
SCORE_THRESHOLD = 0.04  #0.04                      # the threshold used for IoU score (in HTML file)
TOPN = 8                                   # to show top N image with highest activation for each unit
PARALLEL = 1                                # how many process is used for tallying (Experiments show that 1 is the fastest)
CATAGORIES = ["object","part","scene","texture","color","material"] # concept categories that are chosen to detect: "object", "part", "scene", "material", "texture", "color"
OUTPUT_FOLDER = "experiments/net-dissect_results/"+MODEL+"_"+"c"+str(len(CATAGORIES))  # result will be stored in this folder
MODEL_FILE = None                           # the path of the model file, if it is None, the pretrained model in torchvision will be used

########### sub settings ###########
# In most of the case, you don't have to change them.
# DATA_DIRECTORY: where broaden dataset locates
# IMG_SIZE: image size, alexnet use 227x227
# NUM_CLASSES: how many labels in final prediction
# FEATURE_NAMES: the array of layer where features will be extracted
# MODEL_FILE: the model file to be probed, "None" means the pretrained model in torchvision
# MODEL_PARALLEL: some model is trained in multi-GPU, so there is another way to load them.
# WORKERS: how many workers are fetching images
# BATCH_SIZE: batch size used in feature extraction
# TALLY_BATCH_SIZE: batch size used in tallying
# INDEX_FILE: if you turn on the TEST_MODE, actually you should provide this file on your own

if MODEL != 'alexnet':
    # Use broaden dataset from main project
    DATA_DIRECTORY = DATASET_ROOTS.get('broden', 'dataset/broden1_224')
    IMG_SIZE = 224
else:
    # For alexnet use smaller size
    DATA_DIRECTORY = DATASET_ROOTS.get('broden227', 'dataset/broden1_227') 
    IMG_SIZE = 227

if DATASET == 'places365':
    NUM_CLASSES = 365
elif DATASET == 'imagenet':
    NUM_CLASSES = 1000
if MODEL == 'resnet18':
    FEATURE_NAMES = ['layer4']
    if DATASET == 'places365':
        MODEL_FILE = 'zoo/resnet18_places365.pth.tar'
        MODEL_PARALLEL = True
    elif DATASET == 'imagenet':
        MODEL_FILE = None
        MODEL_PARALLEL = False
elif MODEL == 'densenet161':
    FEATURE_NAMES = ['features']
    if DATASET == 'places365':
        MODEL_FILE = 'zoo/whole_densenet161_places365_python36.pth.tar'
        MODEL_PARALLEL = False
elif MODEL == 'resnet50':
    FEATURE_NAMES = ['layer1', 'layer2', 'layer3', 'layer4']
    if DATASET == 'places365':
        MODEL_FILE = 'zoo/whole_resnet50_places365_python36.pth.tar'
    MODEL_PARALLEL = False
    OUTPUT_FOLDER += "_l"+str(len(FEATURE_NAMES))
elif MODEL == 'resnext':
    FEATURE_NAMES = ['layer1', 'layer2', 'layer3', 'layer4']
    MODEL_PARALLEL = False
    OUTPUT_FOLDER += "_l"+str(len(FEATURE_NAMES))
elif MODEL == 'cvcl':
    # should be no larger than 4
    # FEATURE_NAMES = ['vision_encoder.model.layer1']
    FEATURE_NAMES = ['vision_encoder.model.layer1', 'vision_encoder.model.layer2', 'vision_encoder.model.layer3', 'vision_encoder.model.layer4']
    MODEL_PARALLEL = False
    OUTPUT_FOLDER += "_l"+str(len(FEATURE_NAMES))
elif MODEL == 'clip':
    FEATURE_NAMES = ['visual.layer1', 'visual.layer2', 'visual.layer3', 'visual.layer4']
    MODEL_PARALLEL = False
    OUTPUT_FOLDER += "_l"+str(len(FEATURE_NAMES))

if TEST_MODE:
    WORKERS = 1
    BATCH_SIZE = 64
    TALLY_BATCH_SIZE = 64
    TALLY_AHEAD = 16
    INDEX_FILE = 'test.csv'
    OUTPUT_FOLDER += "test"
else:
    WORKERS = 12
    INDEX_FILE = 'index.csv'
    if MODEL == 'cvcl' or MODEL == 'clip':
        BATCH_SIZE = 512 # 128
        TALLY_BATCH_SIZE = 256 # 16
        TALLY_AHEAD = 128 # 4
    else:
        BATCH_SIZE = 128 # 128
        TALLY_BATCH_SIZE = 16 # 16
        TALLY_AHEAD = 4 # 4


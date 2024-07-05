## Loading the data

Please obtain the [W&I+LOCNESS v2.1](https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz)
dataset which was published for the [Building Educational Applications 2019 
Shared Task: Grammatical Error Correction](https://www.cl.cam.ac.uk/research/nl/bea2019st/) 
and save it to `data/`.

The preprocessing script `m2_data_preprocessor.py` from this repository can 
handle the files stored at `\m2` of W&I+LOCNESS v2.1.

For training, the following folds should be used: `A.train.gold.bea19.m2`, 
`B.train.gold.bea19.m2`, `C.train.gold.bea19.m2`. 

For validation, please use: `A.dev.gold.bea19.m2`, `B.dev.gold.bea19.m2`, 
`C.dev.gold.bea19.m2`.

Tests can be run on: `N.dev.gold.bea19.m2`.
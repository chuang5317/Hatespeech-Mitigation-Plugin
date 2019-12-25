An overview of what I am doing:
    https://github.com/snorkel-team/snorkel-tutorials/blob/master/getting_started/getting_started.ipynb
    **PLEASE READ & AND GO THROUGH IT TO GET A GENERAL IDEA OF THIS PROJECT**

Install spacy:
    pip install -U spacy

Install spacy for gpu:
    pip install -U spacy[cuda]
    ** read this for more info https://spacy.io/usage/ ** 
    ** requires CUDA **
    ** requires NVIDIA GPU and driver **

Install required spacy models :
    python -m spacy download <model_name>

Install Pandas DataFrame:  **for importing CSV files**
    pip install pandas

spacy api:
    https://spacy.io/api

Install snorkel:
    pip install snorkel

Snorkel official: 
    https://github.com/snorkel-team

A Pandas DataFrame tutorial:
    https://stackabuse.com/beginners-tutorial-on-the-pandas-python-library/

Useful datasets:
    hate_speech_icwsm18
    https://github.com/aitor-garcia-p/hate-speech-dataset

CNN:
    - requires tf 2.0

tensorflow gpu requirements working on my Ubuntu 18.04 (for the api_cnn.py + cnn_train.py):
    - tensorflow 1.15 -- requires specifically cuda 10.0 :( don't try other versions it won't work
    - cuda 10.0 (you may need to uninstall all the nvidia driver first to do this (remove + purge), and maybe disable secure boot)
    - cudnn 7.6.5 please find the specific version that works with cuda 10.0. 
    Run time libraries are sufficient.

ALBERT requirements:
    - only works when the tensorflow version is 1.15, 2.0 does not have tensorflow.contrib 
    - tensorflow 1.15.0 is first available in pip3 19.0.0, upgrade your pip first...
    - and pip3 19.0 has a bug that prevents you from installing things. You may use this to solve it : hash -d pip
    - albert tensorflow is too new so what we depends on could not be installed with pip. Please clone it somewhere and add its address to your PYTHONPATH enviroment (export PYTHONPATH=address/to/your/albert/ALBERT/:$PYTHONPATH)
    - pip3 install sentencepiece
    - pip3 install scikit-learn==0.19.1

BERT requirements:
    - same as albert but with pip3 install bert-tensorflow
    - pathlib
    
https://github.com/snorkel-team/snorkel-tutorials/blob/master/getting_started/getting_started.ipynb

How to use this code :
1. python3 train.py (to generate and save the model)
2. python3 try.py (to use it)

How to use this code (ALBERT):
1. python3 cnn_train.py (to generate and save the model)
2. python3 api_cnn.py (to setup the server)
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


https://github.com/snorkel-team/snorkel-tutorials/blob/master/getting_started/getting_started.ipynb

How to use this code :
1. python3 train.py (to generate and save the model)
2. python3 try.py (to use it)
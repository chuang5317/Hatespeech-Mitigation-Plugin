import os
import pandas as pd
import preprocessing as pre
# Need more datasets
# All functions should return a Pandas DataFrame of spacy documents

# For plain text.
def get_sample_dataset_from_paintext(folder):
    ret = []
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        f = open(filepath, 'r')
        ret.append(pre.preprocess(f.read()))
        f.close()
    return pd.DataFrame(ret)

# For CSV. 
def get_sample_dataset(name):
    addr = "./dataset/" + name
    panda = pd.read_csv(addr)
    #TODO: insert preprocessing



#TODO: get data from tweet id

import dataset as ds
import labelingFunctions as lf 
from snorkel.labeling import LabelModel, PandasLFApplier

df_train = ds.get_sample_dataset_from_paintext("./dataset/white_supremacy_sampled_train")

# Define the set of labeling functions (LFs)
lfs = [lf.lf_neg_short, lf.lf_keyword_strong_swearing, lf.lf_spacy_adj_sexism]

# Apply the LFs to the unlabeled training data
applier = PandasLFApplier(lfs)
L_train = applier.apply(df_train)

# Train the label model and compute the training labels
# Cardinality was 2. Got : ValueError: L_train has cardinality 3, cardinality=2 passed in.
label_model = LabelModel(cardinality=3, verbose=True)
label_model.fit(L_train, n_epochs=500, log_freq=50, seed=123)
df_label = label_model.predict(L=L_train, tie_break_policy="abstain")



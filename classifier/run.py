import pickle
import tensorflow_datasets as tfds
# Assuming class_label is your ClassLabel object
(_, _), ds_info = tfds.load('stanford_dogs',
                                             split=['train', 'test'],
                                             shuffle_files=True,
                                             as_supervised=False,
                                             with_info=True,
                                             data_dir='data/tfds')

# Save the ClassLabel object to a file
with open('class_label.pkl', 'wb') as file:
    pickle.dump(ds_info, file)


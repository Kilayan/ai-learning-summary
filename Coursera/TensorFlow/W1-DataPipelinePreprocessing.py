import tensorflow as tf

# I. tf.data API
dataset = tf.data.TextLineDataset(filename)\
                 .skip(num_header_lines)\
                 .map(add_key)\
                 .map(decode_csv)\
                 .map(lambda feats, labels: preproc(feats), labels)
                 .filter(is_valid)\
                 .cache()
## feature columns
featcols = [
    tf.feature_column.numeric_column("sq_footage"),
    tf.feature_column.categorical_column_with_cocabulary_list("type", ["house", "apt"]) # two property types
]

### 1. fc.bucketized_column splits a numeric feature into categories based on numeric ranges
from tensorflow import feature_column as fc

### set up numeric ranges
NBUCKETS = 16
latbuckets = np.linespace(start=38.0, stop=42.0, num=NBUCKETS).tolist()
lonbuckets = np.linespace(start=-76.0, stop=-72.0, num=NBUCKETS).tolist()

## create bucketized columns for pickup longitude
fc_bucketized_plat = fc.bucketized_column(
    source_column= fc.numeric_column("pickup_latitude"),
    boundaries = latbuckets
)

fc_bucketized_plot = fc.bucketized_column(
    source_column= fc.numeric_column("pickup_longitude"),
    boundaries = lonbuckets
)
### 2. fc.embedding_column represents data as a low-dimensional, dense vector
### when there are sparse dataset
### lower dimensional, dense vector in which each cell contains a number, not just 0 or 1
fc_ploc = fc.embedding_column(categorical_column = fc_crossed_ploc, dimension=3)

### 3. fc.crossed_column enables a model to learn separate for combination of features (synthetic features)
fc_crossed_ploc = fc.crossed_column([fc_bucketized_plat, fc_bucketized_plot],
                                    hash_bucket_size = NBUCKETS * NBUCKETS)
            # crossed_column is backed by a hashed_column, so you must set the size of the hash bucket

### 4. Example
def features_and_label():
    # sq_fotage and type
    features = {"sq_footage": [1000, 2000, 3000, 1000, 2000, 3000],
                "type": ["house", "house", "house", "apt", "apt", "apt"]}
    # prices in thousands
    labels = [500, 1000, 1500, 700, 1300, 1900]
    return features, labels

def create_dataset(pattern, batch_size=1, mode=tf.estimator.ModeKeys.EVAL):
    dataset = tf.data.experimental.make_csv_dataset(
        pattern, batch_size, CSV_COLUMNS, DEFAULTS
    )
    dataset = dataset.map(features_and_label)
    if mode == tf.estimator.ModeKeys.TRAIN:
        dataset = dataset.shuffle(buffer_size = 1000).repeat()
    # take advantage of multi-threading; 1 = AUTOTUNE
    dataset = dataset.prefetch(1)
    return dataset

feature_columns = [...]
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
model = tf.keras.Sequential([
    feature_layer,
    layers.Dense(128, activation= 'relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='linear'),
])

model.fit()

# II. Keras preprocessing layers
## (1) Text: tf.keras.layers.TextVectorization turns raw strings into an encoded representation that can be read by an Embedding layer or Dense layer
## (2) Numerical:
### tf.keras.layers.Normalization() performs feature-wise normalization of input features
### tf.keras.layers.Discretization turns continuous numerical features into bucket data with discrete ranges
## (3) Categorical
### tf.keras.layers.CategoryEncoding turns integer categorical features into one-hot, multi-hot, or count dense representation
### tf.keras.layers.Hashing performs categorical feature hashing, also known as the hashing tricks
### tf.keras.layers.StringLookup turns string categorical values into an encoded representation that can be read by tan embedding layer or dense layer
### tf.keras.layers.IntegerLookup turns integer categorical values into an encoded representation that can be read by tan embedding layer or dense layer

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

def get_category_encoding_layer(name, dataset, dtype, max_token=None):
    if dtype == 'string':
        index = preprocessing.StringLookup(max_tokens = max_token)
    else:
        index = preprocessing.Integerlookup(max_token = max_token)

    # prepare a dataset that only yields our feature
    feature_ds = dataset.map(lambda x,y: x[name])
    # learn that set of possible values and assign them a fixed integer index
    index.adapt(feature_ds)
    # create a discretization for our integer indices
    encoder = preprocessing.CategoryEncoding(num_tokens=index.vocabulary_size())
    # apply one-hot encoding to our indices
    return lambda feature: encoder(index(feature))

def get_normalization_layer(name, dataset):
    # ensure that the mean of each feature is 0 and std is 1
    normalizer = preprocessing.Normalization(axis=None)
    feature_ds = dataset.map(lambda x, y: x[name])
    normalizer.adapt(feature_ds)

    return normalizer

# load data
(x_train, y_train), _ = keras.datasets.cifar10.load_data()
x_train = x_train.reshape((len(x_train), -1))
input_shape = x_train.shape[1:]
classes = 10

# create a normalization layer and set its internal state using the training data
normalizer = layers.Normalization()
normalizer.adapt(x_train)

# create a model that include the normalization layer
inputs = keras.Input(shape = input_shape)
x = normalizer(inputs)
outputs = layers.Dense(classes, activation="softmax")(x)
model = keras.Model(inputs, outputs)

# train the model
model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy")
model.fit(x_train, y_train)








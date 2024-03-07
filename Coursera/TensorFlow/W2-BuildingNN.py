from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([  # The Keras sequential model stacks layers on the top of each other
    Input(shape = (64,)) # the batch size is omitted. Here the model expects batches of vectors with 64 components
    Dense(units=32, activation= "relu", name="hidden1"),
    Dense(units=8, activation="relu", name="hidden2"),
    Dense(units=1, activation="linear", name="output"),
])

import tensorflow as tf
from tensorflow import keras
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# define your model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10, activation="softmax") # classification model, with 10 classes
    ])

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu", name="hidden1")  # a NN with one hidden layer
    tf.keras.layers.Dense(10, activation="softmax", name="output") # classification model, with 10 classes
    ])

# compile the model
def rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_pred - y_true)))

## optimizer: most common one is stochastic gradient descent.
## Adam has little memory required,computation efficient, diagonal rescaling, good for noisy,sparse gradient. large data, lots of parameters
## Adam and FTLR are used default
model.compile(optimizer="adam", loss="mse", metrics=[rmse, "mse"])

# train the model
from tensorflow.keras.callbacks import TensorBoard

## this is a trick so that we have control on the total number of examples the model trains on (NUM_TRAIN_EXAMPLES) AND
## total number of evaluation we want to have during training (NUM_EVALS).
## epoch: the complete pass on the entire dataset
## steps for epoch: the number of batch iterations before a training epoch is considered finished
## validation data, validation steps, batch size determines the number of samples in each mini batch.
#### https://medium.com/google-cloud/ml-design-pattern-3-virtual-epochs-f842296de730
steps_per_epoch = NUM_TRAIN_EXAMPLES // (TRAIN_BATCH_SIZE * NUM_EVALS)

history = model.fit(
    x = trainds,
    steps_per_epoch = steps_per_epoch,
    epochs = NUM_EVALS,
    validation_data = evalds,
    callbacks = [TensorBoard(LOGDIR)]
)

################### Example
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax") # classification model, with 10 classes
    ])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)

# prediction
## predictions: returns a Numpy array of predictions
## steps determines the total number of steps before declaring the prediction round finished.
predictions = model.predict(input_samples, steps=1)


#################### Serving models in the cloud
# SavedModel
OUTPUT_DIR = "./export/savedmodel"
shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
EXPORT_PATH = os.path.join(OUTPUT_DIR, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
tf.saved_model.save(model, EXPORT_PATH) # exports a model object to a SavedModel format

# AI platform service to serve trained model - shell script below to create model in AI platform
%%bash
MODEL_NAME = propertyprice
VERSINO_NAME = dnn
if [[ $(gcloud ai-platform models list --format='value(name)' | grep $MODEL_NAME) ]];
then
    echo "$MODEL_NAME already exists"
else
    echo "Creating $MODEL_NAME"
    gcloud ai-platform models create --regions=$REGION $MODEL_NAME
fi

## model version - create a model version in AI Platform
if [[ $(gcloud ai-platform models list --model $MODEL_NAME --format='value(name)' | grep $VERSION_NAME) ]];
then
    echo "Deleting already existing $MODEL_NAME:$VERSION_NAME ..."
    echo yes | gcloud ai-platform versions delete --model=$MODEL_NAME $VERSION_NAME
    echo "Please run this cell again if you don't see a Creating message ..."
    sleep 2
fi

# deploy SavedModel using gcloud ai-platform - shell script below
gloud ai-platform versions create \
    --model=$MODEL_NAME $VERSION_NAME \
    --framework=tensorflow \
    --python-version=3.5
    --runtime-version=2.1
    --origin=$EXPORT_PATH \
    --staging-bucket=gs://$BUCKET

# make predictions using gloud
input.json = {"sq_footage": 3140, "type": 'house'}
gloud ai-platform predict \
    --model propertyprice \
    --version dnn \
    --json-instances input.json


############ Functional API
# Models are created by specifying their inputs and outputs in a graph of layers
# example - autoencoder
encoder_input = keras.Input(shape=(28, 28, 1), name='img')
x = layers.Dense(16, activation='relu')(encoder_input)
x = layers.Dense(10, activation='relu')(x)
x = layers.Dense(5, activation='relu')(x)
encoder_output = layers.Dense(3, activation='relu')(x)
encoder = keras.Model(encoder_input, encoder_output, name = 'encoder')

x = layers.Dense(5, activation='relu')(encoder_output) # shared layers
x = layers.Dense(10, activation='relu')(x)
x = layers.Dense(16, activation='relu')(x)
decoder_output = layers.Dense(28, activation='linear')(x)

autoencoder = keras.Model(encoder_input, decoder_output, name='autoencoder')

# example of creating a wide and deep model in Keras
INPUT_COLS = [
    'pickup_longitude',
    'pickup_latitude',
    'dropoff_longitude',
    'dropoff_latitude',
    'passenger_count'
]
inputs = {colname:layers.Input(name=colname, shape=(), dtype='float32') for colname in INPUT_COLS}

# create deep columns
deep_columns = [
    # embeding_column to 'group' together
    fc.embedding_column(fc_crossed_pd_pair, 10),

    # numeric columns
    fc.numeric_column('pickup_latitude'),
    fc.numeric_column('pickup_longitude'),
    fc.numeric_column('dropoff_longitude'),
    fc.numeric_column('dropoff_latitude'),]

# create the deep part of model
deep_inputs = layers.DenseFeatures(deep_columns, name='deep_inputs')(inputs)
x = layers.Dense(30, activation='relu')(deep_inputs)
x = layers.Dense(20, activation='relu')(x)

deep_output = layers.Dense(10, activation='relu')(x)


############# subclassing model
import tensorflow as tf
class MyModel(tf.keras.Model):

    def _init_(self):   # example 1 constructor method
        super(myModel, self)._init_()
        self.dense1 = tf.keras.layers.Dense(4, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(5, activation=tf.nn.softmas)

    def _init_(self, num_classes=10): # example 2 constructor method for multi-classes
        super(myModel, self)._init_(name='my_model')
        # define your layers here
        self.dense_1 = layers.Dense(32, activation='relu')
        self.dense_2 = layers.Dense(num_classes, activation='softmax')

    def call(self, inputs): # call method
        x = self.dense1(inputs)
        return self.dense2(x)

# custom training lop
model = MyModel()

with tf.GradientTape() as tape:
    # this training argument is commonly used in batch normalization and dropout layers
    logits = model(images, training=True)
    loss_value = loss(logits, labels)
grads = tape.gradient(loss_value, model.variables)
optimizer.apply_gradients(zip(grads, model.variables))




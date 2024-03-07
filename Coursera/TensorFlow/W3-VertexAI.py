######### Distribute TensorFlow on Vertex AI
"""
Step1: use TensorFlow to create your Keras model
Step2: Package your trainer application
Step3: Configure and start a Vertex AI training job
"""

##### Step 1: model.py and task.py - create your Keras model

# model.py
def train_and_evaluate(hparams):
    # [...] obtain param values from hparam
    model = build_dnn_model(nbuckets, nnsize, lr)
    trainds = create_train_dataset(train_data_path, batch_size)
    evalds = create_eval_dataset(eval_data_path, batch_size)

    # [...] create the callbacks
    stpes_per_epoch = num_examples_to_train_on // (batch_size * num_evals)

    history = model.fit(
        trainds,
        validation_data = evalds,
        epochs = num_evals,
        stpes_per_epoch = max(1, stpes_per_epoch),
        verbose = 2, # 0 = silent, 1 = progress bar, 2 = one line per epoch
        callbacks = [checkpoint_cb, tensorboard_cb]
    )

    tf.saved_model.save(model, model_export_path)
    return history
# task.py
parser .add_argument(
    '--train_data_paths', required=True
)
parser.add_argument(
    '--train_steps', ...
)

##### Step 2: packaging
# test your code locally first -- shell script
EVAL_DATA_PATH = ./taxifare/tests/data/taxi-valid*
TRAIN_DATA_PATH = ./taxifare/tests/data/taxi-train*
OUTPUT_DIR = ./taxifare-model

test ${OUTPUT_DIR} && rm -rf ${OUTPUT_DIR}
export PYTHONGPATH = ${PYTHONPATH}:${PWD}/taxifare

python3 -m trainer.task \
    --eval_data_path $EVAL_DATA_PATH \
    --output_dir $OUTPUT_DIR \
    --train_data_path $TRAIN_DATA_PATH \
    --batch_size 5 \
    --num_examples_to_train_on 100\
    --num_evals 1 \
    --nbuckets 10 \
    --lr 0.001 \
    --nnsize "32 8"

# to make our code compatible with Vertext AI
"""
1. upload data to Google Cloud Storage
2. move code into a trainer Python package
3. Submit training job with gcloud to train on Vertex AI
"""

# bigquery extract data to the target folder
bq --location=US extract \
   --destination_format CSV  \
   --field_delimiter "," --noprint_header \
   taxifare.feateng_training_data \
   $OUTDIR/taxi-train-*.csv


# move code to trainer Python apckage
taxifare/trainer/__init__.py
taxifare/trainer/task.py
taxifare/trainer/model.py
taxifare/setup.py  ##

python ./setup.py sdist --formats=gztar # create resources
gsutil cp taxifare/dist/taxifare_trainer-0.1.tar.gz gs://${BUCKET}/taxifare/  #copy python package to GCS bucket

# submit a job with gcloud ai custom-jobs create
# using a pre-built container
gcloud ai custom-jobs create \
    --region=$REGION \
    --display-name=$JOB_NAME \
    --python-package-uris=$PYTHON_PACKAGE_URIS \  # PYTHON_PACKAGE_URIS = gs://${BUCKET}/taxifare/taxifare_trainer-0.1.tar.gz

    --worker-pool-spec=machine-type=$MACHINE_TYPE, \   # you can use multiple worker pool to do distributed training
    replica-count=$REPLICA_COUNT, \
    executor-image-uri=$PYTHON_PACKAGE_EXECUTOR_IMAGE_URI, \
    python-module=$PYTHON_MODULE

    --worker-pool-spec=machine-type=$SECOND_MACHINE_TYPE, \
    replica-count=$SECOND_REPLICA_COUNT, \
    executor-image-uri=$SECOND_PYTHON_PACKAGE_EXECUTOR_IMAGE_URI, \
    python-module=$SECOND_PYTHON_MODULE

    --args="$ARGS"
"""
ARGS="--eval_data_path=$EVAL_DATA_PATH, \
     --output_dir=$OUTDIR, \
     --train_data_path=$TRAIN_DATA_PATH \
     --batch_size=5 \
     --num_examples_to_train_on=100\
     --num_evals=1 \
     --nbuckets=10 \
     --lr=0.001 \
     --nnsize="32 8"
"""

# using a custom container
gcloud ai custom-jobs create \
    --region=$LOCATION \
    --display-name=$JOB_NAME \
    --worker-pool-spec=machine-type=$MACHINE_TYPE, \
    replica-count=$REPLICA_COUNT, \
    container-image-uri=$CUSTOM_CONTAINER_IMAGE_URI



#!/usr/bin/env python

# Description : Script to train a LSTM model using Keras.  

### Training data consists of a sequence of customer events and the trained model will predict the next sequence of the customer events.  In this particular example, sequence of the customer events is the names of the TV channels viewed.  From this, the trained model will predict the next sequence of channels the customer will view.  The predicted sequence can be used to predict whether a user will view a specific channel or an adverstisement or even rent a particiular movie etc.  This specific event of interest is represent by the word 'visit' in our data set.

### Summary of the algorithm : TODO

# Import the necessary libraries
import boto3
import argparse, os
import time
import sys
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from keras.layers import Input, LSTM, Dense
from keras import backend as K
from sklearn.model_selection import train_test_split


### Read ndarray from S3
def read_ndarray_from_s3(s3_prefix):
    s3 = boto3.resource('s3')
    local_file_downloaded = 'downloaded_encoder_data.npy'
    s3.Bucket("555360056434-sagemaker-us-east-1").download_file(s3_prefix, local_file_downloaded)
    downloaded_encoder_input_data = np.load(local_file_downloaded)
    return downloaded_encoder_input_data

if __name__ == '__main__':
    
    ##Parse arguments passed in
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batchsize', type=int, default=128)
    parser.add_argument('--modeldir', type=str, default='/opt/ml/model')
     
    args, _ = parser.parse_known_args()
    
    epoch_num = args.epochs
    batch_size_num = args.batchsize
    model_dir = args.modeldir
   
    print("epoch_num : ", epoch_num)
    print("batch_size_num : ", batch_size_num) 
    print("model_dir :  ", model_dir)
    
    ##Get the training data from S3
    encoder_input_data = read_ndarray_from_s3("train/train_encoder_input_data.npy")
    decoder_input_data = read_ndarray_from_s3("train/train_decoder_input_data.npy")
    decoder_target_data = read_ndarray_from_s3("train/train_decoder_target_data.npy")
    
    ##Build the LSTM network
    num_encoder_tokens = encoder_input_data.shape[2]
    num_decoder_tokens = decoder_input_data.shape[2]
    latent_dim = 256
    
    # Define an input sequence and process it.
    encoder_inputs = Input(shape=(None, num_encoder_tokens))
    encoder = LSTM(latent_dim, return_state=True)
    encoder_outputs, state_h, state_c = encoder(encoder_inputs)
    # We discard `encoder_outputs` and only keep the states.
    encoder_states = [state_h, state_c]
    
    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None, num_decoder_tokens))
    # We set up our decoder to return full output sequences,
    # and to return internal states as well. We don't use the
    # return states in the training model, but we will use them in inference.
    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                         initial_state=encoder_states)
    decoder_dense = Dense(num_decoder_tokens, activation='softmax')
    decoder_outputs = decoder_dense(decoder_outputs)
                                         
    # Define the model that will turn
    # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
    model = Model(inputs=[encoder_inputs, decoder_inputs], outputs=decoder_outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    model.summary()
    
    ##Model Name                            
    timestr = time.strftime("%Y%m%d-%H%M%S")
    model_name = 'customer_event_prediction_lstm_'+timestr
    model_checkpoint = '/tmp/' + model_name + '_ckpt.h5'
                                         
    
    checkpoint = ModelCheckpoint(model_checkpoint, monitor='val_acc', verbose=1,
                                                                      save_best_only=True, mode='min')
                                         
    model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
                                                   batch_size=batch_size_num,
                                                   epochs=epoch_num,
                                                   validation_split=0.2,
                                                   callbacks=[checkpoint], verbose=2)
                                                                               
    #Save Keras model for Tensorflow Serving
    sess = K.get_session()
                                         
    input_dict = {'encoder_input_data': model.input[0], 'decoder_input_data': model.input[1]}
    output_dict = {}
                                         
    for t in model.outputs :
        output_dict[t.name] = t

    tf.saved_model.simple_save(
                           sess,
                           os.path.join(model_dir, 'model/1'),
                           inputs=input_dict,
                           outputs=output_dict)


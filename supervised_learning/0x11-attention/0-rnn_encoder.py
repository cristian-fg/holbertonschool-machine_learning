#!/usr/bin/env python3
"""RNN Encoder"""
import tensorflow as tf


class RNNEncoder(tf.keras.layers.Layer):
    """Class RNN Encoder"""

    def __init__(self, vocab, embedding, units, batch):
        """
        -> vocab is an integer representing the size of
            the input vocabulary
        -> embedding is an integer representing the dimensionality
            of the embedding vector
        -> units is an integer representing the number of
            hidden units in the RNN cell
        -> batch is an integer representing the batch size
        """
        super(RNNEncoder, self).__init__()
        self.batch = batch
        self.units = units
        self.embedding = tf.keras.layers.Embedding(input_dim=vocab,
                                                   output_dim=embedding)

        self.gru = tf.keras.layers.GRU(units=self.units,
                                       recurrent_initializer="glorot_uniform",
                                       return_sequences=True,
                                       return_state=True)

    def initialize_hidden_state(self):
        """Initializes the hidden states for
            the RNN cell to a tensor of zeros"""
        init = tf.zeros(shape=(self.batch, self.units))

        return init

    def call(self, x, initial):
        """
        -> x is a tensor of shape (batch, input_seq_len) containing
            the input to the encoder layer as word indice
            within the vocabulary
        -> initial is a tensor of shape (batch, units)
            containing the initial hidden state

        -> Returns: outputs, hidden
            * outputs is a tensor of shape (batch, input_seq_len, units)
                containing the outputs of the encoder
            * hidden is a tensor of shape (batch, units) containing
                the last hidden state of the encoder
        """
        x = self.embedding(x)
        outputs, hidden = self.gru(x, initial_state=initial)

        return outputs, hidden

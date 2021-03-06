#!/usr/bin/env python3
"""Transformer Encoder Block"""
import tensorflow as tf
MultiHeadAttention = __import__('6-multihead_attention').MultiHeadAttention


class EncoderBlock(tf.keras.layers.Layer):
    """Class Encoder"""

    def __init__(self, dm, h, hidden, drop_rate=0.1):
        """
        -> dm - the dimensionality of the model
        -> h - the number of heads
        -> hidden - the number of hidden units in the fully connected layer
        -> drop_rate - the dropout rate
        """
        super(EncoderBlock, self).__init__()
        self.mha = MultiHeadAttention(dm, h)

        self.dense_hidden = tf.keras.layers.Dense(units=hidden,
                                                  activation="relu")
        self.dense_output = tf.keras.layers.Dense(dm)

        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = tf.keras.layers.Dropout(drop_rate)
        self.dropout2 = tf.keras.layers.Dropout(drop_rate)

    def call(self, x, training, mask=None):
        """
        -> x - a tensor of shape (batch, input_seq_len, dm)
            containing the input to the encoder block
        -> training - a boolean to determine if the model is training
        -> mask - the mask to be applied for multi head attention

        -> Returns: a tensor of shape (batch, input_seq_len, dm)
            containing the block’s output
        """
        attn_output, _ = self.mha(x, x, x, mask)
        attn_output = self.dropout1(attn_output, training=training)

        out1 = self.layernorm1(x + attn_output)
        forward_output = self.dense_hidden(out1)
        forward_output = self.dense_output(forward_output)

        forward_output = self.dropout2(forward_output, training=training)

        output = self.layernorm2(out1 + forward_output)

        return output

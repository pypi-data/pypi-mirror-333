import tensorflow as tf
from tensorflow import keras
from keras.layers import Layer


class flux(Layer):
    def __init__(self, activation=None, activation2=None, **kwargs):
        super(flux, self).__init__(**kwargs)
        self.activation = activation
        self.activation2 = activation2

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(1,),
            initializer=keras.initializers.Constant(1.0)
        )

        self.b = self.add_weight(
            shape=(1,),
            initializer=keras.initializers.Constant(0.0)
        )

    def call(self, inputs):
        if self.activation:
            if self.activation2:
                return keras.activations.get(self.activation2)((self.w * keras.activations.get(self.activation)(inputs)) + self.b)
            else:
                return keras.activations.get(self.activation)((self.w * keras.activations.get(self.activation)(inputs)) + self.b)
        else:
            return (self.w * inputs) + self.b

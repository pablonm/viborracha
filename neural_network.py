import numpy as np

class Neural_Network(object):
  def __init__(self, inputSize, hiddenLayerSize, outputSize, weights=[], bias=[]):
    self.inputSize = inputSize
    self.hiddenLayerSize = hiddenLayerSize
    self.outputSize = outputSize

    if len(weights) > 0:
      self.set_weights(weights)
    else:
      self.hiddenWeights = np.random.randn(inputSize, hiddenLayerSize)
      self.outputWeights = np.random.randn(hiddenLayerSize, outputSize)

    if len(bias) > 0:
      self.set_bias(bias)
    else:
      self.hiddenBias = np.random.randn(hiddenLayerSize)
      self.outputBias = np.random.randn(outputSize)

  def think(self, inputs):
    z = self._relu(np.dot(inputs, self.hiddenWeights) + self.hiddenBias)
    return np.argmax(self._softmax(np.dot(z, self.outputWeights) + self.outputBias))

  def _relu(self, x): 
    return np.maximum(0, x)

  def _softmax(self, x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

  def get_weights(self): 
    return np.concatenate((self.hiddenWeights.flatten(), self.outputWeights.flatten()))

  def set_weights(self, weights):
    self.hiddenWeights = weights[0:self.hiddenLayerSize * self.inputSize].reshape((self.inputSize, self.hiddenLayerSize))
    self.outputWeights = weights[self.hiddenLayerSize * self.inputSize:len(weights)].reshape((self.hiddenLayerSize, self.outputSize))

  def get_bias(self):
    return np.concatenate((self.hiddenBias, self.outputBias))

  def set_bias(self, bias):
    self.hiddenBias = bias[0:self.hiddenLayerSize]
    self.outputBias = bias[self.hiddenLayerSize: len(bias)]



# nn = Neural_Network(3, 5, 3)
# print(nn.think([1,0,1]))
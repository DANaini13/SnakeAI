import numpy as np

class Layer:
	def __init__(self, inputs_number, outputs_number):
		self.weights = np.random.rand(inputs_number+1, outputs_number) * 0.1 - 0.05
		self.last_diff = np.zeros(self.weights.shape)
		self.filter_func = lambda x: 1.0/(1 + np.exp(-x))
	
	def get_output(self, inputs):
		inputs = np.concatenate((inputs, np.array([1])), axis=0)
		self.inputs = inputs
		return [self.filter_func(i) for i in np.dot(inputs, self.weights)]
	
	def train(self, error, learning_rate, movement):
		weights_diff = []
		for single_error in error:
			weights_diff.append(learning_rate * single_error * self.inputs)
		self.weights += np.array(weights_diff).T + self.last_diff * movement
		self.last_diff = np.array(weights_diff).T

	def get_input_error(self, error):
		input_error = []
		for single_weights in self.weights:
			input_error.append(np.dot(error, single_weights))
		input_error = np.array(input_error)
		return self.inputs * (1 - self.inputs) * input_error


class Network:
	"""
	hidden_layers: a list that store the number of hidden units in each layer.
					example: [20] gonna create one hidden layer with 20 units,
							 [20, 50] gonna create two hidden layer with 20
							 and 50 units.
	input_nums: the lengh of each input as a list or one D numpy array
	outputs_nums: the number of units in the output layer.
	"""
	def __init__(self, hidden_layers, input_nums, outputs_nums):
		self.hidden_layers = []
		for x in range(len(hidden_layers) - 1):
			self.hidden_layers.append(Layer(hidden_layers[x], hidden_layers[x + 1])) 
		if len(hidden_layers) > 0:
			self.hidden_layers.append(Layer(hidden_layers[len(hidden_layers)-1], outputs_nums))
			self.input_layer = Layer(input_nums, hidden_layers[0])
		else:
			self.input_layer = Layer(input_nums, outputs_nums)

	"""
	this function gonna generate outputs for a specific input
	"""
	def get_output(self, inputs):
		if len(self.hidden_layers) <= 0:
			self.output = self.input_layer.get_output(inputs)
			return self.output
		else:
			self.output = self.input_layer.get_output(inputs)
			for layer in self.hidden_layers:
				self.output = layer.get_output(self.output)
			return self.output

	"""
	calling this function when the output result is not correct.
	"""
	def train(self, learning_rate, movement, filter_func, target):
		filtered_out = np.array([filter_func(i) for i in self.output])
		error = self.output * (1 - filtered_out) * (target - self.output)
		if len(self.hidden_layers) <= 0:
			self.input_layer.train(error, learning_rate, movement)
		else:
			hidden_num = len(self.hidden_layers)
			self.hidden_layers[hidden_num - 1].train(error, learning_rate, movement)
			input_error = self.hidden_layers[hidden_num - 1].get_input_error(error)
			for x in range(hidden_num - 1):
				index = hidden_num -x -2
				self.hidden_layers[index].train(input_error[:-1], learning_rate, movement)
				input_error = self.hidden_layers[index].get_input_error(input_error[:-1])
			self.input_layer.train(input_error[:-1], learning_rate, movement)



HurNetFX, an artificial neural network without backpropagation and which, compared to conventional neural networks, reduces the demand for parallel processing by eliminating iterative loops with backpropagation, concentrating parallelism in a single pseudoinverse step, resulting in greater training speed.

# HurNetFX

This code was designed, architected, and developed mathematically and algorithmically by Ben-Hur Varriano for Sapiens Technology®️ and aims to build neural networks algorithms capable of recognizing complex, linear, and nonlinear patterns in tensor structures such as vectors, matrices, and high-dimensionality numerical tensors. The HurNet network does not use backpropagation, which eliminates the need for weight adjustment loops and gradient descent calculations, making the network learn with a single iteration by simply relating the output data to the input data through polynomial terms and the Moore-Penrose pseudo-inverse. The mathematical structure of the HurNet network compared to conventional neural networks causes the demand for parallel processing to decrease as the training speed increases considerably. In this version, the HurNet network uses a feature expansion (FX) technique to enhance results with both simple layers and hidden layers.

**(This is a version of the HurNet network adapted to work with high-dimensionality numerical tensors)**

## Installation

Before installing the main package, it is necessary to install the numpy package as a dependency.

```bash
pip install numpy
```

Or install the recommended version:

```bash
pip install numpy==1.25.2
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install HurNetFX.

```bash
pip install hurnet-fx-tensor
```

## Usage
Basic usage example:
```python
# import MultiLayerHurNetFX main class from hurnet_fx_tensor module
from hurnet_fx_tensor import MultiLayerHurNetFX
# instantiate the MultiLayerHurNetFX class inside the hurnet_neural_network object
hurnet_neural_network = MultiLayerHurNetFX()
# training samples with input and output examples for xor operator logic
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
# calling the training method through the class object
# the input_layer parameter receives a vector, matrix or tensor with the input examples
# the output_layer parameter receives a vector, matrix or tensor with the output examples
# the vectors, matrices or tensors must have only numeric elements
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)
# calling the prediction method through the class object
# input_layer receives input examples with the same dimensionality as the training input_layer and tries to predict the output data
# decimal_places takes an integer with the desired number of decimal places in the numeric elements of the output
test_outputs = hurnet_neural_network.predict(input_layer=inputs, decimal_places=0)
# display the prediction result stored in the output variable
print(test_outputs)
```

Note that the result is returned quickly and with 100% accuracy.

```bash
[[0], [1], [1], [0]]
```
Unlike the example with the XOR operator, which is a classification case, here we will use a regression case.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# samples for training with a pattern that sums the input vectors to obtain the output vectors
inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3], [7], [11], [15]]
# training the artificial neural network with the data for pattern learning
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)
# input samples for the network to predict an output with the pattern learned in training using different data
test_inputs = [[2, 3], [4, 5], [6, 7], [8, 9]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[5.0], [9.0], [13.0], [17.0]]
```
Note below that it is also possible to work with one-dimensional vectors.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# training sample with data distributed in one-dimensional vectors
inputs = [1, 2, 3, 4, 5]
outputs = [2, 4, 6, 8, 10]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)
# the network tries to predict double each input element by applying the pattern learned in training
test_inputs = [6, 7, 8, 9, 10] # always use data with the same dimensionality as the training input sample
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[12.0, 14.0, 16.0, 18.0, 20.0]
```
Here we have an example with multiple elements in the input values and a single element for each output, combining a matrix of vectors with a vector of scalars.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# training to recognize the pattern of double multiplied by ten
inputs = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
outputs = [30, 50, 70, 90, 110]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[2, 5], [7, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[70.0, 80.0]
```
In this example, we use scalar values in an input vector to obtain vectors in an output matrix.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
"""
with this input pattern, the network should learn that for each scalar,
a vector must be created with twice the value in the first element and
twice the value multiplied by ten in the second element
"""
inputs = [2, 4, 6, 8]
outputs = [[4, 40], [8, 80], [12, 120], [16, 160]]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [1, 3, 7, 9]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[2.0, 20.0], [6.0, 60.0], [14.0, 140.0], [18.0, 180.0]]
```
Check out some examples using high dimensionality below.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# example of the xor operator adapted for high dimensionality
inputs = [[[0], [0]], [[0], [1]], [[1], [0]], [[1], [1]]]
outputs = [[0], [1], [1], [0]]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = inputs
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
[[0], [1], [1], [0]]
```
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# example of the xor operator adapted for high dimensionality
inputs = [[[0], [0]], [[0], [1]], [[1], [0]], [[1], [1]]]
outputs = [[[0]], [[1]], [[1]], [[0]]]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = inputs
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
[[[0]], [[1]], [[1]], [[0]]]
```
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# example of the xor operator adapted for high dimensionality
inputs = [[[[[0]], [[0]]]], [[[[0]], [[1]]]], [[[[1]], [[0]]]], [[[[1]], [[1]]]]]
outputs = [[[[0]]], [[[1]]], [[[1]]], [[[0]]]]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = inputs
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
[[[[0]]], [[[1]]], [[[1]]], [[[0]]]]
```
In the following example we are using multiple elements for each input and output.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# the pattern that the network should abstract is just to multiply each element of the input matrix vectors by two
inputs = [[1, 2, 3], [4, 5, 6]]
outputs = [[2, 4, 6], [8, 10, 12]]
"""
the parameter named "interaction" in the training method adds an interaction calculation
using the product of the elements of each input distributed in a matrix of vectors.  
this calculation can increase accuracy in more complex patterns when set to True,
but it may also decrease it in very simple patterns where the input and output have more than one dimension,
for this reason we set it to False
"""
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, interaction=False)

test_inputs = [[7, 8, 9]] # the dimensionality of the prediction continues to match that of the training, even for a single prediction
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[14.0, 16.0, 18.0]]
```
With the "bias" parameter it is possible to add a bias to the neural network training.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
"""
the "bias" parameter adds an arbitrary term to the network's weights,
causing the values to increase proportionally when adding positive values
or decrease proportionally when adding negative values.
"""
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, bias=0.001)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs) # result with positive bias
```
```bash
[[0.001], [1.002], [1.002], [0.004]]
```
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
"""
the "bias" parameter adds an arbitrary term to the network's weights,
causing the values to increase proportionally when adding positive values
or decrease proportionally when adding negative values.
"""
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, bias=-0.001)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs) # result with negative bias
```
```bash
[[-0.001], [0.998], [0.998], [-0.004]]
```
You can use the "activation_function" parameter to assign a function that will apply a transformation to the training data in order to increase the network's ability in learn complex patterns and reduce the possibility of overfitting. This function is especially useful for non-linear patterns, as it adds non-linearity to the model.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# learning the logic of the or operator
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [1]]
"""
the activation_function name parameter receives a string with the name of the activation function,
certain activation functions may increase the network's ability to abstract certain more complex patterns,
but tests must be done because in some cases the pattern abstraction capacity may decrease
"""
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, activation_function='relu')

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
[[0], [1], [1], [1]]
```
Check out all the configuration possibilities for the training method below.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# the pattern sums the inputs in the first element, multiplies the sum by ten in the second, and repeats the first input element in the third output element
inputs = [[1, 2], [3, 4], [5, 6], [7, 8]]
outputs = [[3, 30, 1], [7, 70, 3], [11, 110, 5], [15, 150, 7]]

"""
the activation_function parameter must receive a string with one of the following values:
(`linear`, `sigmoid`, `tanh`, `relu`, `leaky_relu`, `softmax`, `softplus`, `elu`, `silu`, `swish`, `gelu`, `selu`, `mish`, `hard_sigmoid`)
"""
# below are all the training parameters with their default values
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, interaction=True, activation_function='linear', bias=0)

test_inputs = [[2, 3], [4, 5], [6, 7]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[5.0, 50.0, 2.0], [9.0, 90.0, 4.0], [13.0, 130.0, 6.0]]
```
To force the network to learn more sensitive and/or complex patterns, you can use the "addHiddenLayer" method which adds hidden layers to the network before calling training.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]

# note that without hidden layers the network will return negative numbers close to zero
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[-0.0], [1.0], [1.0], [-0.0]]
```
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]

# with hidden layers we will have exactly the numbers zero and one without rounding
# the "num_neurons" parameter receives an integer with a value equivalent to the number of neurons in the hidden layer added
hurnet_neural_network.addHiddenLayer(num_neurons=4)
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)

test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[0.0], [1.0], [1.0], [0.0]]
```
Use the "saveModel" method to save a pre-trained model to the path defined in the "model_path" parameter string.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()

inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]

hurnet_neural_network.addHiddenLayer(num_neurons=4)
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs)
# saves a pre-trained model in the local directory with the name `my_model.hurnet`.  
# the `.hurnet` extension is optional when setting the model name.  
# if no name is set, the model will be saved in the current directory with the name `model.hurnet`.  
# if you prefer, you can also specify a directory for saving by providing the path before the name.  
# the "saveModel" function will return `True` if the save was successful, or `False` otherwise.
hurnet_neural_network.saveModel(model_path='my_model')
```
Use the "loadModel" method to load a pre-trained model directly from the path defined in the "model_path" parameter string.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# loads a pre-trained model contained in the current directory named my_model.hurnet
# the `.hurnet` extension is optional when setting the model name.  
# if no name is specified the function will look for a model in the current directory with the name `model.hurnet`
# if you prefer, you can also specify a directory for loading by providing the path before the name.  
# the "loadModel" function will return `True` if the load was successful, or `False` otherwise.
hurnet_neural_network.loadModel(model_path='my_model')
# with a pre-trained model loaded, training is no longer necessary
# direct prediction without prior training becomes much faster
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs)
print(test_outputs)
```
```bash
[[0.0], [1.0], [1.0], [0.0]]
```


Check below a comparative example between the training and inference time spent running the HurNet network and the Pytorch network commonly used in building language models.
```python
# test run on a macbook pro m3 max with 48gb vram
from hurnet_fx_tensor import measure_execution_time, tensor_similarity_percentage
"""
training pattern
first output element: sums the first two input elements
second output element: multiplies the sum of the first two input elements by ten
third output element: subtracts one from the third input element
"""
# samples for training
input_layer = [[1, 2, 3], [3, 4, 5], [5, 6, 7]]
output_layer = [[3, 30, 2], [7, 70, 4], [11, 110, 6]]
# samples for prediction/test
input_layer_for_testing = [[2, 3, 4], [4, 5, 6]]
expected_output = [[5, 50, 3], [9, 90, 5]]

def test_with_pytorch(): # !pip install torch
    print('###################### ALGORITHM: PYTORCH ######################')
    import torch
    import torch.nn as nn
    import torch.optim as optim
    torch.manual_seed(42)
    inputs = torch.tensor(input_layer, dtype=torch.float32)
    outputs = torch.tensor(output_layer, dtype=torch.float32)
    class NeuralNet(nn.Module):
        def __init__(self):
            super(NeuralNet, self).__init__()
            self.fc1 = nn.Linear(3, 10)
            self.fc2 = nn.Linear(10, 10)
            self.fc3 = nn.Linear(10, 3)
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.fc3(x)
            return x
    model = NeuralNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    # artificial neural network training
    epochs = 9000 # minimum value found to obtain the best result
    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, outputs)
        loss.backward()
        optimizer.step()
    test_inputs = torch.tensor(input_layer_for_testing, dtype=torch.float32)
    # artificial neural network inference
    test_outputs = model(test_inputs).detach().numpy().astype(int).tolist()
    similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
    print(test_outputs)
    print(f'similarity between the result and the expectation: {similarity:.10f}')

# test with the hurnet algorithm, note that it is not necessary to apply deep learning
def test_with_hurnet_fx_tensor(): # !pip install hurnet-fx
    print('###################### ALGORITHM: HURNET  ######################')
    from hurnet_fx_tensor import MultiLayerHurNetFX
    hurnet_neural_network = MultiLayerHurNetFX()
    # artificial neural network training
    hurnet_neural_network.train(input_layer=input_layer, output_layer=output_layer)
    # artificial neural network inference
    test_outputs = hurnet_neural_network.predict(input_layer=input_layer_for_testing, decimal_places=0)
    similarity = tensor_similarity_percentage(obtained_output=test_outputs, expected_output=expected_output)
    print(test_outputs)
    print(f'similarity between the result and the expectation: {similarity:.10f}')

# calculation for measurement of training and inference results
pytorch_time = measure_execution_time(function=test_with_pytorch, display_message=True)
hurnet_fx_tensor_time = measure_execution_time(function=test_with_hurnet_fx_tensor, display_message=True)
difference = int(round(max((hurnet_fx_tensor_time, pytorch_time))/min((hurnet_fx_tensor_time, pytorch_time))))
description = f'''
Note that the HurNet network is {difference} times faster than the Pytorch network ({pytorch_time} divided by {hurnet_fx_tensor_time}).
Also remember that this time difference can increase dramatically as more complexity is added to the network.
'''
print(description)
```
```bash
###################### ALGORITHM: PYTORCH ######################
[[5, 50, 3], [9, 90, 5]]
similarity between the result and the expectation: 1.0000000000
Execution time: 1.7469611659 seconds.
###################### ALGORITHM: HURNET  ######################
[[5, 50, 3], [9, 90, 5]]
similarity between the result and the expectation: 1.0000000000
Execution time: 0.0001855418 seconds.

Note that the HurNet network is 9415 times faster than the Pytorch network (1.7469611659180373 divided by 0.0001855418086051941).
Also remember that this time difference can increase dramatically as more complexity is added to the network.

```

## Classes
### SingleLayerHurNetFX: Used to build simple artificial neural networks that do not contain hidden layers.
### MultiLayerHurNetFX: Used to build complex artificial neural networks that contain hidden layers.

## Methods
### addHiddenLayer (function return type: bool): Returns True if the hidden layer is added successfully, or False otherwise. Only available for MultiLayerHurNetFX class.
Parameters
| Name                | Description                                                                                       | Type | Default Value     |
|---------------------|---------------------------------------------------------------------------------------------------|------|-------------------|
| num_neurons         | number of neurons for the layer being added                                                       | int  | 1                 |

### train (function return type: bool): Returns True if training is successful or False otherwise.
Parameters
| Name                | Description                                                                                       | Type  | Default Value    |
|---------------------|---------------------------------------------------------------------------------------------------|-------|------------------|
| input_layer         | tensor with input samples                                                                         | list  | []               |
| output_layer        | tensor with output samples                                                                        | list  | []               |
| interaction         | True to enable interactive computation for subtle pattern abstraction, or False to disable        | bool  | True             |
| activation_function | string with the name of the activation function to be used for non-linear data abstraction        | str   | 'linear'         |
| bias                | positive or negative floating number used to add bias to the network                              | float | 0                |

### saveModel (function return type: bool): Returns True if the training save is successful or False otherwise.
Parameters
| Name                | Description                                                                                       | Type | Default Value     |
|---------------------|---------------------------------------------------------------------------------------------------|------|-------------------|
| model_path          | path and name of the file to be generated, for the saved training model                           | str  | ''                |

### loadModel (function return type: bool): Returns True if the training load is successful or False otherwise.
Parameters
| Name                | Description                                                                                       | Type | Default Value     |
|---------------------|---------------------------------------------------------------------------------------------------|------|-------------------|
| model_path          | path and name of the file to be loaded, for the pre-trained model to be used                      | str  | ''                |

### predict (function return type: list): Returns a multidimensional tensor with the numerical results of the inference.
Parameters
| Name                | Description                                                                                       | Type | Default Value     |
|---------------------|---------------------------------------------------------------------------------------------------|------|-------------------|
| input_layer         | input tensor with samples for prediction                                                          | list | []                |
| decimal_places      | integer with the number of decimal places for the elements of the prediction output tensor        | int  | 8                 |

## Functions
### measure_execution_time: (function return type: float): Returns the time spent in seconds executing a given function.
Parameters
| Name                | Description                                                                                       | Type     | Default Value |
|---------------------|---------------------------------------------------------------------------------------------------|----------|---------------|
| function            | name of the function to be performed and measured                                                 | function | print         |
| display_message     | if True displays a message with the time elapsed in seconds, if False does not display            | bool     | True          |

### tensor_similarity_percentage: (function return type: float): Returns a percentage number between 0 and 1 with the degree of similarity between two tensors.
Parameters
| Name                | Description                                                                                       | Type     | Default Value |
|---------------------|---------------------------------------------------------------------------------------------------|----------|---------------|
| obtained_output     | tensor with the prediction response                                                               | list     | []            |
| expected_output     | tensor with the expected data as response                                                         | list     | []            |

Check out an example below with all the features available in the current package.
```python
from hurnet_fx_tensor import MultiLayerHurNetFX
hurnet_neural_network = MultiLayerHurNetFX()
# deep learning model training
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_neural_network.addHiddenLayer(num_neurons=4) # only available for the "MultiLayerHurNetFX" class
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, interaction=True, activation_function='relu', bias=0)
save = hurnet_neural_network.saveModel(model_path='./my_model.hurnet')
if save: print('Model SAVED SUCCESSFULLY!!')
else: print('ERROR saving model.')
# deep learning model loading
load = hurnet_neural_network.loadModel(model_path='./my_model.hurnet')
if load: print('Model LOADED SUCCESSFULLY!!')
else: print('ERROR loading model.')
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
Model SAVED SUCCESSFULLY!!
Model LOADED SUCCESSFULLY!!
[[0], [1], [1], [0]]
```
Or:
```python
from hurnet_fx_tensor import SingleLayerHurNetFX
hurnet_neural_network = SingleLayerHurNetFX()
# deep learning model training
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [[0], [1], [1], [0]]
hurnet_neural_network.train(input_layer=inputs, output_layer=outputs, interaction=True, activation_function='relu', bias=0)
save = hurnet_neural_network.saveModel(model_path='./my_model.hurnet')
if save: print('Model SAVED SUCCESSFULLY!!')
else: print('ERROR saving model.')
# deep learning model loading
load = hurnet_neural_network.loadModel(model_path='./my_model.hurnet')
if load: print('Model LOADED SUCCESSFULLY!!')
else: print('ERROR loading model.')
test_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
test_outputs = hurnet_neural_network.predict(input_layer=test_inputs, decimal_places=0)
print(test_outputs)
```
```bash
Model SAVED SUCCESSFULLY!!
Model LOADED SUCCESSFULLY!!
[[0], [1], [1], [0]]
```

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.

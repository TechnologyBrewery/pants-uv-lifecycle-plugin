import numpy as np 
from src.example_project.generate_array import generate_array

def test_generate_array():
    numpy_array = generate_array()
    numpy_array_type = type(numpy_array)
    assert isinstance(numpy_array, np.ndarray), f'The numpy_array is of type {numpy_array_type}, but it was expected to be of type numpy.ndarray.'
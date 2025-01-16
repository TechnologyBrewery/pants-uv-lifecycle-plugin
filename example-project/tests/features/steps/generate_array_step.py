from behave import when, then
import numpy as np 
from src.example_project.generate_array import generate_array

@when("the generate numpy array functionality is executed")
def step_impl(context):
    context.numpy_array = generate_array()

@then("a numpy array is generated")
def step_impl(context):
    numpy_array_type = type(context.numpy_array)
    assert isinstance(context.numpy_array, np.ndarray), f'The context.numpy_array is of type {numpy_array_type}, but it was expected to be of type numpy.ndarray.'
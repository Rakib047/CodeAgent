# data_processing.py

import file_handler
import math_ops

def load_data():
    return file_handler.read_file("data.txt")

def process_data(data):
    processed = []
    for num in data:
        processed.append(math_ops.square(num))
    return processed



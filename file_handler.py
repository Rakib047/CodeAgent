# file_handler.py

def read_file(filename):
    numbers = []
    with open(filename, 'r') as f:
        for line in f:
            numbers.append(int(line.strip()))
    return numbers



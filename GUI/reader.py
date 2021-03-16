"""
    Handles importing CSV file of output and formatting for display
"""
import json
import os
import pandas


def read_csv(input_file):
    ds = pandas.read_csv(input_file, sep=',', header=None)

    return ds


def read_json(path='output.json'):
    if os.path.exists(path):
        file = path
    else:
        print("ERROR: File not found")
        return None

    with open(file) as f:
        data = json.load(f)

    eqs = data['equations']
    paths = data['paths']

    return eqs, paths


if __name__ == '__main__':
    print(read_json())

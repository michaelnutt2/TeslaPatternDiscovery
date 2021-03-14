"""
    Handles importing CSV file of output and formatting for display
"""
import json
import os
import pandas


def read_csv():
    if os.path.exists('output.csv'):
        file = 'output.csv'
    else:
        print("Error: File not found")
        return None

    df = pandas.read_csv(file)
    print(df)
    df_list = df.columns.to_list()
    df_dict = {'original': df_list[0]}

    return df_dict


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

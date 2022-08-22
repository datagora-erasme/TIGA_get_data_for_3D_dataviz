"""
    This script process the output data of main.py in order to be plotted by the old DataViz
    Carto 3D entreprises Lyon, using deck.gl and D3.js
"""
import time
import pandas as pd
import numpy as np

def process_data():
    """
    Opens the 'output.csv' output data
    and filters data in order to fit the dataviz
    :return:
    saves a file DataProcessed.csv
    """

    input_df = pd.read_csv('output.csv')
    input_df['secteur'] = 1
    input_df['capitaux'] = np.random.randint(101, size=len(input_df))
    input_df.to_csv("data/data_processed.csv", index=False)

if __name__ == '__main__':
    t0 = time.time()
    process_data()
    t1 = time.time()

    print("Temps écoulé : ", t1-t0)

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import os

def generate_model_data():
    excel_directory = 'models/excel_results'

    dataframes = []
    for excel_file in os.listdir(excel_directory):
        data = pd.read_excel(f'{excel_directory}/{excel_file}')
        data['MRR'] = data['MRR'].round(4)
        dataframes.append(data)

    data = pd.concat(dataframes, ignore_index=True)

    new_names = {'cloneSize': 'minCloneSize', 'T1Boost': 't1Boost', 'T2Boost': 't2Boost'}
    data.rename(columns=new_names, inplace=True)

    siamese_parameters = [
        "ngramSize",
        "minCloneSize",
        "QRPercentileNorm",
        "QRPercentileT2",
        "QRPercentileT1",
        "QRPercentileOrig",
        "normBoost",
        "t2Boost",
        "t1Boost",
        "origBoost",
        "simThreshold"
    ]

    X = data[siamese_parameters]
    y_mrr = data['MRR']
    y_mop = data['MOP']


    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, siamese_parameters)
        ])
    
    return X, y_mrr, y_mop, preprocessor

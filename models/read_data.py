import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import os

excel_directory = 'excel_results'

dataframes = []
for excel_file in os.listdir(excel_directory):
    data = pd.read_excel(f'{excel_directory}/{excel_file}')
    data['MRR'] = data['MRR'].round(4)
    dataframes.append(data)

data = pd.concat(dataframes, ignore_index=True)

drop_columns = ['execution',
                'filename',
                "time",
                "WA(MRR,MOP) - (0.5,0.5)",
                "WA(MRR,MOP) - (0.7,0.3)",
                "WA(MRR,MOP) - (0.3,0.7)"]

siamese_parameters = [
    "ngramSize",
    "cloneSize",
    "QRPercentileNorm",
    "QRPercentileT2",
    "QRPercentileT1",
    "QRPercentileOrig",
    "normBoost",
    "T2Boost",
    "T1Boost",
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

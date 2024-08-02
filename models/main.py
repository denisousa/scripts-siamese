import pandas as pd
from linear_regression_algorithm import get_linear_regression_pipeline
from random_forest_regressor_algorithm import get_forest_regressor_pipeline
from svm_algorithm import get_svm_pipeline
from xgboost_algorithm import get_xgboost_pipeline
from MLPRegressor_algorithm import get_nn_regressor_pipeline
from read_data import X, y_mrr, y_mop, preprocessor

def predict(metric, pipeline, new_parameters):
    new_parameters_df = pd.DataFrame([new_parameters])
    result = pipeline.predict(new_parameters_df)
    
    print(f'Predicted {metric}: {result[0].round(4)}')

linear_regression_pipeline_mrr, _ = get_linear_regression_pipeline('mrr', X, y_mrr, preprocessor)
linear_regression_pipeline_mop, _ = get_linear_regression_pipeline('mop', X, y_mop, preprocessor)
print()
forest_regressor_pipeline_mrr, _ = get_forest_regressor_pipeline('mrr', X, y_mrr, preprocessor)
forest_regressor_pipeline_mop, _ = get_forest_regressor_pipeline('mop', X, y_mop, preprocessor)
print()
svm_pipeline_mrr, _ = get_svm_pipeline('mrr', X, y_mrr, preprocessor)
svm_pipeline_mop, _ = get_svm_pipeline('mop', X, y_mop, preprocessor)
print()
xgboost_pipeline_mrr, _ = get_xgboost_pipeline('mrr', X, y_mrr, preprocessor)
xgboost_pipeline_mop, _ = get_xgboost_pipeline('mop', X, y_mop, preprocessor)
print()
nn_regressor_pipeline_mrr, _ = get_nn_regressor_pipeline('mrr', X, y_mrr, preprocessor)
nn_regressor_pipeline_mop, _ = get_nn_regressor_pipeline('mop', X, y_mop, preprocessor)


new_parameters = {
    'ngramSize': 10,
    'minCloneSize': 13,
    'QRPercentileNorm': 10,
    'QRPercentileT2': 20,
    'QRPercentileT1': 18,
    'QRPercentileOrig': 10,
    'normBoost': 14,
    'T2Boost': 6,
    'T1Boost': 10,
    'origBoost': 2,
    'simThreshold': '20%,40%,60%,70%'
}

print(f'\n\nPredict: {new_parameters}\n')
print('MRR:0,5892', 'MOP: 0,1722')

predict('mrr', linear_regression_pipeline_mrr, new_parameters)
predict('mop', linear_regression_pipeline_mop, new_parameters)
print()
predict('mrr', forest_regressor_pipeline_mrr, new_parameters)
predict('mop', forest_regressor_pipeline_mop, new_parameters)
print()
predict('mrr', svm_pipeline_mrr, new_parameters)
predict('mop', svm_pipeline_mop, new_parameters)
print()
predict('mrr', xgboost_pipeline_mrr, new_parameters)
predict('mop', xgboost_pipeline_mop, new_parameters)
print()
predict('mrr', nn_regressor_pipeline_mrr, new_parameters)
predict('mop', nn_regressor_pipeline_mop, new_parameters)


'''
Os menores valores de MSE foram:
MRR:
Random Forest: 0.0013046664820347013

MOP:
XBoost: 0.00010575680930984704
'''
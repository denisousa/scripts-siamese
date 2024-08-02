from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from models.calculate_time import execution_time
from sklearn.metrics import mean_squared_error

@execution_time
def get_xgboost_pipeline(metric, X, y, preprocessor):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                            ('model', XGBRegressor(n_estimators=100, random_state=42))])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f'XBoost - {metric}')
    print(f'Mean Squared Error: {mse}')

    return pipeline, mse


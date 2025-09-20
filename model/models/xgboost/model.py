from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib, os

class XGBoostModel:
    def __init__(self, params=None):
        if params is None:
            params = {
                'objective': 'binary:logistic',
                'eval_metric': 'logloss',
                'use_label_encoder': False,
                'learning_rate': 0.1,
                'max_depth': 6,
                'n_estimators': 100
            }
        self.params = params

        # Define preprocessing for numerical and categorical features
        preprocessor = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        # Define Final Model Pipeline
        self.model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', XGBClassifier(**self.params))
        ])

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    
    def search_cv(self, params, X_train, y_train):
        grid_search = GridSearchCV(self.model, params, cv=5, scoring='recall_weighted')
        grid_search.fit(X_train, y_train)
        return grid_search.best_estimator_
    
    def save_model(self, path):
        joblib.dump(self.model, os.path.join(path, 'xgboost_model.pkl'))
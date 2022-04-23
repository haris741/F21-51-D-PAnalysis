import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import joblib
from keras import backend as K 
import gc
class Model:
    def __init__(self):
        self.models = []


    def addModel(self, filename):
        self.models.append(filename)

    def predict(self, data):
        prediction=[]
        for model_name in self.models:
            model=joblib.load(model_name)
            number = preprocessing.LabelEncoder()
            data['cleaned_content'] = number.fit_transform(data.content)
            prediction.append( model.predict(data['cleaned_content'].values.reshape(-1, 1), ))
            del model
            K.clear_session()
            _=gc.collect()

        prediction= pd.DataFrame(prediction)
        prediction=prediction.apply(pd.Series.value_counts)
        return prediction

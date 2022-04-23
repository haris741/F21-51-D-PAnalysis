import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import joblib
from keras import backend as K 
import gc
# class to handle models and prediction
class Model:

    # initialise and empty list in the class to handle the addition of the models
    def __init__(self):
        self.models = []


    # this would add the model using filename
    def addModel(self, filename):
        self.models.append(filename)

    # predict the output using the list of models
    def predict(self, data):
        prediction=[]
        for model_name in self.models:
            # load the model
            model=joblib.load(model_name)
            number = preprocessing.LabelEncoder()

            # fit the data accordingly
            data['cleaned_content'] = number.fit_transform(data.content)

            # predict and append it to the prediction list
            prediction.append( model.predict(data['cleaned_content'].values.reshape(-1, 1), ))
            del model

            # clear the main memory
            K.clear_session()
            _=gc.collect()

        # converting the prediction list to dataframe
        prediction= pd.DataFrame(prediction)

        # count the values for prediction of each model added
        prediction=prediction.apply(pd.Series.value_counts)
        return prediction

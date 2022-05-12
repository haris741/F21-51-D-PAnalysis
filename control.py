# This python program would run and check if there's a query that needs to be processed
# each query has a status
# if the status of query says that it needs to be started, the program would fetch the data related to that query and start processing
# before processing, the program would change the status of query to working so no other node would try to access that
# this prevents two nodes working on the same query
# if an error occurs, it handles the exception and change the status of the query to error and move on to the next query if available
# if no query is available, it would sleep for a while and then again look if any query is ready to start

# in case of error, it would not stop, rather start looking for another query

# database class handles the opening and closing of the connection
# a connection is closed as soon as it is no longer required so there can be multiple nodes accessing to the database without getting deadlock



from DatabaseConnection import DatabaseConnection
import time
from scraper import Scraper
import pandas as pd
from collections import Counter
from models import Model
# import libraries
from sklearn.metrics import f1_score,classification_report
from utils import get_logger,preprocess_text
import pandas as pd
import unittest
import logging
import warnings
import joblib
import os
warnings.filterwarnings('ignore')
class Predicting():
    def __init__(self):
        self.queries = []
        self.db = DatabaseConnection()

    #model_prediction

    #it takes a username as argument, fetch tweets from the database
    # call the model class
    # record predictions and insert back into database
    def make_prediction(self, username):

        # create connection
        cursor, db = self.db.getFreshConnection()

        # get tweets from the database
        cursor.execute("select * from tweets WHERE username=%s", [username])
        data= cursor.fetchall()
        self.db.close_connection(cursor, db)

        # store it in pandas
        df= pd.DataFrame(data)

        #assigning columns to the dataframe
        df.columns =['id', 'tweetID', 'content', 'tweetTS', 'username', 'cleaned_content']

        # To have the output dataframe, we must have the id of the dataframe to insert into database
        ids= df['id'].values.reshape(-1,1)
        # create a model object
        model = Model()
        model.addModel("static/models/humour_en/saved_model/random_forest.joblib")


        # analysing humour prediction first 
        humour_df=model.predict(df)
        humour_df=humour_df.transpose()
        humour_df=humour_df.rename({0: 'Neutral', 1: 'Funny', 2: 'Neutral'}, axis='columns')
        output = pd.DataFrame()
        output["humour"] = humour_df.idxmax(axis=1)
        output["tweet_id"]= ids


        # hatespeech offensive prediction
        vectorizer = joblib.load(os.path.join('static/models/hatespeech_offensive/saved_model','vectorizer.pkl'))

        model = joblib.load(os.path.join('static/models/hatespeech_offensive/saved_model','model.pkl'))
        X_test = vectorizer.transform(df['content'].map(preprocess_text))
        hatespeech_offensive = []
        hatespeech_offensive.append( model.predict(X_test))
        hatespeech_offensive= pd.DataFrame(hatespeech_offensive)
        hatespeech_offensive=hatespeech_offensive.apply(pd.Series.value_counts)
        hatespeech_offensive = hatespeech_offensive.transpose()
        hatespeech_offensive=hatespeech_offensive.rename({0: 'Hate Speech', 1: 'Offensive', 2: 'Neutral'},  axis='columns')
        # appendinge hatespeech_offensive to existing dataframe
        output["hatespeech_offensive"] = hatespeech_offensive.idxmax(axis=1)


        # negative positive neutral prediction
        model = Model()
        model.addModel("static/models/negative_positive_neutral_en/saved_model/random_forest.joblib")
        negativePositiveNeutral=model.predict(df)
        negativePositiveNeutral=negativePositiveNeutral.transpose()
        negativePositiveNeutral=negativePositiveNeutral.rename({0: 'Neutral', 1: 'Positive', 2: 'Negative', 3: 'Mixed'}, axis='columns')
        output["negative_positive_neutral"] = negativePositiveNeutral.idxmax(axis=1)
        print(negativePositiveNeutral)
        cursor, db = self.db.getFreshConnection()
        
        # generating list of columns to insert into database
        cols = "`,`".join([str(i) for i in output.columns.tolist()])


        print(output.head())
        # Insert DataFrame recrds one by one.
        for i,row in output.iterrows():
            sql = "INSERT INTO `tweets_prediction` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
            cursor.execute(sql, tuple(row))

        # the connection is not autocommitted by default, so we must commit to save our changes
        db.commit()

        # close the connection after accomplishing the task
        self.db.close_connection(cursor, db)

    # a function that users the scraper class to scrape the data from the twitter and inserts into the database
    def scrape(self, username):
        obj = Scraper(username)
        cursor, db = self.db.getFreshConnection()

        # populate user data from twitter like the photo, number of followers etc
        obj.populateUserData(cursor)

        # scrape tweets from twitter and start inserting into the database
        obj.populateUserTweets(100, cursor)
        db.commit()
        self.db.close_connection(cursor, db)

    # this funciton acts as the query handler for the prediction model
    # it looks if a query needs attention and then call the make_prediction function to predict the data and store it back to the database
    def predict(self):
        
        while(1):
            cursor, db = self.db.getFreshConnection()

            # getting the queries which have status => ready to start <= only
            cursor.execute('''select * from query where status =1
            limit 1

            ''')


            row = cursor.fetchone()
               
            # if there is no query which is ready to start, then sleep for 10 seconds
            if(row is None):
                self.db.close_connection(cursor, db)
                print("sleeping")
                time.sleep(10)

                continue
            else:
                # a data exist to be scraped

                #change the status of the data to working
                cursor.execute("UPDATE `query` set status = 2 where id= %s",[row[0]])
                db.commit()

                # close the connection so other nodes could start processing
                self.db.close_connection(cursor, db)
                if 1==1:
                    # self.scrape(row[2])
                    

                    # try making the prediction given the username 
                    # if an error occurs, exception would be handled
                    self.make_prediction(row[2])

                    # if the prediction goes well, then update the status to completed
                    cursor, db = self.db.getFreshConnection()


                    cursor.execute("UPDATE `query` set status = 4 where id= %s",[row[0]])
                    db.commit()
                    self.db.close_connection(cursor, db)
                # except Exception as e:
                #     cursor, db = self.db.getFreshConnection()
                #     print("Exception")
                #     print(e )
                #     cursor.execute("UPDATE `query` set status = 3 where id= %s",[row[0]])
                #     db.commit()
                #     self.db.close_connection(cursor, db)



obj = Predicting()
obj.predict()
time.sleep(5)

# importing libraries and packages
from signal import CTRL_BREAK_EVENT
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import numpy as np
import re
import re
import nltk
from nltk.corpus import stopwords

#downloading stopwords frm nltk resource to be removed from the tweets upon scraping
nltk.download('stopwords')

# removing emoji for the data cleaning part
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


# scraper class to handle the data cleaning and scraping
class Scraper():

    # constructor to initalise variables to be used
    def __init__(self, userName):
        self.userName = userName
        self.profileURL = None
        self.name = None
        self.followersCount = None
        self.desc = None
        self.location = None
        self.profileImage = None
        self.isVerified = None


    # this function will scrape data and push to the database
    # this funciton only includes the user profile data like the number of followers etc
    def populateUserData(self, db):
        for i in sntwitter.TwitterSearchScraper('from:' + self.userName).get_items():
            self.profileURL = 'https://twitter.com/' + self.userName
            self.name = i.user.displayname
            self.followersCount = i.user.followersCount
            self.desc = i.user.description
            self.location = i.user.location
            self.profileImage = i.user.profileImageUrl
            self.isVerified = i.user.verified
            break
        # db.setUser(self.userName, self.profileURL, self.profileImage, self.name, self.desc, self.location,
        #            self.followersCount, self.isVerified)
        db.execute("REPLACE INTO `users_profile` (`username`, `profileURL`, `profileImage`, `name`, `description`, `location`, `followersCount`, `isVerified`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(self.userName, self.profileURL, self.profileImage, self.name, self.desc, self.location,self.followersCount, self.isVerified))
    
    # function to clean the scrapped tweet and insert it into a seperate column as cleaned_content
    # This function removes stopwords, remove mentions, hashtags and only the raw tweet is available
    def clean_tweet(self, tweet):
        if type(tweet) == np.float:
            return ""
        temp = tweet.lower()
        temp = re.sub("'", "", temp) # to avoid removing contractions in english
        temp = re.sub("@[A-Za-z0-9_]+","", temp)
        temp = re.sub("#[A-Za-z0-9_]+","", temp)
        temp = re.sub(r'http\S+', '', temp)
        temp = re.sub('[()!?]', ' ', temp)
        temp = re.sub('\[.*?\]',' ', temp)
        temp = re.sub("[^a-z0-9]"," ", temp)
        temp = temp.split()
        temp = [w for w in temp if not w in stopwords.words()]
        temp = " ".join(word for word in temp)
        return temp

    # funciton to scrape tweets from the user profile and insert them back to the database available for processing and prediction
    def populateUserTweets(self, noOfTweets, db):
        # Creating list to append tweet data
        tweets_list1 = []
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper('from:' + self.userName).get_items()):  # declare a username
            if i > noOfTweets:  # number of tweets you want to scrape
                break
            tweets_list1.append(
                [tweet.date, tweet.id, tweet.content, tweet.user.username])  # declare the attributes to be returned

        # Creating a dataframe from the tweets list above
        tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
        for index, i in tweets_df1.iterrows():
            date_time_obj = datetime.strptime(str(i['Datetime'])[:19], '%Y-%m-%d %H:%M:%S')
            if len(self.clean_tweet(i['Text'])) > 0:
                db.execute("INSERT INTO `tweets` (`id`, `tweetID`, `content`, `tweetTS`, `username`, `cleaned_content`) VALUES (NULL, %s, %s, %s, %s, %s)",(i['Tweet Id'], i['Text'].encode('ascii', 'ignore'), date_time_obj, i['Username'], self.clean_tweet(i['Text'])))
            # db.setTweets(i['Tweet Id'], i['Text'].encode('ascii', 'ignore'), date_time_obj, i['Username'])
        db.execute("update query set status=1 where status=0 and keyword=%s;", [self.userName])
        print("All Tweets Added to DB")


    # function to test the scrapper 
    def display(self):
        print(self.userName)
        print(self.profileURL)
        print(self.name)
        print(self.followersCount)
        print(self.desc)
        print(self.location)
        print(self.profileImage)
        print(self.isVerified)


# # Initiate connection to the databse.
# db = DB.init()
# # Run the Scraper
# username = 'haris__manzoor'
# obj = Scraper(username)
# obj.populateUserData(db)
# obj.populateUserTweets(10, db)

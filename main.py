# importing necessary libraries and packages
import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import snscrape.modules.twitter as twitterscraper
from pymongo import MongoClient

# Global variable required for the program flow
current_timestamp = datetime.now()


# Function for initial configuration of dashboard
def initial_config():
    # Setting the page configuration, giving title and brief explanation to users
    st.set_page_config(page_title="Twitter Scrapping",
                       page_icon=":hash:",
                       layout="wide",
                       menu_items={"About": "This is a mini version of twitter scraping app. You can download the "
                                            "scraped data either in csv or json format"})
    st.title("Twitter Scrapping!!!")
    st.write("This app displays scrapped data from twitter")


def dashboard_input():
    # The user to provide the keyword or any part of sentence of the tweet contents to be scrapped
    # A variable named "text" assigned to the keyword in order to use it further in the below coding
    txt = st.text_input("Keyword or Hashtag:")

    # User to provide start date and end date so that the tweets can be scrapped from those period of days
    # Variables assigned to the dates in order to use it further in the below coding
    start_init_date = st.date_input("Start Date",
                                    max_value=date.today(),
                                    key="a")
    end_init_date = st.date_input("End Date",
                                  max_value=date.today(),
                                  key="b")

    # The user to provide the number of tweet counts to be scrapped from Twitter
    max_no_tweets = st.slider("Tweet Count",
                              min_value=1,
                              max_value=1000)
    return txt, start_init_date, end_init_date, max_no_tweets


# Function to check the validity of start and end dates
def date_check(start_dt, end_dt):
    # If start and end dates are same, a day is added to the end date to overcome since(inclusive)/until(exclusive).
    # Raising error and indicating user to select the dates properly of TwitterSearchScraper
    valid = True
    if start_dt < end_dt:
        st.success(f"start date: {start_dt} \n\n end date: {end_dt}")
    elif start_dt == end_dt:
        st.success(f"start date: {start_dt} \n\n end date: {end_dt}")
        end_dt += timedelta(1)
    else:
        st.error("Error. End date must fall on or after start date ", icon="🚨")
        valid = False

    return start_dt, end_dt, valid


# Function for scrapping the data from Twitter using snscrape library
def tweet_scrape(hashtag, st_dt, nd_dt, tweet_count):
    tweet_list = list()

    # Enumerate to have control over the number of tweets to be scraped
    st.subheader("Scraped Data :")
    for i, tweet in enumerate(
            twitterscraper.TwitterSearchScraper(f"{hashtag} since:{st_dt} until:{nd_dt}").get_items()):
        if i > tweet_count:
            break

        # The scrapped data is appended to a list
        tweet_list.append(
            {
                "date": tweet.date,
                "id": tweet.id,
                "url": tweet.url,
                "user": tweet.user.username,
                "content": tweet.rawContent,
                "reply_count": tweet.replyCount,
                "retweet_count": tweet.retweetCount,
                "language": tweet.lang,
                "source": tweet.source,
                "like_count": tweet.likeCount,
                "hashtag": tweet.hashtags
            }
        )
    # scraped data is then returned in the form of dictionary
    tweet_dict = {
        f"{hashtag}+{current_timestamp}": tweet_list
    }
    return tweet_dict


def tweets_for_dashboard(dict_of_tweets, hashtag):
    df = pd.DataFrame(dict_of_tweets[f"{hashtag}+{current_timestamp}"], dtype=str)

    return df


# Function for downloading the file in multiple formats from dashboard
def data_download(df, hashtag):
    # Choice of the user to select the format of the data to be downloaded
    st.download_button("Download as csv file",
                       data=df.to_csv(),
                       file_name=f"{hashtag}.csv",
                       mime="text/csv")

    st.download_button("Download as Json file",
                       data=df.to_json(indent=1),
                       file_name=f"{hashtag}.json")


# Function for uploading the data in Mongo DB
def upload_db(dict_of_tweets):
    st.button("Upload to MongoDB")
    client = MongoClient("mongodb://localhost:27017/")
    db = client["twitter_scraping"]
    col = db["scraped_data"]
    col.insert_one(dict_of_tweets)


# Program execution
if __name__ == "__main__":
    # Function call for the initial configuration on dashboard
    initial_config()
    # Function call to get all the required data from the dashboard
    text, st_date, nd_date, max_tweets = dashboard_input()

    # submit button on dashboard
    # The scrapped data will appear on the dashboard in the form of a table
    # All the other functions like downloading the database in csv or json format, uploading the data in noSQL DB,
    # Will be executed One by One after clicking the submit button

    if st.button("Submit"):
        # Function call to check for the valid start and end dates
        start_date, end_date, valid_check = date_check(st_date, nd_date)

        if valid_check:
            # Function call to scrape the data for the valid dates
            tweets_dict = tweet_scrape(text, start_date, end_date, max_tweets)
            # Function call to get the scraped data as data frame
            df_of_tweets = tweets_for_dashboard(tweets_dict, text)
            # Displays the data frame on dashboard
            st.dataframe(df_of_tweets)
            # Function call to download the data in multiple formats csv/json
            data_download(df_of_tweets, text)
            # Upload the scraped data to Mongo DB
            upload_db(tweets_dict)

# twitter_scrapper_mini_project
# Twitter_scrapper

This project is built using

•	Streamlit

•	Snscrape

•	Pandas

•	Pymongo

•	Datetime


Twitter Scrapper

Below is the dashboard created for scrapping twitter data with the help of streamlit.

 ![image](https://user-images.githubusercontent.com/115402011/213877533-7ee89916-5a9a-46e0-81be-4f6092fd47d4.png)

The inputs to the dashboard are
1.	Keyword / Hashtag to be scrapped
2.	From date
3.	To date 
4.	Maximum tweet count

Output 1
The scrapped data represented as a table according to above inputs
The start and end dates are validated and displayed on the dashboard 

 ![image](https://user-images.githubusercontent.com/115402011/213877553-6feeefc8-528d-45aa-a1ab-90c72cc25b26.png)

Output 2
Two download options provided to download the data in csv and json format

 ![image](https://user-images.githubusercontent.com/115402011/213877561-6ac3bb43-038a-4e6c-afc3-46b6167d2538.png)

Output 3
Upload to MongoDB option given to save all the scrapped data for future reference
NOTE: To upload the scrapped data to MongoDB, The user should make sure to download and install MongoDB Community Server.

 ![image](https://user-images.githubusercontent.com/115402011/213877573-85766e3b-1137-4358-9c15-3bba546db86d.png)

Output 4
The scrapped data uploaded in MongoDB under twitter_scraping database and scraped_data collection.
The scrapped data uploaded as a single dictionary document inside the collection along with the hashtag or keyword used to scrape the data + current time stamp

 ![image](https://user-images.githubusercontent.com/115402011/213877600-2da8d04a-f95c-4adf-87fa-823c2e5dfe30.png)


Installations required

Pip

•	pip install streamlit

•	pip install snscrape

•	pip install pandas

•	pip install datetime

•	pip install pymongo


MongoDB

•	MongoDB Compass

https://www.mongodb.com/docs/compass/current/install/


•	MongoDB Community Server

https://www.mongodb.com/try/download/community

Run Streamlit

Streamlit run main.py

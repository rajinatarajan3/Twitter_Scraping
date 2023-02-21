
import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
import base64

keyword = st.text_input('Enter a twitter search query')
since_date = str(st.date_input("Select the since date"))
until_date =str(st.date_input("until_date"))
limits= st.number_input("Enter the tweet limit",min_value=1.0,max_value=1000.0)
tweets=[]
query= keyword +" since:"+since_date+ " until:"+until_date
if st.button('Search Tweets'):
    st.write(f'Tweets matching "{query}')
    
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == int(limits):
            break
        else:
            tweets.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])
            tweet_data = {
                'date':tweet.date,
                'id':tweet.id,
                'url':tweet.url,
                'content':tweet.content,
                'user': tweet.user,
                'replyCount':tweet.replyCount,
                'retweetCount':tweet.retweetCount,
                'language':tweet.lang,
                'source':tweet.source,
                'likeCount': tweet.likeCount
                }       
    df=pd.DataFrame(tweets,columns=["Date","Id","Url","Tweet_content","User","Reply_count","Retweet_count","Language","Source","Like_count"])

    st.write(df)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv"> Download CSV file </a>'
    st.markdown(href, unsafe_allow_html=True)

    json = df.to_json(orient='records')
    b64= base64.b64encode(json.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="data.json"> Download Json file </a>'
    st.markdown(href, unsafe_allow_html=True)
    
    if st.button("Database"):
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=client["project1"]
        collection=mydb["collection"]
        collection.insert_one(tweet_data)    
    

from dotenv import load_dotenv
import os
import pandas as pd
import requests
import json
import pandas as pd
from openai import OpenAI
import tweepy
import time
from scrapethat import *

def get_one_box(box):
    title = box.select_one('h2').text
    teaser = box.select('p')[1].text
    link = "https://www.coindesk.com/" + box.select('a')[1]['href']
    return {
        'title': title,
        'teaser': teaser,
        'link': link
    }

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")

# get news

t = read_cloud('https://www.coindesk.com/latest-crypto-news')

# news_text = '\n'.join([x.text  for x in t.select('.bg-white.flex.gap-6.w-full.shrink.justify-between')])
df = pd.DataFrame(list(map(get_one_box, t.select('.bg-white.flex.gap-6.w-full.shrink.justify-between'))))

news_text = df.to_dict(orient='records')


# Prompt prepatation
prompt = f"""
You are an expert in cryptocurrency news summarization. Your task is to:
1. Select the **4-5 most important news items** from the provided data.
2. Summarize each news item concisely.
3. Present the output as a plain text list, avoiding Markdown syntax entirely.
4. Include emojis directly in the titles to increase engagement.
5. Include the link to the article at the end of each item without "Read more" or extra words.

Here is the news data:
{news_text}

Requirements:
1. Your response should only contain the plain text list with the top 4-5 most important news items.
2. Summarize the key points into a maximum of 280 characters per item.
3. Highlight the most important news items and use appropriate hashtags (e.g., #Crypto, #Bitcoin).
4. Use emojis where relevant for engagement directly in the text.
5. Include hashtags only at the end of the last post.
6. Ensure your response fits the character limits and formatting of Twitter threads.
7. Make sure you split the articles with two newlines (\n\n).
8. The response should only be the Twitter posts and nothing else.
"""


client = OpenAI(
    #api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    api_key = OPEN_AI_API_KEY
    )

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4o",
)


new_post = chat_completion.choices[0].message.content
postok = new_post.split('\n\n')
# check if text startswith  '- ' if yes that remove from begining
postok = [x[2:] if x.startswith('- ') else x for x in postok]
# remove post if it is  '---'
postok = [x for x in postok if x != '---']

# remove if starts with #
postok = [x for x in postok if not x.startswith('#')]

# check if post lengtht is less than 280 characters
# postok = [x for x in postok if len(x) <= 320]


print(postok)


# Twitter API
# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(
    ACCESS_KEY,
    ACCESS_SECRET,
)
# this is the syntax for twitter API 2.0. It uses the client credentials that we created
newapi = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)

# Create API object using the old twitter APIv1.1
api = tweepy.API(auth)

print(api.rate_limit_status())
time.sleep(10)


main_tweet = f"📰 Daily Crypto Highlights {pd.Timestamp.now().strftime('%Y-%m-%d')} !"

# FMain tweet
main_post = newapi.create_tweet(text=main_tweet)
time.sleep(10)

# A thread ID
thread_id = main_post.data['id']

# Thread létrehozása
for tweet_content in postok:
    try:
        print('posting')
        time.sleep(20)
        thread_post = newapi.create_tweet(
            text=tweet_content,
            in_reply_to_tweet_id= thread_id  
        )
        print(tweet_content)
    except Exception as e:
        print(e)
        pass



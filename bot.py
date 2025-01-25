from dotenv import load_dotenv
import os
import pandas as pd
import requests
import json
import pandas as pd
from openai import OpenAI
import tweepy
import time

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
print('-----------------')
print(ACCESS_KEY[0])
print(ACCESS_KEY[-1])
print('-----------------')

print(ACCESS_SECRET[0])
print(ACCESS_SECRET[-1])
print('-----------------')

print(CONSUMER_KEY[0])
print(CONSUMER_KEY[-1])
print('-----------------')

print(CONSUMER_SECRET[0])
print(CONSUMER_SECRET[-1])
print('-----------------')

print(BEARER_TOKEN[0])
print(BEARER_TOKEN[-1])

    

headers = {
    'accept': 'text/x-component',
    'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'text/plain;charset=UTF-8',
    # 'cookie': 'country=HU; city=Budapest; region=fra1; currencyCode=HUF; _pbjs_userid_consent_data=3524755945110770; _gtmeec=e30%3D; _fbp=fb.1.1737578090165.1656185372; _gcl_au=1.1.157704988.1737578978; FPAU=1.1.157704988.1737578978; CookieConsent={stamp:%276wElLcrlArOaQYv72KK7rHNcXazbG1F909Z1x5djCY2aw7vvu7VjTQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:10%2Cutc:1737578977707%2Cregion:%27hu%27}; _ga=GA1.1.385283001.1737578975; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://www.coindesk.com/latest-crypto-news%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1737578978242%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=28a03ae6-2ab9-46a3-bde6-d88de109f52a%22%2C%22session_count%22:1%2C%22last_session_ts%22:1737578978242}; subregion=Central%20Europe; oficialCountryName=Hungary; currencySymbol=Ft; currencyName=Hungarian%20forint; FPID=FPID2.2.UBTQPNtesSjuOaTZp1nyAdGMqnSiYMXilThOtWFvjzM%3D.1737578975; FPLC=4eZYa2Q9D8CktLR6iQTgMRLzeLYkgd%2BSKNQiRdtdSBVpYYX%2BtPdg3a3sGIs4GN%2F%2BvuEoLwM4zSXVaud1sfsxqoJeY1xSRzakMnf3AOC%2BDc3yPH012UJrUNY9QF0njQ%3D%3D; COINDESK_PREFERENCES=eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkQXQiOjE3Mzc1NzkzNzM5MjMsImxhc3RBY2Nlc3NlZCI6MTczNzU3OTM3MzkyNCwidGhlbWUiOiJsaWdodCIsImlhdCI6MTczNzU3OTM3MywiZXhwIjoxNzQ1MzU1MzczLCJpc3MiOiJjb29raWUtc2VydmljZSIsImF1ZCI6InVzZXIifQ.OfmH8RSMcLMV3Mrlr2Ak2Wp-PQ7Ip4aF9Y2eloI7oc0; COINDESK_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkQXQiOjE3Mzc1NzkzNzM5MjQsImxhc3RBY2Nlc3NlZCI6MTczNzU3OTM3MzkyNSwicGxhbiI6eyJuYW1lIjoiNS1wbGFuIiwibGltaXQiOjUsInBlcmlvZCI6Im1vbnRocyIsImR1cmF0aW9uIjoxLCJyb2xsaW5nIjpmYWxzZX0sInN0YXJ0RGF0ZSI6MTczNzU3OTM3MzkyNCwiYXJ0aWNsZXNSZWFkIjowLCJhbGxvd2VkIjpbXSwiY29udmVydGVkIjpmYWxzZSwiaWF0IjoxNzM3NTc5MzczLCJleHAiOjE3NDUzNTUzNzMsImlzcyI6ImNvb2tpZS1zZXJ2aWNlIiwiYXVkIjoidXNlciJ9.wyhaJYAmFSqATOzPb2SYOwZNQZ3tF8OREo0-xWf_nbQ; locale=en; sailthru_pageviews=3; _rdt_uuid=1737578978253.4ff1059d-c81c-4356-89ec-84e0003935de; sailthru_content=cafa2c926904464b3f48ba5f4d182b92; sailthru_visitor=e6698c1b-96fa-419d-bec7-bebf5d9a5cf4; cto_bundle=jThB619iYlRldnVLRnU1YmJRWGpCY2dSbHRQdGhVY2ljcTBTWm9wM25oOWJMQUhYUmRuR0o0QjhjU1l2MHdWRFlUUHFjYmVCOXdDazVFbVNRZEZMNE02RHlZb1d5cjUlMkIlMkYzRzJudGJhWWVKZXB3UEI2RmJOdUhLcHlqRjJKOXlSJTJGdnNEeiUyRkZNNSUyQlpFNyUyQldtblY0ZW1VN3QyZkElM0QlM0Q; _ga_VM3STRYVN8=GS1.1.1737578972.1.1.1737579765.0.0.1191420872; _pn_Zepx0dJv=eyJzdWIiOnsidWRyIjowLCJpZCI6Ik9CWmhzbmZXc25iUVVFNXloTU1wMWRSaDhHaXRaWUZhIiwic3MiOi0xfSwibHVhIjoxNzM3NTc5NzY1OTE3fQ; _dd_s=rum=2&id=af5ebce1-38db-400b-b4c6-8ca605f2166b&created=1737578975791&expire=1737580669014',
    'next-action': '40e2c881baef274abca4f12f54acf2d96cb0f3fbf7',
    'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(media)%22%2C%7B%22children%22%3A%5B%22latest-crypto-news%22%2C%7B%22children%22%3A%5B%22__PAGE__%3F%7B%5C%22viewport%5C%22%3A%5C%22desktop%5C%22%2C%5C%22country%5C%22%3A%5C%22HU%5C%22%2C%5C%22city%5C%22%3A%5C%22Budapest%5C%22%2C%5C%22countryRegion%5C%22%3A%5C%22BU%5C%22%2C%5C%22region%5C%22%3A%5C%22fra1%5C%22%2C%5C%22subregion%5C%22%3A%5C%22Central%2BEurope%5C%22%2C%5C%22oficialCountryName%5C%22%3A%5C%22Hungary%5C%22%2C%5C%22currencyCode%5C%22%3A%5C%22HUF%5C%22%2C%5C%22currencySymbol%5C%22%3A%5C%22Ft%5C%22%2C%5C%22currencyName%5C%22%3A%5C%22Hungarian%2Bforint%5C%22%2C%5C%22locale%5C%22%3A%5C%22en%5C%22%7D%22%2C%7B%7D%2C%22%2Flatest-crypto-news%22%2C%22refresh%22%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%5D',
    'origin': 'https://www.coindesk.com',
    'priority': 'u=1, i',
    'referer': 'https://www.coindesk.com/latest-crypto-news',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-deployment-id': 'dpl_3A2Z8eMigbuGovJ5WxWZeYsbWGUe',
}

data = '[{"size":100,"page":1}]'

response = requests.post('https://www.coindesk.com/latest-crypto-news', headers=headers, data=data)
t = response.text
t = t.split('\n')

raw_data=t[8]
start_index = raw_data.find("{")  # Az első "{" pozíciója
json_data = raw_data[start_index:]  # Minden innen indul

# JSON betöltése
try:
    parsed_data = json.loads(json_data)
    print("JSON sikeresen feldolgozva:")
except json.JSONDecodeError as e:
    print(f"Hiba történt a JSON feldolgozásakor: {e}")
    

# Convert the JSON data to a DataFrame
df = pd.DataFrame(list(map(lambda x:{
    "title" : x.get('title'),
    "body" : x.get('description'),
    "url" : "https://www.coindesk.com/" + x.get('pathname'),
    "publish_date": x.get('date')['displayDate']
}, parsed_data['articles'])))


#filter df if publish date older than 24 hours with format 2025-01-23T13:40:35Z
df['publish_date'] = pd.to_datetime(df['publish_date'], format='mixed')


# Get the current time in UTC
current_time = pd.to_datetime('now', utc=True)

# Filter rows where the publish date is within the last 24 hours
df = df[df['publish_date'] > current_time - pd.Timedelta(days=1)]


# Convert the DataFrame to a list of dictionaries
news_data = df[['title', 'body', 'url']].to_dict(orient='records')

# Prompt prepatation
prompt = f"""
You are an expert in cryptocurrency news summarization. Your task is to:
1. Select the **4-5 most important news items** from the provided data.
2. Summarize each news item concisely.
3. Present the output as a plain text list, avoiding Markdown syntax entirely.
4. Include emojis directly in the titles to increase engagement.
5. Include the link to the article at the end of each item without "Read more" or extra words.

Here is the news data:
{news_data}

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


#print(prompt)



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

main_tweet = f"📰 Daily Crypto Highlights {pd.Timestamp.now().strftime('%Y-%m-%d')} !"

# FMain tweet
main_post = newapi.create_tweet(text=main_tweet)

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


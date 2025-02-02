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

headers = {
    'accept': 'text/x-component',
    'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'text/plain;charset=UTF-8',
    # 'cookie': '_pbjs_userid_consent_data=3524755945110770; _gtmeec=e30%3D; _fbp=fb.1.1737578090165.1656185372; _gcl_au=1.1.157704988.1737578978; FPAU=1.1.157704988.1737578978; _ga=GA1.1.385283001.1737578975; FPID=FPID2.2.UBTQPNtesSjuOaTZp1nyAdGMqnSiYMXilThOtWFvjzM%3D.1737578975; CookieConsent={stamp:%27teFTgegWbj1MVj/5EJtzbuo7a+z/Ha0aADb5RHp4fyXCgZCwy0cVNA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:10%2Cutc:1738314860945%2Cregion:%27hu%27}; COINDESK_PREFERENCES=eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkQXQiOjE3MzgzMTQ4NTAxMjksImxhc3RBY2Nlc3NlZCI6MTczODQyNDQ4MDY5MSwidGhlbWUiOiJsaWdodCIsImlhdCI6MTczODQyNDQ4MCwiZXhwIjoxNzQ2MjAwNDgwLCJpc3MiOiJjb29raWUtc2VydmljZSIsImF1ZCI6InVzZXIifQ.-ClXwVJPvdH7preHs_CFsHqXoGaJ_GEmL-9WHYNLpoo; _parsely_session={%22sid%22:7%2C%22surl%22:%22https://www.coindesk.com/latest-crypto-news%22%2C%22sref%22:%22%22%2C%22sts%22:1738424483389%2C%22slts%22:1738314854617}; _parsely_visitor={%22id%22:%22pid=28a03ae6-2ab9-46a3-bde6-d88de109f52a%22%2C%22session_count%22:7%2C%22last_session_ts%22:1738424483389}; FPLC=%2FaUjjpPF6BxUEigqGIxSV%2FNsG%2FCo9bdZmu1JgBBBGS56c%2BqAZQbjCKu7sxZCinLEoBTXlUQGZ7sdSmJSB5KLxF5Ptk0uHEaQni2opWqEONX%2F%2FqmKG0WPtgEPym88Lg%3D%3D; sailthru_pageviews=2; _rdt_uuid=1737578978253.4ff1059d-c81c-4356-89ec-84e0003935de; sailthru_content=01ccae6c19066797b9741b6ca3b0528f5d52d950ebbbf61248bdbad1a1d537a2f4618b8837368562f9d01fbc250e974be3b5f228491628bb7ac74c1409a83f1bcafa2c926904464b3f48ba5f4d182b92; sailthru_visitor=e6698c1b-96fa-419d-bec7-bebf5d9a5cf4; cto_bundle=AkQP5l9iYlRldnVLRnU1YmJRWGpCY2dSbHRJTldWalhFMmxnWkElMkJ3Q0ZNQnkxRnU5Vlp6clFTb0ZPd1lKSFdTcWFNZzdaa1d4bUdYVyUyRlZ3eFBOOHhmQmc0YWN4WFFyVDc5S3VxaUwxM3B6aGlOTHZPaXdxSjN2cFNPZU11THd4aGFCV2N4bFROVWdSSUgyNDgwUyUyQnRxWnFUUHclM0QlM0Q; _pn_Zepx0dJv=eyJzdWIiOnsidWRyIjowLCJpZCI6Ik9CWmhzbmZXc25iUVVFNXloTU1wMWRSaDhHaXRaWUZhIiwic3MiOi0xfSwibHVhIjoxNzM4NDI0NDkyMjU1fQ; COINDESK_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVkQXQiOjE3MzgzMTQ4NTAxMjksImxhc3RBY2Nlc3NlZCI6MTczODQyNDU5MjAyOCwicGxhbiI6eyJuYW1lIjoiMy1wbGFuIiwibGltaXQiOjMsInBlcmlvZCI6Im1vbnRocyIsImR1cmF0aW9uIjoxLCJyb2xsaW5nIjpmYWxzZX0sInN0YXJ0RGF0ZSI6MTczODMxNDg1MDEyOSwiYXJ0aWNsZXNSZWFkIjowLCJhbGxvd2VkIjpbXSwiY29udmVydGVkIjpmYWxzZSwiaWF0IjoxNzM4NDI0NTkyLCJleHAiOjE3NDYyMDA1OTIsImlzcyI6ImNvb2tpZS1zZXJ2aWNlIiwiYXVkIjoidXNlciJ9.-ELxfnGe1rP2ufLZG0gZ5pI1nLng4dJWq6Ffyl5iyfc; _ga_VM3STRYVN8=GS1.1.1738424483.7.1.1738424592.0.0.313145541; FPGSID=1.1738424483.1738424593.G-VM3STRYVN8.QBHcydfbqJPRCPozHZU_dQ; _dd_s=rum=2&id=cf635c13-32b4-4a54-b78a-99680d1603d1&created=1738424487194&expire=1738425494971',
    'next-action': '40e09715dcf3114df59d795c0a0195fedff1b5a3c7',
    'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(media)%22%2C%7B%22children%22%3A%5B%22latest-crypto-news%22%2C%7B%22children%22%3A%5B%22__PAGE__%3F%7B%5C%22viewport%5C%22%3A%5C%22desktop%5C%22%2C%5C%22country%5C%22%3A%5C%22HU%5C%22%2C%5C%22city%5C%22%3A%5C%22Budapest%5C%22%2C%5C%22countryRegion%5C%22%3A%5C%22BU%5C%22%2C%5C%22region%5C%22%3A%5C%22fra1%5C%22%2C%5C%22subregion%5C%22%3A%5C%22Central%20Europe%5C%22%2C%5C%22oficialCountryName%5C%22%3A%5C%22Hungary%5C%22%2C%5C%22currencyCode%5C%22%3A%5C%22HUF%5C%22%2C%5C%22currencySymbol%5C%22%3A%5C%22Ft%5C%22%2C%5C%22currencyName%5C%22%3A%5C%22Hungarian%20forint%5C%22%2C%5C%22locale%5C%22%3A%5C%22en%5C%22%7D%22%2C%7B%7D%2C%22%2Flatest-crypto-news%22%2C%22refresh%22%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%5D',
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
    'x-deployment-id': 'dpl_8xgtKAS1hbW6HpqpLZ6K79VzPyEX',
}

data = '[{"size":100, "page":1}]'

response = requests.post('https://www.coindesk.com/latest-crypto-news', headers=headers, data=data)
t = response.text
t = t.split('\n')

raw_data=list(filter(lambda x: "articles" in x, t))[0]
start_index = raw_data.find('{"articles')  # Az első "{" pozíciója
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

df_top8 = df.head(8)

# Get the current time in UTC
current_time = pd.to_datetime('now', utc=True)

# Filter rows where the publish date is within the last 24 hours
df = df[df['publish_date'] > current_time - pd.Timedelta(days=1)]
if len(df) < 8:
    df = df_top8

# Reset the index of the filtered DataFrame
df.reset_index(drop=True, inplace=True)

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


print(prompt)



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



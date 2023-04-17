import os
import smtplib
from email.message import EmailMessage

import pandas as pd
import praw
import requests
from dotenv import load_dotenv
from IPython.display import HTML

load_dotenv()
# set up oauth and connect to Reddit API via PRAW
client_id, client_key = os.getenv("CLIENT_ID"), os.getenv("SECRET_KEY")
auth = requests.auth.HTTPBasicAuth(client_id, client_key)

reddit = praw.Reddit(client_id=client_id, client_secret=client_key, username=os.getenv(
    "REDDIT_USERNAME"), password=os.getenv("REDDIT_PASSWORD"), user_agent="MyBot/0.0.1 by @Jetskiis")

# initialize Pandas DataFrame

hot_df = pd.DataFrame()
best_df = pd.DataFrame()

hot_df.style.set_table_styles(
    [dict(selector='th', props=[('text-align', 'left')])])
best_df.style.set_table_styles(
    [dict(selector='th', props=[('text-align', 'left')])])



# build dataframe
# subscribed_subreddits = reddit.user.subreddits(limit=None)

for post in reddit.front.best(limit=25):
    new_row = pd.DataFrame(
        {"Title": "-  " + post.title, "Subreddit": f'<a href="https://new.reddit.com{post.permalink}">{post.subreddit}</a>', "Score": post.score}, index=pd.Index([len(best_df)]))
    best_df = pd.concat([best_df, new_row])


for post in reddit.front.hot(limit=25):
    new_row = pd.DataFrame(
        {"Title": "-  " + post.title, "Subreddit": f'<a href="https://new.reddit.com{post.permalink}">{post.subreddit}</a>', "Score": post.score}, index=pd.Index([len(hot_df)]))
    hot_df = pd.concat([hot_df, new_row])


# print(best_df)
# print(hot_df)

# build output html
html = """\
<html>
  <head></head>
  <body style="font-size: 1rem">
  <h2 style="text-align: center">Sort by Best</h2>
    {0}
  <h2 style="text-align: center">Sort by Hot</h2>
    {1}
  </body>
</html>
""".format((best_df.to_html(escape=False, index=False, justify="center", border=0)), (hot_df.to_html(escape=False, index=False, justify="center", border=0)))

# send data to email
msg = EmailMessage()
msg["Subject"] = "Reddit Feed"
msg["From"] = os.getenv("EMAIL")
msg["To"] = os.getenv("RECIPIENT_EMAIL")
msg.set_content(html, subtype="html")

s = smtplib.SMTP('smtp-mail.outlook.com', 587)
s.starttls()
s.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
s.send_message(msg)
s.quit()

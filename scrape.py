#!/usr/bin/env python3
import sys, time, sched, json, threading, re

from urllib.request import urlopen
from bs4 import BeautifulSoup
from bottle import route, run, template

if len(sys.argv) < 2:
    print("Need a twitter handle as an argument.")
    sys.exit(0)

handle = sys.argv[1]
if re.match(r'^[a-zA-Z_0-9]{1,15}$', handle) is None:
    print("Invalid twitter handle %s. Max 15 chars and letters A-Z,"\
           "numbers 0-9 and underscores allowed." % handle)
    sys.exit(0)

print("Monitoring %s" % handle)
collected = []

def fetch(sc):
    #Scrape the mobile version for tweets as its not doing any funky xhr
    url = ("https://mobile.twitter.com/%s" % handle)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    tweets = soup.find_all("div", attrs={"class":"tweet-text"})

    for tweet in tweets:
        tweet_text = tweet.find('div',{"class":'dir-ltr'}).text.strip()
        if tweet_text in collected:
            break
        collected.append(tweet_text)
        print(tweet_text)
        print("----")

        if len(collected) == 5:
            break

    s.enter(600, 1, fetch, (sc,)) #Schedule another run in 10 minutes

#Create a scheduled loop in a new thread so the web server can run on main
s = sched.scheduler(time.time, time.sleep)
t = threading.Thread(target=s.run)
s.enter(0, 1, fetch, (s,))
t.start()

# Server some pretty json tweets
@route('/tweets')
def index():
    return json.dumps(collected, indent=2)

run(host='localhost', port=8080)
## Twitter Scraper

Simple script to monitor a twitter handle. On start last 5 tweets will print to std out followed by 10 minute updates.

### Usage

```
pip install -r requirements
python scrape.py abcnews
```

### Web Server

A web server runs that outputs a json of all collected tweets so far:

```
curl http://localhost:8080/tweets
```

### Docker service

```
sudo docker build .
sudo docker run -p 8080 <imageid>
``` 
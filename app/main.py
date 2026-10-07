import feedparser

url = "https://feeds.bbci.co.uk/news/technology/rss.xml"
feed = feedparser.parse(url)

for entry in feed.entries[:5]:
    print(entry.title)
    print(entry.link)
    print()
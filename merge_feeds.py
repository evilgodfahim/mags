import feedparser
import hashlib
import requests
from datetime import datetime
from feedgen.feed import FeedGenerator

# List of feed URLs
FEED_URLS = [
    "https://www.scientificamerican.com/platform/syndication/rss/",
    "https://feeds.newscientist.com/science-news",
    "https://nautil.us/feed/",
    "http://ftr.fivefilters.org/makefulltextfeed.php?url=http%3A%2F%2Fmentalfloss.com%2Frss.xml&max=9",
    "https://www.theatlantic.com/feed/channel/ideas/",
    "https://www.popsci.com/rss.xml",
    "https://www.psychologytoday.com/intl/front/feed",
    "https://theconversation.com/us/topics/psychology-28/articles.atom",
    "https://theconversation.com/us/topics/artificial-intelligence-ai-90/articles.atom",
    "https://theconversation.com/global/topics/climate-change-27/articles.atom",
    "https://politepol.com/fd/j6weY8TmEdGW.xml"
]

def main():
    fg = FeedGenerator()
    fg.title("Merged Feed")
    fg.link(href="https://yourusername.github.io/merged-feed/merged.xml", rel="self")
    fg.description("Aggregated RSS from multiple sources")
    fg.language("en")

    seen = set()
    all_entries = []

    for url in FEED_URLS:
        print(f"Fetching {url}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                link = entry.get("link", "")
                if not link:
                    continue
                uid = hashlib.md5(link.encode("utf-8")).hexdigest()
                if uid not in seen:
                    seen.add(uid)
                    all_entries.append(entry)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Sort entries by published date (if available)
    def get_date(entry):
        return entry.get("published_parsed") or entry.get("updated_parsed") or datetime.utcnow().timetuple()

    all_entries.sort(key=get_date, reverse=True)

    for entry in all_entries:
        fe = fg.add_entry()
        fe.title(entry.get("title", "No title"))
        fe.link(href=entry.get("link", ""))
        fe.description(entry.get("summary", ""))
        if "published" in entry:
            fe.pubDate(entry.published)

    fg.rss_file("merged.xml")

if __name__ == "__main__":
    main()

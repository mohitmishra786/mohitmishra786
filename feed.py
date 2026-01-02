import feedparser
import time
import re
from os import path
import requests

def open_readme():
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
        readme = f.read()
    return readme

def write_readme(updated):
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(updated)

def modify_readme(readme, text, identifier=''):
    start_tag = f'<!-- {identifier}_START -->'
    end_tag = f'<!-- {identifier}_END -->'
    pattern = f'{re.escape(start_tag)}.*?{re.escape(end_tag)}'
    replacement = f'{start_tag}\n{text}\n{end_tag}'
    return re.sub(pattern, replacement, readme, flags=re.DOTALL)

def fetch_rss_posts(feed_url, limit=5):
    posts = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:limit]:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            published = "recent"
            if 'published_parsed' in entry:
                published = time.strftime('%Y-%m-%d', entry['published_parsed'])
            posts.append(f"- [{title}]({link}) ({published})")
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
    return posts

def fetch_twitter_posts(username, limit=3):
    # Public Nitter instances and RSS bridges are flaky.
    # We try multiple stable ones and log any issues.
    sources = [
        f"https://rsshub.app/twitter/user/{username}",
        f"https://nitter.net/{username}/rss",
        f"https://nitter.cz/{username}/rss",
        f"https://nitter.privacydev.net/{username}/rss",
        f"https://nitter.poast.org/{username}/rss",
        f"https://nitter.moomoo.me/{username}/rss"
    ]
    tweets = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for url in sources:
        try:
            print(f"Attempting to fetch tweets from: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                if feed.entries:
                    for entry in feed.entries[:limit]:
                        title = entry.get('title', 'Tweet').split('\n')[0][:100]
                        if len(entry.get('title', '')) > 100:
                            title += "..."
                        link = entry.get('link', '#')
                        published = time.strftime('%Y-%m-%d', entry['published_parsed']) if 'published_parsed' in entry else "recent"
                        tweets.append(f"- [{title}]({link}) ({published})")
                    if tweets:
                        print(f"Successfully fetched {len(tweets)} tweets from {url}")
                        break
            else:
                print(f"Failed to fetch from {url}: Status {response.status_code}")
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            continue
    return tweets

def main():
    # Feeds
    substack = "https://chessman7.substack.com/feed"
    medium = "https://medium.com/feed/@mohitmishra786687"
    coredump = "https://mohitmishra786.github.io/TheCoreDump/feed.xml"
    
    all_posts = []
    all_posts.extend(fetch_rss_posts(substack, limit=3))
    all_posts.extend(fetch_rss_posts(medium, limit=3))
    all_posts.extend(fetch_rss_posts(coredump, limit=3))
    
    # Twitter
    tweets = fetch_twitter_posts("chessMan786", limit=3)
    
    readme = open_readme()
    
    if all_posts:
        # Sort or just join (they are already grouped by source)
        blog_text = "\n".join(all_posts)
        readme = modify_readme(readme, blog_text, identifier='BLOG')
        
    if tweets:
        tweet_text = "\n".join(tweets)
        readme = modify_readme(readme, tweet_text, identifier='TWITTER')
        
    write_readme(readme)

if __name__ == '__main__':
    main()

import feedparser
import time
import re
from os import path


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
    start_tag = f'{identifier}_START'
    end_tag = f'{identifier}_END'
    return re.sub(f'(?<=<!-- {start_tag} -->).*?(?=<!-- {end_tag} -->)', text, readme, flags=re.DOTALL)


def list_featured_posts(feed):
    """
    List the featured posts from the RSS feed.
    """
    posts = []
    feed = feedparser.parse(feed)
    for entry in feed.entries:
        # Check if the post is featured
        featured = entry.get('featured', 'no')
        if featured != 'yes':
            continue
        title = entry['title']
        link = entry['link']
        published = time.strftime('%Y-%m-%d', entry['published_parsed'])
        posts.append(f"- [{title}]({link}) ({published})")
    return '\n' + '\n'.join(posts) + '\n'


def main():
    posts = list_featured_posts("http://medium.com/feed/@mohitmishra786687")
    original = open_readme()
    updated = modify_readme(original, posts, identifier='BLOG')
    write_readme(updated)


if __name__ == '__main__':
    main()

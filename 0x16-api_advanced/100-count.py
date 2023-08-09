#!/usr/bin/python3
""" raddit api"""

import requests

def count_words(subreddit, word_list, after=None, count=None):
    if count is None:
        count = {word.lower(): 0 for word in word_list}
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 100}
    if after:
        params['after'] = after
    
    headers = {'User-Agent': 'bhalut'}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        topics = data['data']['children']
        
        for topic in topics:
            title_words = topic['data']['title'].lower().split()
            for word in title_words:
                if word in count:
                    count[word] += 1
        
        after = data['data']['after']
        if not after:
            sorted_words = sorted(count.keys(), key=lambda w: (-count[w], w))
            
            for word in sorted_words:
                if count[word] > 0:
                    print(f"{word}: {count[word]}")
        else:
            count_words(subreddit, word_list, after, count)
    else:
        print(f"Error: {response.status_code}")

# Example usage
count_words('python', ['python', 'java', 'ruby', 'javascript'])

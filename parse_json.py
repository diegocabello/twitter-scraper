import json
import sqlite3
import requests
import os

if not os.path.exists("images"):
    os.makedirs("images")

connection = sqlite3.connect('data2.db')
cursor = connection.cursor()

def get_nested_value(data, keys):
    for key in keys:
        if key in data:
            data = data[key]
        else:
            return None
    return data

post_template_data = {
    "post_rest_id": ["rest_id"],
    "post_author_rest_id": ["core", "user_results", "result", "rest_id"],
    "post_author_name": ["core", "user_results", "result", "legacy", "name"],
    "post_author_screen_name": ["core", "user_results", "result", "legacy", "screen_name"],
    "post_author_affiliates": ["core", "user_results", "result", "affiliates_highlighted_label"],
    "post_author_banner_url": ["core", "user_results", "result", "legacy", "profile_banner_url"],
    "post_author_countries_withheld": ["core", "user_results", "result", "legacy", "withheld_in_countries"],
    "post_author_description": ["core", "user_results", "result", "legacy", "description"],
    "post_author_followers": ["core", "user_results", "result", "legacy", "followers_count"],
    "post_author_friends_count": ["core", "user_results", "result", "legacy", "friends_count"],
    "post_author_joined_at": ["core", "user_results", "result", "legacy", "created_at"],
    "post_author_likes_count": ["core", "user_results", "result", "legacy", "favourites_count"],
    "post_author_location": ["core", "user_results", "result", "legacy", "location"],
    "post_author_media_count": ["core", "user_results", "result", "legacy", "media_count"],
    "post_author_pfp_url": ["core", "user_results", "result", "legacy", "profile_image_url_https"],
    "post_author_pfp_shape": ["core", "user_results", "result", "profile_image_shape"],
    "post_author_pinned": ["core", "user_results", "result", "legacy", "pinned_tweet_ids_str"],
    "post_author_posts_count": ["core", "user_results", "result", "legacy", "statuses_count"],
    "post_author_verified": ["core", "user_results", "result", "legacy", "verified"],

    "post_bookmarks": ["legacy", "bookmark_count"],
    "post_created_at": ["legacy", "created_at"],
    "post_is_quote": ["legacy", "is_quote_status"],
    "post_likes": ["legacy", "favorite_count"],
    "post_replies": ["legacy", "reply_count"],
    "post_retweets": ["legacy", "retweet_count"],
    "post_text_content": ["legacy", "full_text"],
    "post_times_quoted": ["legacy", "quote_count"],
    "post_views": ["views", "count"], 

    "post_media_id_str": ["legacy", "entities", "media", "id_str"],
    "post_media_url_https": ["legacy", "entities", "media", "media_url_https"],
    "post_media_type": ["legacy", "entities", "media", "type"],
    "post_media_availability": ["legacy", "entities", "media", "ext_media_availability"],
}

cursor.execute('''CREATE TABLE IF NOT EXISTS media (
            id_str TEXT PRIMARY KEY,
            url_https TEXT,
            type TEXT,
            availability INT
            )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            author INTEGER,
            bookmarks INTEGER,
            created_at TEXT,
            is_quote INTEGER,
            likes INTEGER, 
            replies INTEGER, 
            retweets INTEGER, 
            text_content TEXT,
            times_quoted INTEGER,
            views INTEGER
            )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT,
            screenname TEXT,
            affiliates TEXT,
            banner_url TEXT,
            countries_withheld TEXT,
            description TEXT, 
            followers INTEGER,
            friends INTEGER,
            joined_at TEXT, 
            likes_count INTEGER,
            location TEXT, 
            media_count INTEGER,
            pfp_url TEXT,
            pfp_shape TEXT,
            posts_count INTEGER,
            verified INTEGER
            )''')


def save(inx):

    post_data = {}

    for key, path in post_template_data.items():
        try:
            post_data[key] = get_nested_value(inx, path)
        except KeyError:
            post_data[key] = None

    cursor.execute('''
        INSERT OR REPLACE INTO authors (
            id, name, screenname, affiliates, banner_url, 
            countries_withheld, description, followers, friends, 
            joined_at, likes_count, location, media_count, pfp_url, 
            pfp_shape, posts_count, verified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        post_data["post_author_rest_id"], post_data["post_author_name"],
        post_data["post_author_screen_name"],
        json.dumps(post_data["post_author_affiliates"]),
        post_data["post_author_banner_url"],
        json.dumps(post_data["post_author_countries_withheld"]),
        post_data["post_author_description"],
        post_data["post_author_followers"],
        post_data["post_author_friends_count"],
        post_data["post_author_joined_at"],
        post_data["post_author_likes_count"],
        post_data["post_author_location"],
        post_data["post_author_media_count"],
        post_data["post_author_pfp_url"],
        post_data["post_author_pfp_shape"],
        post_data["post_author_posts_count"],
        post_data["post_author_verified"]
    ))

    cursor.execute('''
        INSERT OR REPLACE INTO posts (
            id, author, bookmarks, created_at, is_quote, likes, 
            replies, retweets, text_content, times_quoted, views
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        post_data["post_rest_id"], post_data["post_author_rest_id"],
        post_data["post_bookmarks"], post_data["post_created_at"],
        post_data["post_is_quote"], post_data["post_likes"],
        post_data["post_replies"], post_data["post_retweets"],
        post_data["post_text_content"], post_data["post_times_quoted"],
        post_data["post_views"]
    ))

    media = get_nested_value(inx, ("legacy", "entities", "media"))
    if media: 
        for m in media: #(inx["legacy"]["entities"]["media"]):
            #print('\n\n-----------------------\n')
            #print(json.dumps(m, indent=2))
            try:
                cursor.execute('INSERT INTO media ( id_str, url_https, type, availability ) VALUES ( ?, ?, ?, ? )', (m["id_str"], m["type"], m["media_url_https"], m["ext_media_availability"]["status"]))
            except sqlite3.IntegrityError as e:
                print(f'dupe: {e}')

            response = requests.get(m["media_url_https"])
            if response.status_code == 200:
                with open(os.path.join("images", f"{m['id_str']}.png"), "wb") as file:
                    file.write(response.content)
                print(f"Image {m['id_str']}.png from post {post_data["post_rest_id"]} downloaded successfully.")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")



with open(os.path.join('outputs', 'skibidi15.txt')) as file:

    post_count = 0
    for count, line in enumerate(file):
        # if count > 5:
        #     break 
            
        print(count)
        data = json.loads(line)
        usable_data = data["data"]["bookmark_timeline_v2"]["timeline"]["instructions"][0]["entries"]

        for post in usable_data[:20]:
            post_count += 1
            skip = post["content"]["itemContent"]["tweet_results"]["result"]

            try:
                save(skip["tweet"]["core"]["user_results"]["result"])
                print('did a differently structured one')
            except KeyError:
                try:
                    save(skip)
                except KeyError as e:
                    print(e)

            if post_count == 20:
                connection.commit()
                post_count = 0

connection.commit()
connection.close()

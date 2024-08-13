import sqlite3
from datetime import datetime, timedelta

class TwitterDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY,
                upload_date TIMESTAMP,
                post_id TEXT,
                author_id INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT,
                author_id INTEGER,
                post_date TIMESTAMP,
                edit_timestamp TIMESTAMP,
                likes INTEGER,
                reposts INTEGER,
                replies INTEGER,
                bookmarks INTEGER,
                views INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER,
                timestamp TIMESTAMP,
                username TEXT,
                handle TEXT,
                follower_count INTEGER,
                post_count INTEGER,
                following_count INTEGER,
                bio TEXT,
                subscription_count INTEGER,
                verification_status BOOLEAN,
                corporation_affiliation BOOLEAN
            )
        ''')

        self.conn.commit()

    def add_image(self, upload_date, post_id, author_id):
        self.cursor.execute('''
            INSERT INTO images (upload_date, post_id, author_id)
            VALUES (?, ?, ?)
        ''', (upload_date, post_id, author_id))
        self.conn.commit()

    def add_post(self, post_id, author_id, post_date, edit_timestamp, likes, reposts, replies, bookmarks, views):
        self.cursor.execute('''
            INSERT INTO posts (post_id, author_id, post_date, edit_timestamp, likes, reposts, replies, bookmarks, views)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (post_id, author_id, post_date, edit_timestamp, likes, reposts, replies, bookmarks, views))
        self.conn.commit()

    def update_author(self, author_id, username, handle, follower_count, post_count, following_count, bio, subscription_count, verification_status, corporation_affiliation):
        # Check if author was updated in the last 5 minutes
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        self.cursor.execute('''
            SELECT * FROM authors
            WHERE author_id = ? AND timestamp > ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (author_id, five_minutes_ago))
        recent_record = self.cursor.fetchone()

        if recent_record:
            return  # Don't update if there's a recent record

        # Get the most recent record for this author
        self.cursor.execute('''
            SELECT * FROM authors
            WHERE author_id = ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (author_id,))
        last_record = self.cursor.fetchone()

        # Prepare new record, using None for unchanged fields
        new_record = [
            author_id,
            datetime.now(),
            username if not last_record or username != last_record[2] else None,
            handle if not last_record or handle != last_record[3] else None,
            follower_count if not last_record or follower_count != last_record[4] else None,
            post_count if not last_record or post_count != last_record[5] else None,
            following_count if not last_record or following_count != last_record[6] else None,
            bio if not last_record or bio != last_record[7] else None,
            subscription_count if not last_record or subscription_count != last_record[8] else None,
            verification_status if not last_record or verification_status != last_record[9] else None,
            corporation_affiliation if not last_record or corporation_affiliation != last_record[10] else None
        ]

        self.cursor.execute('''
            INSERT INTO authors (author_id, timestamp, username, handle, follower_count, post_count, following_count, bio, subscription_count, verification_status, corporation_affiliation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', new_record)
        self.conn.commit()

    def close(self):
        self.conn.close()
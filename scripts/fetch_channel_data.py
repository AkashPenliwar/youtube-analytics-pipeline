from dotenv import load_dotenv
import os
import requests
import psycopg2
import json
from db_connect import connect_to_postgres

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

import requests
import psycopg2

# === YOUR API KEY ===
API_KEY = "AIzaSyDOpKUhkFtn1Ngtn7dxAimVy528NRHCAy0"

# === CHANNEL ID to track (example: TechBurner) ===
channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Replace this with any channel ID

# === YouTube API endpoint ===
url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"

response = requests.get(url)
data = response.json()

if "items" not in data:
    print(" No data found. Check your channel ID or API key.")
    exit()

channel = data["items"][0]
channel_info = {
    "channel_id": channel["id"],
    "title": channel["snippet"]["title"],
    "published_at": channel["snippet"]["publishedAt"],
    "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
    "view_count": int(channel["statistics"].get("viewCount", 0)),
    "video_count": int(channel["statistics"].get("videoCount", 0))
}

print(" Fetched channel info:", channel_info)

# === Store in PostgreSQL ===
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="youtube_analytics",
        user="postgres",
        password="Akash1812"  # replace with your PostgreSQL password
    )
    cursor = conn.cursor()

    # INSERT or UPDATE
    cursor.execute("""
        INSERT INTO channel_info (channel_id, title, published_at, subscriber_count, view_count, video_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (channel_id) DO UPDATE SET
            title = EXCLUDED.title,
            published_at = EXCLUDED.published_at,
            subscriber_count = EXCLUDED.subscriber_count,
            view_count = EXCLUDED.view_count,
            video_count = EXCLUDED.video_count;
    """, (
        channel_info["channel_id"],
        channel_info["title"],
        channel_info["published_at"],
        channel_info["subscriber_count"],
        channel_info["view_count"],
        channel_info["video_count"]
    ))

    conn.commit()
    print(" Channel data inserted/updated in PostgreSQL.")

    cursor.close()
    conn.close()

except Exception as e:
    print(" Database error:", e)

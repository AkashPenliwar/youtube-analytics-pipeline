import requests
import psycopg2

API_KEY = "AIzaSyDOpKUhkFtn1Ngtn7dxAimVy528NRHCAy0"
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Example channel

# ✅ Step 1: Get the channel title
channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={CHANNEL_ID}&key={API_KEY}"
channel_response = requests.get(channel_url).json()

if "items" not in channel_response or not channel_response["items"]:
    print(" Could not fetch channel details.")
    exit()

channel_title = channel_response["items"][0]["snippet"]["title"]
print(f" Channel Title: {channel_title}")

# Step 2: Fetch videos from the channel
search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=10"
search_response = requests.get(search_url)
search_data = search_response.json()

video_stats = []

if "items" not in search_data:
    print(" No videos found.")
    exit()

for item in search_data["items"]:
    if item["id"]["kind"] == "youtube#video":
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        published_at = item["snippet"]["publishedAt"]

        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
        stats_response = requests.get(stats_url)
        stats_data = stats_response.json()

        if "items" in stats_data and len(stats_data["items"]) > 0:
            stats = stats_data["items"][0]["statistics"]
            view_count = int(stats.get("viewCount", 0))
            like_count = int(stats.get("likeCount", 0))
            comment_count = int(stats.get("commentCount", 0))

            video_entry = {
                "video_id": video_id,
                "channel_id": CHANNEL_ID,
                "channel_title": channel_title,
                "title": video_title,
                "published_at": published_at,
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count
            }

            # ✅ Print for debugging
            print("⬇ Inserting video:")
            print(video_entry)
            video_stats.append(video_entry)

# ✅ Step 3: Insert video data into PostgreSQL
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="youtube_analytics",
        user="postgres",
        password="Akash1812"
    )
    cursor = conn.cursor()

    for video in video_stats:
        cursor.execute("""
            INSERT INTO video_stats (
                video_id, channel_id, channel_title, title, published_at,
                view_count, like_count, comment_count
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO UPDATE SET
                channel_title = EXCLUDED.channel_title,
                title = EXCLUDED.title,
                published_at = EXCLUDED.published_at,
                view_count = EXCLUDED.view_count,
                like_count = EXCLUDED.like_count,
                comment_count = EXCLUDED.comment_count;
        """, (
            video["video_id"],
            video["channel_id"],
            video["channel_title"],
            video["title"],
            video["published_at"],
            video["view_count"],
            video["like_count"],
            video["comment_count"]
        ))

    conn.commit()
    print(" Video stats inserted/updated in PostgreSQL.")

    cursor.close()
    conn.close()

except Exception as e:
    print(" Database error:", e)

#  YouTube Analytics Data Pipeline
"A YouTube Analytics Platform built from scratch using Python, PostgreSQL, and Streamlit – engineered for insights, optimized for scale."

This project is a complete **Data Engineering + Analysis pipeline** that fetches YouTube channel and video data using the YouTube Data API, stores it in PostgreSQL, and visualizes it using a Streamlit dashboard.

---

##  Features

- Fetch channel and video stats from YouTube API
- Store structured data in PostgreSQL
- Streamlit dashboard for:
  - Channel filters
  - View/like/comment filters
  - Keyword search
  - Date range filtering
  -  Download CSV feature

---

##  Project Structure
youtube analytics pipeline/
├── scripts/
│ ├── db_connect.py
│ ├── fetch_channel_data.py
│ └── fetch_video_stats.py
├── app.py
├── .env # API key (not uploaded)
├── .gitignore
└── README.md

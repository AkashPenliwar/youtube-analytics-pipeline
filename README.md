# 📊 YouTube Analytics Dashboard

An interactive and powerful analytics dashboard built with **Streamlit**, **PostgreSQL**, and **Plotly** to visualize and explore YouTube channel data like views, likes, comments, and publishing trends.

> 🚀 Built by Akash Penliwar

---

## 📌 Project Overview

This YouTube Analytics Dashboard enables users to:
- Input **any YouTube Channel ID**
- Analyze the **latest 50 videos**
- Apply **real-time filters** and generate **visual insights**
- Download the filtered dataset as CSV

It fetches the video stats from a PostgreSQL database (populated from the YouTube API) and provides an intuitive interface for creators, marketers, and analysts.

---

## ✨ Features

- 🔄 **Multi-channel input:** Analyze any channel by pasting its Channel ID
- 🔍 **Filters:**
  - Search by **keywords** in video titles
  - Set a **minimum view count**
  - Choose a **date range** for published videos
- 📈 **Visualizations** (using Plotly):
  - Top 10 most viewed videos (bar chart)
  - View count over time (line chart)
  - Likes vs. Comments (scatter plot)
- 💾 **Export** filtered video stats as CSV
- 📱 **Responsive UI** using Streamlit’s wide layout

---

## 🧱 Tech Stack

| Component       | Tool/Framework        |
|-----------------|-----------------------|
| Frontend        | Streamlit             |
| Backend         | Python, psycopg2      |
| Database        | PostgreSQL            |
| Visualization   | Plotly, Matplotlib    |
| Data Handling   | Pandas                |

---

## 🚀 Getting Started

### ⚙️ Prerequisites

- Python 3.8+
- PostgreSQL database with video data
- YouTube Data inserted into a table named `video_stats` with at least:
  - `title`, `view_count`, `like_count`, `comment_count`, `published_at`, `channel_id`

---

### 🔧 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/youtube-analytics-pipeline.git
   cd youtube-analytics-pipeline

Install dependencies:
pip install -r requirements.txt

Update your PostgreSQL credentials in app.py:
DB_NAME = "your_db"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

Run the app:
streamlit run app.py

Folder Structure
youtube-analytics-pipeline/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Files to ignore in version control
└── assets/                 # (Optional) Images for README


Sample Query Used:
SELECT title, view_count, like_count, comment_count, published_at
FROM video_stats
WHERE channel_id = %s
ORDER BY published_at DESC
LIMIT 50;

Future Enhancements
 YouTube API integration to automate data fetching

 Add sentiment analysis on comments

 Compare two or more channels side-by-side

 Deploy on cloud (e.g., Streamlit Cloud or Render)


 Author
Akash Penliwar
LinkedIn: linkedin.com/in/akash-penliwar
GitHub: github.com/akashpenliwar
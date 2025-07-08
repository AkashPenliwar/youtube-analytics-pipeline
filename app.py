import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# PostgreSQL connection details
DB_NAME = "youtube_analytics"
DB_USER = "postgres"
DB_PASSWORD = "Akash1812"
DB_HOST = "localhost"
DB_PORT = "5432"

st.set_page_config(layout="wide")
st.title(" YouTube Analytics Dashboard")

# Fetch data from PostgreSQL
def fetch_data(channel_id):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        query = """
            SELECT title, view_count, like_count, comment_count, published_at
            FROM video_stats
            WHERE channel_id = %s
            ORDER BY published_at DESC
            LIMIT 50;
        """
        df = pd.read_sql_query(query, conn, params=(channel_id,))
        conn.close()
        return df
    except Exception as e:
        st.error(f" Error: {e}")
        return pd.DataFrame()

# --- Sidebar Filters ---
st.sidebar.header(" Filters")
channel_id = st.sidebar.text_input("Enter YouTube Channel ID", value="UC_x5XG1OV2P6uZZ5FSM9Ttw")

if channel_id:
    df = fetch_data(channel_id)

    if not df.empty:
        df["published_at"] = pd.to_datetime(df["published_at"])

        keyword = st.sidebar.text_input(" Search in Title", "")
        min_views = st.sidebar.slider(" Minimum Views", 0, int(df["view_count"].max()), 0)

        date_range = st.sidebar.date_input(
            " Published Between",
            [df["published_at"].min().date(), df["published_at"].max().date()]
        )

        # Apply all filters
        filtered_df = df[
            df["title"].str.contains(keyword, case=False, na=False) &
            (df["view_count"] >= min_views) &
            df["published_at"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
        ]

        st.subheader(" Filtered Video Data")
        st.dataframe(filtered_df)

        # --- Plotly Visualizations ---
        st.subheader(" Visual Insights")

        # 1. Top 10 videos by view count
        top_videos = filtered_df.sort_values(by="view_count", ascending=False).head(10)
        fig1 = px.bar(
            top_videos,
            x="view_count",
            y="title",
            orientation="h",
            title=" Top 10 Most Viewed Videos",
            labels={"view_count": "Views", "title": "Video Title"},
            color="view_count",
            color_continuous_scale="blues"
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Views over time
        fig2 = px.line(
            filtered_df.sort_values("published_at"),
            x="published_at",
            y="view_count",
            title=" Views Over Time",
            labels={"published_at": "Published Date", "view_count": "Views"},
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 3. Likes vs Comments scatter
        fig3 = px.scatter(
            filtered_df,
            x="like_count",
            y="comment_count",
            hover_name="title",
            title=" Likes vs Comments",
            labels={"like_count": "Likes", "comment_count": "Comments"},
            color="view_count",
            size="view_count",
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # --- Download as CSV ---
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download as CSV",
            data=csv,
            file_name="youtube_filtered_data.csv",
            mime="text/csv"
        )

    else:
        st.warning(" No data found for the provided Channel ID.")

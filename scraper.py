import pandas as pd
from googleapiclient.discovery import build
import os
import time

API_KEY = "AIzaSyCFLntjIYVr6jijthBc9938MqCjCzWbV-0"
youtube = build('youtube', 'v3', developerKey=API_KEY)

# === FUNGSI: cari video berdasarkan kata kunci ===
def search_videos(query, max_results=50):
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=max_results,
        type="video",
        order="relevance"
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        videos.append({'video_id': video_id, 'title': title, 'query': query})
    return videos

# === FUNGSI: ambil komentar dari satu video ===
def get_comments(video_id, max_results=500):
    comments = []
    next_page_token = None

    while len(comments) < max_results:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': snippet['authorDisplayName'],
                'comment': snippet['textDisplay'],
                'likes': snippet['likeCount'],
                'publishedAt': snippet['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

        time.sleep(1)

    return pd.DataFrame(comments[:max_results])

# === MAIN ===
queries = ["tunjangan DPR", "gaji DPR"]
all_comments = []

for q in queries:
    print(f"Mencari video untuk kata kunci: '{q}'...")
    videos = search_videos(q, max_results=50)

    for idx, vid in enumerate(videos, start=1):
        video_id = vid['video_id']
        title = vid['title'].replace('/', '_').replace('\\', '_')
        print(f"[{q}] ({idx}/{len(videos)}) Mengambil komentar dari: {title}")

        try:
            df = get_comments(video_id, max_results=500)
            df["video_title"] = title
            df["query"] = q
            all_comments.append(df)
            print(f"✔ {len(df)} komentar berhasil diambil")
        except Exception as e:
            print(f"⚠ Gagal mengambil komentar: {e}")

        time.sleep(2)

# === Gabungkan semua komentar ===
if all_comments:
    df_all = pd.concat(all_comments, ignore_index=True)
    output_path = "all_comments.csv"
    df_all.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ Semua komentar digabung dan disimpan ke: {output_path}")
    print(f"Total komentar: {len(df_all)}")
else:
    print("❌ Tidak ada komentar yang berhasil diambil.")

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Baca hasil analisis sentimen
df = pd.read_csv("sentiment_comments.csv")

# Bersihkan data dari error / NaN
df = df.dropna(subset=["clean_comment", "sentiment"])  # hapus baris yang kosong
df = df[df["clean_comment"].str.strip() != ""]          # hapus komentar kosong

# Pastikan folder hasil visualisasi ada
os.makedirs("visualisasi_sentimen", exist_ok=True)

# Hitung jumlah setiap sentimen
sentiment_counts = df["sentiment"].value_counts()

# Pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=['lightcoral', 'gold', 'lightgreen']
)
plt.title("Distribusi Sentimen Komentar YouTube")
plt.tight_layout()
plt.savefig("visualisasi_sentimen/pie_chart_sentimen.png", dpi=300)
plt.close()

# Bar chart
plt.figure(figsize=(7, 4))
sentiment_counts.plot(kind='bar', color=['lightcoral', 'gold', 'lightgreen'])
plt.title("Jumlah Komentar per Sentimen")
plt.xlabel("Sentimen")
plt.ylabel("Jumlah Komentar")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("visualisasi_sentimen/bar_chart_sentimen.png", dpi=300)
plt.close()

# Fungsi buat WordCloud per sentimen
def generate_wordcloud(sentiment_label, data):
    subset = data[data["sentiment"] == sentiment_label]
    text = " ".join(subset["clean_comment"].astype(str))
    if not text.strip():
        print(f"⚠ Tidak ada teks valid untuk sentimen '{sentiment_label}', dilewati.")
        return
    wc = WordCloud(width=900, height=450, background_color="white", collocations=False).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"WordCloud - {sentiment_label.capitalize()} Comments")
    plt.tight_layout()
    file_path = f"visualisasi_sentimen/wordcloud_{sentiment_label.lower()}.png"
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"✔ WordCloud {sentiment_label} disimpan di {file_path}")

# WordCloud per kategori sentimen
for s in df["sentiment"].unique():
    generate_wordcloud(s, df)

# WordCloud keseluruhan
all_text = " ".join(df["clean_comment"].astype(str))
if all_text.strip():
    wc_all = WordCloud(width=1000, height=500, background_color="white", collocations=False).generate(all_text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc_all, interpolation="bilinear")
    plt.axis("off")
    plt.title("WordCloud - Semua Komentar")
    plt.tight_layout()
    plt.savefig("visualisasi_sentimen/wordcloud_all.png", dpi=300)
    plt.close()
    print("✔ WordCloud keseluruhan disimpan di visualisasi_sentimen/wordcloud_all.png")
else:
    print("Tidak ada teks valid untuk membuat WordCloud keseluruhan.")

print("Semua visualisasi selesai dibuat dan disimpan di folder 'visualisasi_sentimen'!")
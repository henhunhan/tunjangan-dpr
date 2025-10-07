import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# === SETUP DASAR ===
st.set_page_config(page_title="Dashboard Analisis Sentimen", layout="wide")

st.title("📊 Dashboard Analisis Sentimen YouTube tentang DPR")

# === LOAD DATA ===
try:
    df = pd.read_csv("sentiment_comments.csv")
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()

# Pastikan kolom sentiment dan komentar ada
required_cols = ["sentiment"]
if not any(c in df.columns for c in ["clean_comment", "comment"]):
    st.warning("Kolom teks komentar tidak ditemukan. Visualisasi teks akan dilewati.")
    text_col = None
else:
    text_col = "clean_comment" if "clean_comment" in df.columns else "comment"

if "sentiment" not in df.columns:
    st.error("Kolom 'sentiment' tidak ditemukan dalam file CSV.")
    st.stop()

# Normalisasi label sentimen
df["sentiment"] = df["sentiment"].astype(str).str.lower().replace({
    "positive": "positif",
    "negative": "negatif",
    "neutral": "netral"
})

# Hapus baris kosong
df = df.dropna(subset=["sentiment"])
df = df[df["sentiment"].isin(["positif", "negatif", "netral"])]

if df.empty:
    st.warning("Tidak ada data sentimen yang valid untuk divisualisasikan.")
else:
    # === STATISTIK DASAR ===
    total_data = len(df)
    count_pos = len(df[df["sentiment"] == "positif"])
    count_neg = len(df[df["sentiment"] == "negatif"])
    count_net = len(df[df["sentiment"] == "netral"])

    st.markdown("### 🔍 Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Data", total_data)
    col2.metric("Positif", count_pos, f"{(count_pos/total_data*100):.1f}%" if total_data else "0%")
    col3.metric("Negatif", count_neg, f"{(count_neg/total_data*100):.1f}%" if total_data else "0%")
    col4.metric("Netral", count_net, f"{(count_net/total_data*100):.1f}%" if total_data else "0%")

    st.divider()

    # === TAB NAVIGASI ===
    tabs = st.tabs(["📈 Visualisasi Sentimen", "☁️ Word Cloud", "📊 Analisis Tren", "🔎 Analisis Mendalam", "📄 Data Explorer"])

    # === TAB 1: VISUALISASI SENTIMEN ===
    with tabs[0]:
        st.subheader("Distribusi Sentimen")

        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 4))
            df["sentiment"].value_counts().plot.pie(
                autopct="%1.1f%%",
                colors=["green", "red", "gray"],
                ax=ax1,
                textprops={"fontsize": 8}
            )
            ax1.set_ylabel("")
            ax1.set_title("Persentase Sentimen", fontsize=10)
            st.pyplot(fig1, use_container_width=True)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            df["sentiment"].value_counts().plot(
                kind="bar",
                color=["green", "red", "gray"],
                ax=ax2
            )
            ax2.set_title("Jumlah Komentar per Sentimen", fontsize=10)
            ax2.set_xlabel("")
            ax2.set_ylabel("Jumlah", fontsize=9)
            st.pyplot(fig2, use_container_width=True)



# === TAB 2: WORD CLOUD ===
with tabs[1]:
    st.subheader("Word Cloud Berdasarkan Sentimen")

    sentiments = ["positif", "negatif", "netral"]
    for s in sentiments:
        st.markdown(f"#### 💬 {s.capitalize()}")
        text = " ".join(df[df["sentiment"] == s][text_col].astype(str))
        if not text.strip():
            st.warning(f"Tidak ada data untuk sentimen {s}")
            continue
        wc = WordCloud(width=800, height=400, background_color="white").generate(text)
        st.image(wc.to_array(), use_container_width=True)

    st.markdown("### ☁️ Word Cloud Keseluruhan")
    all_text = " ".join(df[text_col].astype(str))
    wc_all = WordCloud(width=900, height=500, background_color="black", colormap="viridis").generate(all_text)
    st.image(wc_all.to_array(), use_container_width=True)

# === TAB 3: ANALISIS TREN (opsional, kalau ada tanggal)
with tabs[2]:
    if "publishedAt" in df.columns:
        df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
        df["date"] = df["publishedAt"].dt.date
        daily = df.groupby(["date", "sentiment"]).size().unstack(fill_value=0)
        st.line_chart(daily)
    else:
        st.info("Kolom tanggal tidak tersedia di data.")

# === TAB 4: ANALISIS MENDALAM ===
# === TAB 4: ANALISIS MENDALAM ===
with tabs[3]:
    st.subheader("🔎 Analisis Sentimen Mendalam")

    # === TOP KATA PER SENTIMEN ===
    if text_col:
        st.markdown("### 🔠 Kata yang Paling Sering Muncul per Sentimen")

        from collections import Counter
        import re

        def top_words(df_sentiment, n=10):
            text = " ".join(df_sentiment[text_col].astype(str))
            words = re.findall(r"\b[a-zA-Záéíóúüñ]+(?:'\w+)?\b", text.lower())
            counter = Counter(words)
            common = counter.most_common(n)
            return pd.DataFrame(common, columns=["Kata", "Frekuensi"])

        for s in ["positif", "negatif", "netral"]:
            st.markdown(f"#### 💬 {s.capitalize()}")
            subdf = df[df["sentiment"] == s]
            if len(subdf) == 0:
                st.info(f"Tidak ada komentar {s}.")
                continue
            freq_df = top_words(subdf)
            st.dataframe(freq_df, use_container_width=True)

    else:
        st.warning("Kolom teks komentar tidak tersedia untuk analisis mendalam.")

    st.divider()

    # === DISTRIBUSI LIKE PER SENTIMEN ===
    if "likes" in df.columns:
        st.markdown("### 📊 Rata-rata Like per Sentimen")
        avg_like = df.groupby("sentiment")["likes"].mean().reset_index()
        st.bar_chart(avg_like, x="sentiment", y="likes", color="#1f77b4")
    else:
        st.info("Kolom 'likes' tidak tersedia untuk analisis kuantitatif.")

# === TAB 5: DATA EXPLORER ===
with tabs[4]:
    st.subheader("📄 Data Explorer")

    # Hapus kolom tidak relevan
    drop_cols = ["confidence", "publishedAt", "likes"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    # Pastikan kolom teks yang dipakai
    text_col = "clean_comment" if "clean_comment" in df.columns else "comment"

    # Bersihkan teks agar ada spasi yang rapi
    df[text_col] = df[text_col].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

    # === Filter Sentimen ===
    st.markdown("### 🎯 Filter Data")
    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input("🔍 Cari komentar", "")
    with col2:
        sentiment_filter = st.selectbox(
            "Filter Sentimen",
            ["Semua", "positif", "negatif", "netral"]
        )

    # === Terapkan filter ===
    filtered_df = df.copy()

    # Filter teks berdasarkan pencarian
    if search_query:
        filtered_df = filtered_df[
            filtered_df[text_col].str.contains(search_query, case=False, na=False)
        ]

    # Filter berdasarkan sentimen
    if sentiment_filter != "Semua":
        filtered_df = filtered_df[filtered_df["sentiment"] == sentiment_filter]

    # Tampilkan hasil
    st.markdown(f"Menampilkan **{len(filtered_df)}** dari **{len(df)}** total data.")
    st.dataframe(filtered_df, use_container_width=True)


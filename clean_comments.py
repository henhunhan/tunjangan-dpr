import pandas as pd
import re

# Baca hasil gabungan
df = pd.read_csv("all_comments.csv")

# Fungsi untuk menghapus emoji
def remove_emoji(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emotikon wajah
        u"\U0001F300-\U0001F5FF"  # simbol & pictographs
        u"\U0001F680-\U0001F6FF"  # transportasi & simbol
        u"\U0001F1E0-\U0001F1FF"  # bendera (iOS)
        u"\U00002700-\U000027BF"  # simbol tambahan
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Fungsi utama pembersihan teks
def clean_text(text):
    text = str(text).lower()
    text = remove_emoji(text)                           # hapus emoji
    text = re.sub(r"http\S+|www\S+|https\S+", '', text) # hapus link
    text = re.sub(r"[^a-zA-Z\s]", '', text)             # hapus simbol, angka, tanda baca
    text = re.sub(r"\s+", ' ', text).strip()            # hapus spasi ganda
    return text

# Bersihkan komentar dan bentuk DataFrame baru
df_cleaned = pd.DataFrame()
df_cleaned["author"] = df["author"]
df_cleaned["clean_comment"] = df["comment"].apply(clean_text)
df_cleaned["likes"] = df["likes"]
df_cleaned["publishedAt"] = df["publishedAt"]

# Simpan hasilnya
df_cleaned.to_csv("clean_comments.csv", index=False, encoding="utf-8")

print(f"Pembersihan teks selesai! Total {len(df_cleaned)} komentar disimpan ke 'clean_comments.csv'")

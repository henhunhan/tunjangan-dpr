import pandas as pd
import glob

# Gabung semua CSV di folder youtube_comments ===
files = glob.glob("youtube_comments/*.csv")
df_list = [pd.read_csv(f) for f in files]
df = pd.concat(df_list, ignore_index=True)

# Hapus komentar kosong
df.dropna(subset=["comment"], inplace=True)
df = df[df["comment"].str.strip() != ""]

# Simpan hasil gabungan
df.to_csv("all_comments.csv", index=False, encoding="utf-8-sig")

print(f"Gabung selesai! Total komentar: {len(df)} disimpan di 'all_comments.csv'")

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

# Baca hasil cleaning
df = pd.read_csv("clean_comments.csv")

# Load model IndoBERT Sentiment
model_name = "w11wo/indonesian-roberta-base-sentiment-classifier"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    "w11wo/indonesian-roberta-base-sentiment-classifier"
)

# Buat pipeline analisis sentimen
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Prediksi setiap komentar
sentiments = []
confidences = []

for comment in tqdm(df["clean_comment"], desc="Menganalisis Sentimen"):
    try:
        result = sentiment_pipeline(comment[:512])[0]  # batasi max 512 token
        sentiments.append(result["label"].lower())
        confidences.append(round(result["score"], 3))
    except Exception as e:
        sentiments.append("error")
        confidences.append(0)

# Tambahkan hasil ke DataFrame
df["sentiment"] = sentiments
df["confidence"] = confidences

# Simpan ke CSV baru
df.to_csv("sentiment_comments.csv", index=False, encoding="utf-8-sig")

print("Analisis Sentimen selesai!")
print("Hasil disimpan ke 'sentiment_comments.csv'")
print(df["sentiment"].value_counts())
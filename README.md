# 📊 Laporan: Analisis Sentimen Komentar Publik Terhadap Tunjangan dan Gaji DPR di Youtube
Proyek ini bertujuan untuk menganalisis opini pengguna platform Youtube terhadap isu "Tunjangan dan Gaji DPR" yang sempat ramai di Indonesia.\
Output dari project ini adalah opini pengguna platform youtube yang terbagi menjadi sentimen positif, negatif, dan netral.

# 🚀Link Demo Streamlit
## Link : https://tunjangan-dpr-lqivfvn6v8bhkvekdmbdly.streamlit.app/

## 1. Latar Belakang 
Isu Tunjangan dan Gaji DPR menjadi topik hangat yang sering muncul di media sosial, terutama portal berita yang menayangkan berita di platform Youtube.\
Proyek ini bertujuan untuk memahami bagaimana pengguna platform Youtube melihat topik tersebut dan arah opini dari pengguna platform Youtube, apakah opini mereka positif/mendukung, negatif/menolak, atau netral.\
Pemilihan platform Youtube dikarenakan banyak video yang membahas isu tersebut dan juga banyak pengguna yang menonton isu tersebut di platform Youtube.

## 2. Metodologi

### A. Pengambilan data (Data Crawling)
- Pengambilan data dilakukan pada platform Youtube dengan kata kunci
  - `Tunjangan DPR`
  - `Gaji DPR`.
- Pengambilan data dilakukan dengan menggunakan API Youtube yaitu Youtube Data API V3 yang disediakan oleh Google secara resmi.
- crawling data dilakukan pada file
  - `scraper.py`
- Data hasil crawling disimpan dalam format .csv dengan nama
   - `all.comments.csv`
  
### B. Data Preprocessing 
- Data yang sudah di crawling kemudian dilakukan pembersihan seperti menghapus link, menghapus emoji, menghapus tanda baca dan simbol, menghapus spasi ganda dan mengubah teks menjadi lowercase
- preprocessing data dilakukan pada file
  - `clean_comments.py`
- Data yang sudah di preprocessing disimpan pada file
  - `clean.comments.csv`

### C. Analisis Sentimen
- Model yang digunakan adalah `w11wo/indonesian-roberta-base-sentiment-classifier` dari hugging face transformers untuk mengklasifikasikan komentar pengguna platform youtube ke dalam tiga kategori, yaitu positif, negatif dan netral
- Sentiment Analysis dilakukan pada file
  - `sentiment_analysis.py`
- Hasil sentiment analysis disimpan pada file
  - `sentiment_comments.py`
 
### D. Visualisasi 
- Setelah analisis sentimen, hasil sentimen di-visualisasikan dalam bentuk `bar chart`, `pie chart`, dan `workcloud` yang menampilkan kata kata yang paling sering muncul pada masing masing sentimen positif, negatif, netral dan setimen secara umum.
- Visualisasi sentimen dilakukan pada file
  - `sentiment.visualization.py`
- Hasil visualisasi sentimen disimpan pada folder
  - `visualisasi_sentimen`


## 3. User Guide 
1. Pastikan Python sudah terinstall pada device
2. Clone repository ini dengan menggunakan `git clone` ataupun download dalam bentuk .zip
3. Jalankan script `scraper.py` untuk melakukan data crawling pada platform Youtube. Ubah Youtube API sesuai dengan Youtube API yang dimiliki. Jika ingin mengubah search query, bisa langsung diubah pada bagian `queries`
4. Jalankan script `clean_comments.py` untuk membersihkan comment hasil crawling.
5. Jalankan script `sentiment.analysis.py` untuk melakukan sentiment analysis terhadap data yang sudah dibersihkan.
6. Jalankan script `sentiment.visualization.py` untuk visualisasi hasil sentiment analysis. Hasil dapat dilihat pada folder visualisasi sentimen

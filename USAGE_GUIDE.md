# AlphaForge Core — Cara Pakai

AlphaForge punya 2 command utama, dan keduanya dirancang buat dipakai
**berurutan**, bukan pilih salah satu. Analoginya: `scan` itu jaring lebar,
`analyze` itu kaca pembesar.

```
scan (luas, banyak ticker, sinyal cepat)
        ↓
   pilih kandidat yang menarik
        ↓
analyze (dalam, 1 ticker, laporan lengkap)
```

---

## Langkah 1 — `scan` dulu: nemuin kandidat

```bash
python -m alphaforge.main scan data/watchlist.txt
```

**Fungsinya:** nyisir semua ticker di `watchlist.txt` (sekarang isinya 33
saham tema AI/Space/Energy), ngasih tiap satu skor gabungan (financial +
technical + institutional), terus **ranking dari yang paling menonjol**.

**Kenapa dulu ini:** kamu belum tentu tau ticker mana yang lagi "hot" hari
ini. `scan` ngasih kamu titik awal — daftar pendek yang layak dicek lebih
dalam, dari daftar panjang yang belum tentu semuanya menarik.

**Yang perlu diperhatiin dari hasilnya:**
- Ranking teratas (composite score tertinggi)
- Section "New institutional positions" — ticker yang baru aja dilirik
  smart money kuartal ini, biasanya paling worth dicek duluan
- Ticker yang gagal di-fetch (bagian "returned no usable data") — abaikan
  dulu, itu bukan sinyal apa-apa, cuma masalah teknis (typo, delisted, dst)

---

## Langkah 2 — `analyze` buat kandidat yang menarik

Dari hasil `scan`, ambil 2-5 ticker teratas (atau yang paling narik
perhatian kamu), lalu dalami satu-satu:

```bash
python -m alphaforge.main analyze nvda
python -m alphaforge.main analyze rklb
python -m alphaforge.main analyze oklo
```

**Fungsinya:** laporan lengkap 1 ticker — quote, financial snapshot,
financial score dengan alasan per kriteria, technical analysis, dan
institutional ownership detail (fund mana pegang berapa, naik/turun berapa
persen), plus berita terbaru.

**Kenapa belakangan:** `analyze` jauh lebih detail tapi juga lebih lambat
(karena hit SEC EDGAR + Yahoo Finance lebih dalam per ticker). Nggak
efisien kalau dipakai buat 33 ticker sekaligus — makanya `scan` yang
nyaring dulu, `analyze` yang mendalami hasil saringannya.

---

## Kapan pakai yang mana aja (tanpa keduanya berurutan)

**Cuma `analyze` aja** — kalau kamu **udah tau** ticker yang mau dicek
(misal abis baca berita, atau ada rekomendasi dari luar). Nggak perlu
`scan` dulu kalau targetnya udah jelas.

**Cuma `scan` aja** — kalau kamu cuma mau liat gambaran cepat/ranking
semua watchlist tanpa perlu detail penuh tiap ticker. Cocok buat cek rutin
mingguan/bulanan, liat ada perubahan menonjol apa nggak dari watchlist
kamu.

---

## Alur lengkap contoh nyata

```bash
# 1. Scan seluruh watchlist, lihat siapa yang menonjol
python -m alphaforge.main scan data/watchlist.txt

# Hasilnya misal nunjukin NVDA, OKLO, RKLB di posisi atas,
# dan OKLO punya 3 fund baru masuk kuartal ini — menarik.

# 2. Dalami satu-satu yang menarik
python -m alphaforge.main analyze oklo
python -m alphaforge.main analyze nvda
python -m alphaforge.main analyze rklb

# 3. Baca laporan lengkapnya, putuskan mana yang layak diriset lebih jauh
#    di luar AlphaForge (baca 10-K, dengerin earnings call, dst)
```

---

## Satu hal penting yang perlu selalu diinget

`composite_score` di `scan` dan `Grade` di `analyze` itu **alat bantu
prioritas riset, bukan sinyal beli/jual**. AlphaForge nunjukin "mana yang
layak dicek lebih dalam duluan", bukan "mana yang pasti bagus". Keputusan
akhir tetap perlu riset manual di luar angka-angka ini.

---

© AlphaForge

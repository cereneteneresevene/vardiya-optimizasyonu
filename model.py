# -*- coding: utf-8 -*-
import pandas as pd
from pulp import *

# --- VERİYİ OKU ---
hemsireler = pd.read_csv("data/hemsireler.csv")
vardiyalar = pd.read_csv("data/vardiyalar.csv")

# --- TANIMLAMALAR ---
hemsire_listesi = hemsireler["isim"].tolist()
vardiya_listesi = vardiyalar["vardiya_adi"].tolist()
gunler = list(range(7))  # 0=Pzt, 6=Pzr

# --- MODEL OLUŞTUR ---
model = LpProblem("Vardiya_Optimizasyonu", LpMinimize)

# --- DEĞİŞKENLER ---
# x[hemşire][gün][vardiya] = 1 ya da 0
x = LpVariable.dicts(
    "calisma",
    [(h, g, v) for h in hemsire_listesi
               for g in gunler
               for v in vardiya_listesi],
    cat="Binary"
)

# --- AMAÇ FONKSİYONU ---
# Kıdemli hemşireleri gece vardiyasına daha az ver
# Kıdem arttıkça gece vardiyası maliyeti artar
model += lpSum(
    x[(h, g, "gece")] * hemsireler.loc[hemsireler["isim"] == h, "kidem_yil"].values[0]
    for h in hemsire_listesi
    for g in gunler
)

# --- KISITLAR ---

# 1. Her vardiyada minimum kişi sayısı karşılanmalı
for g in gunler:
    for v in vardiya_listesi:
        min_kisi = vardiyalar.loc[vardiyalar["vardiya_adi"] == v, "min_kisi"].values[0]
        model += lpSum(x[(h, g, v)] for h in hemsire_listesi) >= min_kisi

# 2. Bir hemşire izin gününde çalışamaz
for _, row in hemsireler.iterrows():
    h = row["isim"]
    izin = row["izin_gun"]
    for v in vardiya_listesi:
        model += x[(h, izin, v)] == 0

# 3. Haftalık max saati aşamaz (her vardiya 8 saat)
for _, row in hemsireler.iterrows():
    h = row["isim"]
    max_saat = row["max_haftalik_saat"]
    model += lpSum(
        x[(h, g, v)] * 8
        for g in gunler
        for v in vardiya_listesi
    ) <= max_saat

# 4. Günde sadece 1 vardiyada çalışabilir
for h in hemsire_listesi:
    for g in gunler:
        model += lpSum(x[(h, g, v)] for v in vardiya_listesi) <= 1

# --- ÇÖZDÜR ---
model.solve(PULP_CBC_CMD(msg=0))

# --- SONUÇLARI GÖSTER ---
print(f"Durum: {LpStatus[model.status]}")
print("\n📅 Haftalık Vardiya Planı:\n")

gun_isimleri = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Pzr"]

for g in gunler:
    print(f"--- {gun_isimleri[g]} ---")
    for v in vardiya_listesi:
        çalışanlar = [h for h in hemsire_listesi if value(x[(h, g, v)]) == 1]
        print(f"  {v}: {', '.join(çalışanlar)}")
    print()
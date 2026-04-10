# -*- coding: utf-8 -*-
import pandas as pd
import random

random.seed(42)  # Aynı veriyi üretmek için sabitliyoruz

# --- HEMŞİRELER ---
isimler = [
    "Ayşe", "Fatma", "Zeynep", "Meral", "Selin",
    "Hülya", "Elif", "Büşra", "Merve", "Canan",
    "Tuğba", "Sevgi", "Derya", "Nazan", "Pınar",
    "Gül", "Esra", "Arzu", "Nilüfer", "Sibel"
]

gunler = [0, 1, 2, 3, 4, 5, 6]  # 0=Pazartesi, 6=Pazar

hemsire_listesi = []
for isim in isimler:
    hemsire_listesi.append({
        "isim": isim,
        "max_haftalik_saat": random.choice([24, 32, 40]),
        "kidem_yil": random.randint(1, 15),
        "izin_gun": random.choice(gunler)
    })

hemsireler = pd.DataFrame(hemsire_listesi)

# --- VARDİYALAR ---
vardiyalar = pd.DataFrame({
    "vardiya_adi": ["sabah", "oglen", "gece"],
    "baslangic": ["07:00", "15:00", "23:00"],
    "bitis":     ["15:00", "23:00", "07:00"],
    "sure_saat": [8, 8, 8],
    "min_kisi":  [3, 3, 2]
})

# --- KAYDET ---
hemsireler.to_csv("data/hemsireler.csv", index=False)
vardiyalar.to_csv("data/vardiyalar.csv", index=False)

print("✅ Hemşireler:")
print(hemsireler)
print("\n✅ Vardiyalar:")
print(vardiyalar)
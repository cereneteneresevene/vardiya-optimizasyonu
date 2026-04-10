# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pulp import *

st.set_page_config(page_title="Vardiya Optimizasyonu", page_icon="🏥")
st.title("🏥 Hemşire Vardiya Optimizasyonu")
st.markdown("Haftalık vardiya planını otomatik oluştur.")

# --- VERİYİ OKU ---
hemsireler = pd.read_csv("data/hemsireler.csv")
vardiyalar = pd.read_csv("data/vardiyalar.csv")

# --- KENAR ÇUBUĞU ---
st.sidebar.header("⚙️ Ayarlar")
st.sidebar.dataframe(hemsireler)

# --- ÇALIŞTIR BUTONU ---
if st.button("🚀 Vardiya Planını Oluştur"):

    hemsire_listesi = hemsireler["isim"].tolist()
    vardiya_listesi = vardiyalar["vardiya_adi"].tolist()
    gunler = list(range(7))
    gun_isimleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

    # MODEL
    model = LpProblem("Vardiya_Optimizasyonu", LpMinimize)

    x = LpVariable.dicts(
        "calisma",
        [(h, g, v) for h in hemsire_listesi
                   for g in gunler
                   for v in vardiya_listesi],
        cat="Binary"
    )

    model += lpSum(
        x[(h, g, "gece")] * hemsireler.loc[hemsireler["isim"] == h, "kidem_yil"].values[0]
        for h in hemsire_listesi
        for g in gunler
    )

    for g in gunler:
        for v in vardiya_listesi:
            min_kisi = vardiyalar.loc[vardiyalar["vardiya_adi"] == v, "min_kisi"].values[0]
            model += lpSum(x[(h, g, v)] for h in hemsire_listesi) >= min_kisi

    for _, row in hemsireler.iterrows():
        h = row["isim"]
        izin = row["izin_gun"]
        for v in vardiya_listesi:
            model += x[(h, izin, v)] == 0

    for _, row in hemsireler.iterrows():
        h = row["isim"]
        max_saat = row["max_haftalik_saat"]
        model += lpSum(
            x[(h, g, v)] * 8
            for g in gunler
            for v in vardiya_listesi
        ) <= max_saat

    for h in hemsire_listesi:
        for g in gunler:
            model += lpSum(x[(h, g, v)] for v in vardiya_listesi) <= 1

    model.solve(PULP_CBC_CMD(msg=0))

    if LpStatus[model.status] == "Optimal":
        st.success("✅ Optimal vardiya planı oluşturuldu!")

        # SONUÇLARI TABLOYA DÖKÜT
        rows = []
        for g in gunler:
            for v in vardiya_listesi:
                çalışanlar = [h for h in hemsire_listesi if value(x[(h, g, v)]) == 1]
                rows.append({
                    "Gün": gun_isimleri[g],
                    "Vardiya": v,
                    "Çalışanlar": ", ".join(çalışanlar),
                    "Kişi Sayısı": len(çalışanlar)
                })

        sonuc_df = pd.DataFrame(rows)

        # GÜNLERE GÖRE GÖSTER
        for gun in gun_isimleri:
            st.subheader(f"📅 {gun}")
            gun_df = sonuc_df[sonuc_df["Gün"] == gun][["Vardiya", "Çalışanlar", "Kişi Sayısı"]]
            st.dataframe(gun_df, use_container_width=True)

    else:
        st.error("❌ Optimal çözüm bulunamadı.")
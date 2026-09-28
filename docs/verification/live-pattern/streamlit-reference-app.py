# -*- coding: utf-8 -*-
"""AgroHydro — Konya göreli sulama baskısı karar destek uygulaması."""

import json
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from agrohydro_core import (
    duyarilik_matrisi_hesapla,
    iklim_carpani_hesapla,
    optimize_urun_deseni,
    oranlari_dengele,
    oranlari_dogrula,
    pareto_egri_hesapla,
    toplam_baski_hesapla,
    urun_baskilari_hesapla,
    varsayim_simulasyonu,
)


st.set_page_config(
    page_title="AgroHydro | Su Yönetimi Karar Destek Sistemi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = {
    "Bugday": "#D89A2B",
    "Arpa": "#4E7A5B",
    "Dane Misir": "#D2653C",
    "Seker Pancari": "#6B6FA9",
}
URUN_GORUNUM = {
    "Bugday": "Buğday",
    "Arpa": "Arpa",
    "Dane Misir": "Dane Mısır",
    "Seker Pancari": "Şeker Pancarı",
}
SENARYO_GORUNUM = {
    "Baz": "Baz",
    "Orta_Baski": "Orta Baskı",
    "Yuksek_Baski": "Yüksek Baskı",
}
PALETTE = {
    "ink": "#17221B",
    "muted": "#66736B",
    "green": "#2E684B",
    "gold": "#C58A24",
    "orange": "#D2653C",
    "blue": "#416E8C",
    "grid": "#E5E9E3",
}
GELIR_KATSAYILARI = {
    "Bugday": 1.0,
    "Arpa": 0.8,
    "Dane Misir": 2.5,
    "Seker Pancari": 3.0,
}


st.markdown(
    """
    <style>
    :root {
        --ag-ink: #17221B;
        --ag-muted: #66736B;
        --ag-green: #2E684B;
        --ag-green-dark: #214E38;
        --ag-green-soft: #DDEAE1;
        --ag-canvas: #F4F6F1;
        --ag-surface: #FFFFFF;
        --ag-border: #DDE3DC;
        --ag-ease: cubic-bezier(0.23, 1, 0.32, 1);
    }
    .stApp { background: var(--ag-canvas); color: var(--ag-ink); }
    [data-testid="stHeader"] { background: rgba(244, 246, 241, 0.92); }
    [data-testid="stSidebar"] {
        background: #EDF2EA;
        border-right: 1px solid var(--ag-border);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: var(--ag-ink); }
    .block-container { max-width: 1440px; padding-top: 1.4rem; padding-bottom: 4rem; }
    .ag-hero {
        background: var(--ag-surface);
        border: 1px solid var(--ag-border);
        border-radius: 22px;
        padding: 28px 30px 26px;
        margin-bottom: 18px;
        box-shadow: 0 10px 34px rgba(31, 55, 41, 0.06);
    }
    .ag-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--ag-green-dark);
        background: var(--ag-green-soft);
        border: 1px solid #C7DCCB;
        border-radius: 999px;
        padding: 6px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .ag-hero h1 {
        margin: 14px 0 7px;
        color: var(--ag-ink);
        font-size: clamp(2.15rem, 5vw, 3.7rem);
        line-height: 0.98;
        letter-spacing: -0.045em;
    }
    .ag-hero p {
        max-width: 820px;
        margin: 0;
        color: var(--ag-muted);
        font-size: 1.02rem;
        line-height: 1.6;
    }
    .ag-badges { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 17px; }
    .ag-badge {
        border: 1px solid var(--ag-border);
        border-radius: 999px;
        background: #F9FAF7;
        color: #405047;
        padding: 6px 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    [data-testid="stMetric"] {
        background: var(--ag-surface);
        border: 1px solid var(--ag-border);
        border-radius: 16px;
        padding: 17px 18px;
        box-shadow: 0 4px 18px rgba(31, 55, 41, 0.035);
    }
    [data-testid="stMetricLabel"] { color: var(--ag-muted); }
    [data-testid="stMetricValue"] { color: var(--ag-ink); letter-spacing: -0.025em; }
    .ag-section-note {
        color: var(--ag-muted);
        font-size: 0.92rem;
        margin: -0.45rem 0 1.1rem;
    }
    .ag-callout {
        background: #F9FAF7;
        border: 1px solid var(--ag-border);
        border-left: 4px solid var(--ag-green);
        border-radius: 12px;
        padding: 14px 16px;
        color: #34443A;
        line-height: 1.55;
    }
    .stButton > button, .stDownloadButton > button {
        border-radius: 11px;
        min-height: 2.65rem;
        font-weight: 650;
        transition: transform 140ms var(--ag-ease), border-color 140ms ease, background-color 140ms ease;
    }
    .stButton > button:active, .stDownloadButton > button:active { transform: scale(0.98); }
    .stButton > button:focus-visible, .stDownloadButton > button:focus-visible {
        outline: 3px solid rgba(46, 104, 75, 0.22);
        outline-offset: 2px;
    }
    button[data-baseweb="tab"] { font-weight: 650; }
    [data-testid="stDataFrame"] { border: 1px solid var(--ag-border); border-radius: 14px; overflow: hidden; }
    div[data-testid="stExpander"] { border: 1px solid var(--ag-border); border-radius: 14px; background: #FAFBF8; }
    hr { border-color: var(--ag-border); }
    @media (hover: hover) and (pointer: fine) {
        .stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-1px); }
    }
    @media (prefers-reduced-motion: reduce) {
        .stButton > button, .stDownloadButton > button { transition: none; }
        .stButton > button:hover, .stDownloadButton > button:hover { transform: none; }
    }
    @media (max-width: 768px) {
        .block-container { padding: 0.75rem 0.8rem 2.5rem; }
        .ag-hero { border-radius: 16px; padding: 20px 18px; }
        .ag-hero h1 { font-size: 2.35rem; }
        .ag-hero p { font-size: 0.94rem; }
        .ag-badges { gap: 6px; }
        .ag-badge { font-size: 0.72rem; padding: 5px 8px; }
        [data-testid="stMetric"] { padding: 13px 14px; }
        button[data-baseweb="tab"] { font-size: 0.78rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def veri_yukle():
    crops = pd.read_csv(os.path.join(BASE_DIR, "crops.csv"))
    climate = pd.read_csv(os.path.join(BASE_DIR, "climate_baseline.csv"))
    scenarios = pd.read_csv(os.path.join(BASE_DIR, "scenario_config.csv"))
    with open(os.path.join(BASE_DIR, "optimization_rules.json"), encoding="utf-8") as stream:
        rules = json.load(stream)
    return crops, climate, scenarios, rules


def figur_stili(fig, height=430, legend=True):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Segoe UI, Arial, sans-serif", color=PALETTE["ink"], size=13),
        margin=dict(l=36, r=24, t=62, b=42),
        hoverlabel=dict(bgcolor="#17221B", font_color="white", bordercolor="#17221B"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""
        ) if legend else dict(visible=False),
    )
    fig.update_xaxes(gridcolor=PALETTE["grid"], zerolinecolor=PALETTE["grid"])
    fig.update_yaxes(gridcolor=PALETTE["grid"], zerolinecolor=PALETTE["grid"])
    return fig


def goreli_durum(endeks):
    if endeks < 0.95:
        return "Altında"
    if endeks <= 1.05:
        return "Yakın"
    if endeks <= 1.25:
        return "Üzerinde"
    return "Yüksek"


def csv_bytes(frame):
    return frame.to_csv(index=False).encode("utf-8-sig")


crops_df, climate_df, scenarios_df, rules = veri_yukle()
urunler = crops_df["urun"].tolist()
toplam_alan = float(crops_df["alan_da"].sum())
su_katsayilari = crops_df["su_katsayisi"].to_numpy(dtype=float)
mevcut_oranlar = crops_df["alan_da"].to_numpy(dtype=float) / toplam_alan
alt_oranlar = crops_df["min_oran"].to_numpy(dtype=float)
ust_oranlar = crops_df["max_oran"].to_numpy(dtype=float)
baz_toplam = toplam_baski_hesapla(mevcut_oranlar, toplam_alan, su_katsayilari, 1.0)

mevcut_yuzdeler = np.round(mevcut_oranlar * 100, 1)
mevcut_yuzdeler[-1] += round(100.0 - float(mevcut_yuzdeler.sum()), 1)
presets = {
    "Mevcut desen": mevcut_yuzdeler,
    "Su verimli örnek": np.array([47.0, 45.0, 5.0, 3.0]),
    "Su yoğun örnek": np.array([40.0, 20.0, 25.0, 15.0]),
}

for urun, value in zip(urunler, mevcut_yuzdeler):
    st.session_state.setdefault(f"oran_{urun}", float(value))
st.session_state.setdefault("desen_preset", "Mevcut desen")


def preset_uygula():
    secim = st.session_state.get("desen_preset")
    if secim in presets:
        for urun, value in zip(urunler, presets[secim]):
            st.session_state[f"oran_{urun}"] = float(value)


def ozel_olarak_isaretle():
    st.session_state["desen_preset"] = "Özel"


def oranlari_dengele_callback():
    values = [st.session_state[f"oran_{u}"] for u in urunler]
    balanced = oranlari_dengele(values, alt_oranlar * 100, ust_oranlar * 100)
    for urun, value in zip(urunler, balanced):
        st.session_state[f"oran_{urun}"] = float(value)
    st.session_state["desen_preset"] = "Özel"


with st.sidebar:
    st.markdown("## AgroHydro")
    st.caption("Canlı senaryo laboratuvarı")
    st.markdown("### İklim koşulları")
    sicaklik_artisi = st.slider(
        "Sıcaklık artışı", 0.0, 3.0, 1.5, 0.1, format="%.1f °C",
        help="Baz döneme göre varsayılan ortalama sıcaklık artışı.",
    )
    yagis_yuzde = st.slider(
        "Yağış değişimi", -30, 0, -15, 1, format="%d%%",
        help="Negatif değer yağış azalmasını ifade eder.",
    )
    yagis_orani = yagis_yuzde / 100.0
    iklim_carpani = iklim_carpani_hesapla(sicaklik_artisi, yagis_orani)
    st.metric(
        "İklim çarpanı",
        f"{iklim_carpani:.3f}",
        f"{(iklim_carpani - 1) * 100:+.1f}%",
        delta_color="inverse",
    )

    st.divider()
    st.markdown("### Ürün deseni")
    st.selectbox(
        "Hızlı senaryo",
        ["Mevcut desen", "Su verimli örnek", "Su yoğun örnek", "Özel"],
        key="desen_preset",
        on_change=preset_uygula,
    )
    for i, urun in enumerate(urunler):
        st.slider(
            f"{URUN_GORUNUM[urun]} payı",
            float(alt_oranlar[i] * 100),
            float(ust_oranlar[i] * 100),
            step=0.1,
            format="%.1f%%",
            key=f"oran_{urun}",
            on_change=ozel_olarak_isaretle,
        )

    kullanici_yuzdeler = np.array([st.session_state[f"oran_{u}"] for u in urunler])
    toplam_yuzde = float(kullanici_yuzdeler.sum())
    if abs(toplam_yuzde - 100.0) <= 0.05:
        st.success(f"Toplam: %{toplam_yuzde:.1f}")
    else:
        st.error(f"Toplam: %{toplam_yuzde:.1f} — %100 olmalı")
    st.button(
        "Oranları %100'e dengele",
        on_click=oranlari_dengele_callback,
        use_container_width=True,
    )
    st.divider()
    st.caption("Model, kesin m³ su tüketimi değil; karşılaştırmalı göreli sulama baskısı üretir.")


st.markdown(
    """
    <section class="ag-hero">
        <span class="ag-eyebrow">🏆 TÜBİTAK 2204-D Su Yönetimi Türkiye Birincisi</span>
        <h1>AgroHydro</h1>
        <p>Konya'da iklim baskısı ile ürün desenini aynı modelde buluşturan, alternatifleri anlık olarak karşılaştıran ve kısıtlar altında uygulanabilir ürün deseni üreten karar destek sistemi.</p>
        <div class="ag-badges">
            <span class="ag-badge">Açıklanabilir model</span>
            <span class="ag-badge">Doğrusal programlama</span>
            <span class="ag-badge">Canlı senaryo analizi</span>
            <span class="ag-badge">12,69 milyon dekar</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

kullanici_oranlar = kullanici_yuzdeler / 100.0
gecerli, oran_mesaji = oranlari_dogrula(
    kullanici_oranlar, alt_oranlar, ust_oranlar, tolerans=5e-4
)
if not gecerli:
    st.error(f"Senaryo durduruldu: {oran_mesaji}")
    st.info("Sol menüdeki **Oranları %100'e dengele** düğmesiyle geçerli bir ürün deseni oluşturabilirsiniz.")
    st.stop()

mevcut_iklim_baski = toplam_baski_hesapla(
    mevcut_oranlar, toplam_alan, su_katsayilari, iklim_carpani
)
kullanici_baski = toplam_baski_hesapla(
    kullanici_oranlar, toplam_alan, su_katsayilari, iklim_carpani
)
kullanici_norm = kullanici_baski / baz_toplam
iklim_etkisi = mevcut_iklim_baski - baz_toplam
desen_etkisi = kullanici_baski - mevcut_iklim_baski
desen_degisim_yuzde = desen_etkisi / mevcut_iklim_baski * 100
durum_metni = goreli_durum(kullanici_norm)
su_odakli_opt = optimize_urun_deseni(
    crops_df, iklim_carpani, rules, gelir_katsayilari=GELIR_KATSAYILARI
)

tabs = st.tabs(
    ["Genel Bakış", "Simülasyon", "Optimizasyon", "Duyarlılık", "Model ve Veriler"]
)


with tabs[0]:
    st.subheader("Karar özeti")
    st.markdown(
        '<p class="ag-section-note">Seçilen iklim koşulları ve ürün deseninin baz duruma göre konumu.</p>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Normalize baskı",
        f"{kullanici_norm:.3f}",
        f"{(kullanici_norm - 1) * 100:+.1f}% baz",
        delta_color="inverse",
    )
    c2.metric(
        "Ürün deseni etkisi",
        f"{desen_degisim_yuzde:+.1f}%",
        "aynı iklim altında",
        delta_color="inverse",
    )
    c3.metric("Su odaklı iyileşme", f"%{su_odakli_opt['azalma_yuzdesi']:.1f}", "azalma")
    c4.metric("Baz karşılaştırması", durum_metni, help=f"Normalize endeks: {kullanici_norm:.3f}")

    left, right = st.columns([1.0, 1.25], gap="large")
    with left:
        gauge_max = max(1.50, kullanici_norm * 1.08)
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=kullanici_norm,
                number={"valueformat": ".3f", "font": {"size": 42, "color": PALETTE["ink"]}},
                title={"text": "Baz = 1.000", "font": {"size": 14, "color": PALETTE["muted"]}},
                gauge={
                    "axis": {"range": [0.75, gauge_max], "tickwidth": 1},
                    "bar": {"color": PALETTE["green"], "thickness": 0.28},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0.75, 1.0], "color": "#E7EFE8"},
                        {"range": [1.0, 1.25], "color": "#F3E8C9"},
                        {"range": [1.25, gauge_max], "color": "#F3D9CF"},
                    ],
                    "threshold": {"line": {"color": PALETTE["ink"], "width": 3}, "value": 1.0},
                },
            )
        )
        figur_stili(fig_gauge, height=340, legend=False)
        fig_gauge.update_layout(margin=dict(l=24, r=24, t=55, b=15))
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    with right:
        katkilar = urun_baskilari_hesapla(
            kullanici_oranlar, toplam_alan, su_katsayilari, iklim_carpani
        )
        katki_df = pd.DataFrame(
            {
                "Ürün": [URUN_GORUNUM[u] for u in urunler],
                "Kod": urunler,
                "Baskı": katkilar,
                "Katkı (%)": katkilar / katkilar.sum() * 100,
            }
        ).sort_values("Baskı")
        fig_katki = go.Figure(
            go.Bar(
                x=katki_df["Baskı"],
                y=katki_df["Ürün"],
                orientation="h",
                marker_color=[COLORS[u] for u in katki_df["Kod"]],
                text=[f"%{v:.1f}" for v in katki_df["Katkı (%)"]],
                textposition="outside",
                customdata=katki_df[["Katkı (%)"]],
                hovertemplate="<b>%{y}</b><br>Baskı: %{x:,.0f}<br>Katkı: %{customdata[0]:.1f}%<extra></extra>",
            )
        )
        fig_katki.update_layout(title="Ürünlerin göreli baskı katkısı", xaxis_title="Göreli baskı puanı")
        figur_stili(fig_katki, height=340, legend=False)
        st.plotly_chart(fig_katki, use_container_width=True, config={"displayModeBar": False})

    if abs(desen_degisim_yuzde) < 0.05:
        yorum = "Seçilen ürün deseni mevcut desenle aynı göreli baskı düzeyindedir."
    elif desen_etkisi < 0:
        yorum = f"Seçilen ürün deseni, aynı iklim koşullarındaki mevcut desene göre baskıyı %{abs(desen_degisim_yuzde):.1f} azaltıyor."
    elif desen_etkisi > 0:
        yorum = f"Seçilen ürün deseni, aynı iklim koşullarındaki mevcut desene göre baskıyı %{desen_degisim_yuzde:.1f} artırıyor."
    st.markdown(
        f'<div class="ag-callout"><b>Model yorumu:</b> {yorum} İklim etkisi ve ürün deseni etkisi Simülasyon sekmesinde ayrı ayrı gösterilir.</div>',
        unsafe_allow_html=True,
    )


with tabs[1]:
    st.subheader("İklim ve ürün deseni etkisini ayır")
    st.markdown(
        '<p class="ag-section-note">Toplam değişimin ne kadarının iklim varsayımından, ne kadarının ürün deseninden geldiğini izleyin.</p>',
        unsafe_allow_html=True,
    )
    col_waterfall, col_mix = st.columns([1.15, 1], gap="large")
    with col_waterfall:
        fig_waterfall = go.Figure(
            go.Waterfall(
                x=["Baz", "İklim etkisi", "Ürün deseni etkisi", "Seçilen senaryo"],
                measure=["absolute", "relative", "relative", "total"],
                y=[baz_toplam, iklim_etkisi, desen_etkisi, kullanici_baski],
                text=[f"{baz_toplam:,.0f}", f"{iklim_etkisi:+,.0f}", f"{desen_etkisi:+,.0f}", f"{kullanici_baski:,.0f}"],
                textposition="outside",
                connector={"line": {"color": "#AAB5AD", "width": 1}},
                increasing={"marker": {"color": PALETTE["orange"]}},
                decreasing={"marker": {"color": PALETTE["blue"]}},
                totals={"marker": {"color": PALETTE["green"]}},
                hovertemplate="%{x}<br>%{y:+,.0f}<extra></extra>",
            )
        )
        fig_waterfall.update_layout(title="Bazdan seçilen senaryoya değişim", yaxis_title="Göreli baskı puanı")
        figur_stili(fig_waterfall, height=430, legend=False)
        st.plotly_chart(fig_waterfall, use_container_width=True, config={"displayModeBar": False})

    with col_mix:
        mix_df = pd.DataFrame(
            {
                "Desen": ["Mevcut", "Seçilen"],
                **{urun: [mevcut_oranlar[i] * 100, kullanici_oranlar[i] * 100] for i, urun in enumerate(urunler)},
            }
        )
        fig_mix = go.Figure()
        for urun in urunler:
            fig_mix.add_trace(
                go.Bar(
                    name=URUN_GORUNUM[urun],
                    y=mix_df["Desen"],
                    x=mix_df[urun],
                    orientation="h",
                    marker_color=COLORS[urun],
                    text=[f"%{v:.1f}" if v >= 7 else "" for v in mix_df[urun]],
                    textposition="inside",
                    hovertemplate=f"<b>{urun}</b><br>%{{y}}: %{{x:.1f}}%<extra></extra>",
                )
            )
        fig_mix.update_layout(
            title="Ürün deseni bileşimi", barmode="stack", xaxis_title="Alan payı (%)", xaxis_range=[0, 100]
        )
        figur_stili(fig_mix, height=430, legend=True)
        fig_mix.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.17, xanchor="left", x=0),
            margin=dict(l=36, r=24, t=62, b=92),
        )
        st.plotly_chart(fig_mix, use_container_width=True, config={"displayModeBar": False})

    senaryo_rows = []
    for row in scenarios_df.itertuples(index=False):
        pressure = toplam_baski_hesapla(kullanici_oranlar, toplam_alan, su_katsayilari, row.iklim_carpani)
        senaryo_rows.append(
            {
                "Senaryo": SENARYO_GORUNUM.get(row.senaryo, row.senaryo.replace("_", " ")),
                "İklim çarpanı": row.iklim_carpani,
                "Toplam baskı": pressure,
                "Normalize endeks": pressure / baz_toplam,
            }
        )
    senaryo_rows.append(
        {
            "Senaryo": "Canlı seçim",
            "İklim çarpanı": iklim_carpani,
            "Toplam baskı": kullanici_baski,
            "Normalize endeks": kullanici_norm,
        }
    )
    senaryo_df = pd.DataFrame(senaryo_rows)
    fig_senaryo = go.Figure(
        go.Bar(
            x=senaryo_df["Senaryo"],
            y=senaryo_df["Normalize endeks"],
            marker_color=["#91AA96", "#D7AA55", "#D26B4B", PALETTE["green"]],
            text=[f"{v:.3f}" for v in senaryo_df["Normalize endeks"]],
            textposition="outside",
            customdata=senaryo_df[["Toplam baskı", "İklim çarpanı"]],
            hovertemplate="<b>%{x}</b><br>Endeks: %{y:.3f}<br>Baskı: %{customdata[0]:,.0f}<br>Çarpan: %{customdata[1]:.3f}<extra></extra>",
        )
    )
    fig_senaryo.add_hline(y=1.0, line_dash="dash", line_color="#7F8D84", annotation_text="Baz")
    fig_senaryo.update_layout(title="Seçilen ürün deseni farklı iklim senaryolarında", yaxis_title="Normalize baskı endeksi")
    figur_stili(fig_senaryo, height=420, legend=False)
    st.plotly_chart(fig_senaryo, use_container_width=True, config={"displayModeBar": False})


with tabs[2]:
    st.subheader("Su baskısı ve ekonomik koruma dengesi")
    st.markdown(
        '<p class="ag-section-note">Model, göreli baskıyı azaltırken temsili gelir endeksinin ne kadar korunacağını bir kısıt olarak ele alır.</p>',
        unsafe_allow_html=True,
    )
    gelir_koruma_yuzde = st.slider(
        "Asgari gelir endeksi koruması", 80, 110, 90, 1, format="%d%%",
        help="Temsili gelir katsayılarına göre mevcut desen gelir endeksinin korunması gereken en düşük oran.",
    )
    opt = optimize_urun_deseni(
        crops_df,
        iklim_carpani,
        rules,
        gelir_katsayilari=GELIR_KATSAYILARI,
        minimum_gelir_koruma=gelir_koruma_yuzde / 100.0,
    )
    if not opt.get("basarili"):
        st.error(f"Bu gelir koruma düzeyinde uygulanabilir çözüm bulunamadı: {opt.get('hata')}")
    else:
        o1, o2, o3, o4 = st.columns(4)
        o1.metric(
            "Baskı değişimi",
            f"{opt['azalma_yuzdesi']:+.2f}%",
            "pozitif = azalma",
            delta_color="normal" if opt["azalma_yuzdesi"] >= 0 else "inverse",
        )
        o2.metric("Gelir endeksi koruması", f"{opt['gelir_koruma_orani'] * 100:.1f}%", f"hedef ≥ %{gelir_koruma_yuzde}")
        o3.metric("Optimize baskı", f"{opt['optimize_baski'] / 1_000_000:.2f} Mn", f"{opt['optimize_baski'] / baz_toplam:.3f} normalize")
        o4.metric("Alan toplamı", f"{opt['oran_toplami'] * 100:.1f}%", "kısıt sağlandı")

        comp_rows = []
        for i, urun in enumerate(urunler):
            comp_rows.append(
                {
                    "Ürün": URUN_GORUNUM[urun],
                    "Mevcut": mevcut_oranlar[i] * 100,
                    "Seçilen": kullanici_oranlar[i] * 100,
                    "Optimize": opt["optimize_oranlar"][i] * 100,
                    "Alt sınır": opt["alt_sinirlar"][i] * 100,
                    "Üst sınır": opt["ust_sinirlar"][i] * 100,
                }
            )
        comp_df = pd.DataFrame(comp_rows)
        comp_long = comp_df.melt(
            id_vars=["Ürün", "Alt sınır", "Üst sınır"],
            value_vars=["Mevcut", "Seçilen", "Optimize"],
            var_name="Desen",
            value_name="Alan payı (%)",
        )
        fig_comp = px.bar(
            comp_long,
            x="Ürün",
            y="Alan payı (%)",
            color="Desen",
            barmode="group",
            color_discrete_map={"Mevcut": "#AAB5AD", "Seçilen": PALETTE["gold"], "Optimize": PALETTE["green"]},
            text_auto=".1f",
            title="Mevcut, seçilen ve optimize ürün deseni",
        )
        fig_comp.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
        figur_stili(fig_comp, height=440, legend=True)
        st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})

        pareto = pareto_egri_hesapla(
            crops_df, iklim_carpani, rules, GELIR_KATSAYILARI, np.linspace(0.75, 1.10, 36)
        )
        p_left, p_right = st.columns([1.25, 1], gap="large")
        with p_left:
            fig_pareto = go.Figure(
                go.Scatter(
                    x=pareto["gerceklesen_gelir_koruma_%"],
                    y=pareto["baski_azalmasi_%"],
                    mode="lines+markers",
                    line={"color": PALETTE["green"], "width": 3},
                    marker={"size": 6, "color": "white", "line": {"color": PALETTE["green"], "width": 2}},
                    customdata=pareto[["istenen_gelir_koruma_%", "optimize_baski"]],
                    hovertemplate="Gelir koruma: %{x:.1f}%<br>Baskı değişimi: %{y:+.2f}%<br>İstenen alt sınır: %{customdata[0]:.0f}%<br>Baskı: %{customdata[1]:,.0f}<extra></extra>",
                )
            )
            fig_pareto.add_trace(
                go.Scatter(
                    x=[opt["gelir_koruma_orani"] * 100],
                    y=[opt["azalma_yuzdesi"]],
                    mode="markers",
                    name="Seçilen çözüm",
                    marker={"size": 14, "color": PALETTE["gold"], "line": {"color": PALETTE["ink"], "width": 2}},
                    hovertemplate="Seçilen çözüm<extra></extra>",
                )
            )
            fig_pareto.add_hline(y=0, line_dash="dash", line_color="#98A39C")
            fig_pareto.update_layout(
                title="Su–gelir ödünleşim sınırı",
                xaxis_title="Gerçekleşen temsili gelir endeksi koruması (%)",
                yaxis_title="Göreli baskı azalması (%)",
            )
            figur_stili(fig_pareto, height=430, legend=True)
            st.plotly_chart(fig_pareto, use_container_width=True, config={"displayModeBar": False})
        with p_right:
            display_comp = comp_df.copy()
            for col in ["Mevcut", "Seçilen", "Optimize", "Alt sınır", "Üst sınır"]:
                display_comp[col] = display_comp[col].map(lambda v: f"%{v:.1f}")
            st.markdown("#### Oran ve kısıt tablosu")
            st.dataframe(display_comp, hide_index=True, use_container_width=True)
            st.caption(
                "Gelir katsayıları temsili bir endekstir; piyasa fiyatı, maliyet veya çiftçi kârı değildir. "
                "Bu modül ödünleşimi görünür kılar, gerçek ekonomik tahmin iddiasında bulunmaz."
            )


with tabs[3]:
    st.subheader("Duyarlılık ve varsayım analizi")
    st.markdown(
        '<p class="ag-section-note">Modelin iklim girdilerine ve kabul edilen katsayı değişkenliğine verdiği tepki.</p>',
        unsafe_allow_html=True,
    )
    sicakliklar = np.linspace(0, 3.0, 9)
    yagislar = np.linspace(0, -0.30, 9)
    matris = duyarilik_matrisi_hesapla(
        kullanici_oranlar, toplam_alan, su_katsayilari, baz_toplam, sicakliklar, yagislar
    )
    fig_heat = go.Figure(
        go.Heatmap(
            z=matris,
            x=[f"{v * 100:.0f}%" for v in yagislar],
            y=[f"+{v:.2f}°C" for v in sicakliklar],
            colorscale=[[0, "#EAF1EA"], [0.5, "#E4B65F"], [1, "#B64C32"]],
            colorbar={"title": "Endeks"},
            text=np.round(matris, 3),
            texttemplate="%{text:.3f}",
            hovertemplate="Sıcaklık: %{y}<br>Yağış: %{x}<br>Normalize endeks: %{z:.3f}<extra></extra>",
        )
    )
    fig_heat.update_layout(
        title="Seçilen ürün deseni için sıcaklık × yağış matrisi",
        xaxis_title="Yağış değişimi",
        yaxis_title="Sıcaklık artışı",
    )
    figur_stili(fig_heat, height=520, legend=False)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    with st.expander("Varsayım tabanlı belirsizlik simülasyonu", expanded=True):
        u1, u2, u3 = st.columns(3)
        temp_std = u1.slider("Sıcaklık sapması (σ)", 0.0, 0.8, 0.3, 0.1, format="%.1f °C")
        rain_std_pp = u2.slider("Yağış sapması (σ)", 0, 10, 4, 1, format="%d yüzde puan")
        water_cv_pct = u3.slider("Su katsayısı değişkenliği", 0, 20, 7, 1, format="%d%%")
        sim = varsayim_simulasyonu(
            kullanici_oranlar,
            toplam_alan,
            su_katsayilari,
            baz_toplam,
            sicaklik_artisi,
            yagis_orani,
            temp_std,
            rain_std_pp / 100.0,
            water_cv_pct / 100.0,
            ornek_sayisi=3000,
        )
        p10, p50, p90 = np.percentile(sim["normalize_endeks"], [10, 50, 90])
        s1, s2, s3 = st.columns(3)
        s1.metric("P10", f"{p10:.3f}")
        s2.metric("Medyan", f"{p50:.3f}")
        s3.metric("P90", f"{p90:.3f}")
        fig_hist = go.Figure(
            go.Histogram(
                x=sim["normalize_endeks"],
                nbinsx=38,
                marker_color=PALETTE["green"],
                opacity=0.9,
                hovertemplate="Endeks aralığı: %{x:.3f}<br>Simülasyon sayısı: %{y}<extra></extra>",
            )
        )
        for value, label, color in [
            (p10, "P10", PALETTE["blue"]),
            (p50, "Medyan", PALETTE["ink"]),
            (p90, "P90", PALETTE["orange"]),
        ]:
            fig_hist.add_vline(x=value, line_color=color, line_width=2, annotation_text=f"{label} {value:.3f}")
        fig_hist.update_layout(
            title="Varsayım senaryolarında normalize baskı dağılımı",
            xaxis_title="Normalize baskı endeksi",
            yaxis_title="Simülasyon sayısı",
            bargap=0.03,
        )
        figur_stili(fig_hist, height=430, legend=False)
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            "Bu dağılım istatistiksel güven aralığı değildir. Girilen dağılım ve katsayı değişkenliği "
            "varsayımlarının modele etkisini gösteren keşifsel bir senaryo zarfıdır."
        )


with tabs[4]:
    st.subheader("Model şeffaflığı ve veri katmanı")
    st.markdown(
        '<p class="ag-section-note">Formüller, kısıtlar, doğrulama kontrolleri ve dışa aktarılabilir sonuçlar.</p>',
        unsafe_allow_html=True,
    )
    f1, f2 = st.columns([1.05, 1], gap="large")
    with f1:
        st.markdown("#### Temel formül")
        st.latex(r"B = \sum_i A_i \times K_i \times (1 + 0.05\Delta T - \Delta P)")
        st.markdown(
            """
            - **B:** toplam göreli sulama baskısı
            - **Aᵢ:** ürünün ekim alanı
            - **Kᵢ:** göreli su katsayısı
            - **ΔT:** sıcaklık artışı (°C)
            - **ΔP:** yağış değişim oranı; azalma negatif girilir
            """
        )
        st.info("Endeks karşılaştırma amaçlıdır; m³ su hacmi veya yeraltı suyu seviyesi tahmini değildir.")
    with f2:
        st.markdown("#### Otomatik sağlık kontrolleri")
        scenario_formula = 1 + 0.05 * scenarios_df["sicaklik_artisi_c"] - scenarios_df["yagis_degisim_orani"]
        checks = pd.DataFrame(
            {
                "Kontrol": [
                    "Senaryo çarpanları formülle uyumlu",
                    "Mevcut ürün oranları %100",
                    "Minimum oranlar fizibil",
                    "Maksimum oranlar fizibil",
                    "Seçilen ürün deseni geçerli",
                ],
                "Durum": [
                    bool(np.allclose(scenario_formula, scenarios_df["iklim_carpani"])),
                    bool(np.isclose(mevcut_oranlar.sum(), 1.0)),
                    bool(alt_oranlar.sum() <= 1.0),
                    bool(ust_oranlar.sum() >= 1.0),
                    gecerli,
                ],
            }
        )
        checks["Sonuç"] = checks["Durum"].map({True: "Geçti", False: "Kontrol gerekli"})
        st.dataframe(checks[["Kontrol", "Sonuç"]], hide_index=True, use_container_width=True)

    st.markdown("#### Girdi verileri")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.caption("Ürünler ve kısıtlar")
        crops_display = crops_df.copy()
        crops_display["urun"] = crops_display["urun"].map(URUN_GORUNUM)
        crops_display["mevcut_oran_%"] = mevcut_oranlar * 100
        st.dataframe(crops_display, hide_index=True, use_container_width=True)
    with d2:
        st.caption("İklim senaryoları")
        st.dataframe(scenarios_df, hide_index=True, use_container_width=True)
    with d3:
        st.caption("Aylık iklim referansı")
        st.dataframe(climate_df, hide_index=True, use_container_width=True)

    with st.expander("Modelin sınırları ve doğru yorumlama", expanded=False):
        st.markdown(
            """
            - Model **göreli** bir endeks üretir; gerçek sulama hacmi, akifer seviyesi veya verim tahmini yapmaz.
            - İklim etkisi doğrusal ve ortak bir çarpan olarak uygulanır; ürünlerin iklime özgü tepkileri ayrıştırılmamıştır.
            - Gelir katsayıları temsili olup piyasa fiyatı, maliyet ve destek verileriyle kalibre edilmemiştir.
            - Optimizasyon, yalnızca tanımlı ürünler ve alt/üst oran sınırları içinde çözüm üretir.
            - Belirsizlik simülasyonu kullanıcı varsayımlarına dayanır; güven aralığı olarak yorumlanmamalıdır.
            """
        )

    export_baskilar = urun_baskilari_hesapla(
        kullanici_oranlar, toplam_alan, su_katsayilari, iklim_carpani
    )
    export_df = pd.DataFrame(
        {
            "urun": [URUN_GORUNUM[u] for u in urunler],
            "secilen_oran_%": kullanici_oranlar * 100,
            "secilen_alan_da": kullanici_oranlar * toplam_alan,
            "su_katsayisi": su_katsayilari,
            "urun_baskisi": export_baskilar,
            "iklim_carpani": iklim_carpani,
            "toplam_baski": kullanici_baski,
            "normalize_endeks": kullanici_norm,
        }
    )
    e1, e2, e3 = st.columns(3)
    e1.download_button(
        "Seçilen senaryoyu indir", csv_bytes(export_df), "agrohydro_secilen_senaryo.csv", "text/csv",
        use_container_width=True,
    )
    e2.download_button(
        "Senaryo karşılaştırmasını indir", csv_bytes(senaryo_df), "agrohydro_senaryo_karsilastirma.csv", "text/csv",
        use_container_width=True,
    )
    sensitivity_export = pd.DataFrame(
        matris,
        index=[f"+{v:.2f}C" for v in sicakliklar],
        columns=[f"{v * 100:.0f}%" for v in yagislar],
    ).reset_index().rename(columns={"index": "sicaklik_artisi"})
    e3.download_button(
        "Duyarlılık matrisini indir", csv_bytes(sensitivity_export), "agrohydro_duyarlilik.csv", "text/csv",
        use_container_width=True,
    )


st.markdown("---")
st.caption(
    "AgroHydro · TÜBİTAK 2204-D Su Yönetimi Türkiye Birincisi · "
    "Göreli Sulama Baskısı Karar Destek Sistemi"
)

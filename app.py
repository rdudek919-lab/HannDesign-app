import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Moje Koszty", page_icon="📈", layout="wide")

# --- MAGIA CSS (STYLIZACJA PRZYCISKÓW MENU, RAMEK ORAZ UKRYWANIE ELEMENTÓW) ---
st.markdown("""
<style>
/* Z ukryciem domyślnych kółek radio */
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

/* --- GŁÓWNE MENU (Miesiące - Styl Niebieski + PRZYKLEJONE DO GÓRY NAPRAWIONE) --- */
section[data-testid="stMain"] div[data-testid="stElementContainer"]:has(div[data-testid="stRadio"]) {
    position: sticky !important;
    top: 3.5rem !important; 
    z-index: 999 !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(5px) !important;
    padding: 15px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    border: 1px solid #e2e8f0 !important;
    margin-bottom: 20px !important;
}

section[data-testid="stMain"] div[data-testid="stRadio"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

section[data-testid="stMain"] div[data-testid="stRadio"] > div { display: flex; flex-wrap: wrap; gap: 12px; }
section[data-testid="stMain"] div[data-testid="stRadio"] > div > label {
    background-color: #E3F2FD !important; color: #0D47A1 !important;
    padding: 10px 24px !important; border-radius: 12px !important;
    border: 1px solid #90CAF9 !important; cursor: pointer;
    transition: all 0.2s ease-in-out; margin: 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
section[data-testid="stMain"] div[data-testid="stRadio"] > div > label p { color: inherit !important; margin: 0 !important; font-size: 16px !important; }
section[data-testid="stMain"] div[data-testid="stRadio"] > div > label:hover {
    background-color: #BBDEFB !important; border-color: #2196F3 !important;
    transform: translateY(-2px); box-shadow: 0 4px 8px rgba(33, 150, 243, 0.2);
}
section[data-testid="stMain"] div[data-testid="stRadio"] > div > label:has(input:checked) {
    background-color: #2196F3 !important; color: white !important;
    border-color: #1976D2 !important; box-shadow: 0 4px 10px rgba(33, 150, 243, 0.4);
}
section[data-testid="stMain"] div[data-testid="stRadio"] > div > label:has(input:checked) p { font-weight: 600 !important; }

/* --- MENU BOCZNE (Lata - SZTYWNA SZEROKOŚĆ KAFELKÓW) --- */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div { 
    display: flex; flex-direction: column; gap: 8px; width: 100%;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div > label {
    background-color: #F8FAFC !important;
    color: #1E293B !important;
    padding: 10px 15px !important; 
    border-radius: 8px !important;
    border: 1px solid #CBD5E1 !important; 
    cursor: pointer;
    transition: all 0.2s ease-in-out; 
    margin: 0 !important;
    width: 260px !important;
    min-width: 260px !important;
    display: flex !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div > label p { 
    color: inherit !important; margin: 0 !important; font-size: 16px !important; font-weight: 500 !important; text-align: center;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div > label:hover {
    background-color: #E2E8F0 !important; border-color: #94A3B8 !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div > label:has(input:checked) {
    background-color: #2196F3 !important; 
    color: #FFFFFF !important; 
    border-color: #1976D2 !important; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* --- Ramki dla podsumowań (Karty z wynikami) --- */
div[data-testid="stMetric"] {
    border-radius: 12px;
    padding: 15px 20px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
div[data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); }
.custom-metric {
    border-radius: 12px;
    padding: 15px 20px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    height: 100%;
}
.custom-metric:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); }

/* Niezawodne wymuszenie widoczności podświetlenia naprzemiennego */
div[data-testid="column"]:nth-child(4n+1) div[data-testid="stMetric"], div[data-testid="column"]:nth-child(4n+1) .custom-metric { background-color: #EFF6FF !important; border-left: 6px solid #2563EB !important; }
div[data-testid="column"]:nth-child(4n+2) div[data-testid="stMetric"], div[data-testid="column"]:nth-child(4n+2) .custom-metric { background-color: #F8FAFC !important; border-left: 6px solid #64748B !important; }
div[data-testid="column"]:nth-child(4n+3) div[data-testid="stMetric"], div[data-testid="column"]:nth-child(4n+3) .custom-metric { background-color: #ECFDF5 !important; border-left: 6px solid #059669 !important; }
div[data-testid="column"]:nth-child(4n) div[data-testid="stMetric"], div[data-testid="column"]:nth-child(4n) .custom-metric { background-color: #FFFBEB !important; border-left: 6px solid #D97706 !important; }
div[data-testid="InputInstructions"] { display: none !important; }

/* --- NOWA TABELA PODSUMOWANIA KATEGORII --- */
.cat-table { width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 10px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
.cat-table th { background-color: #f8fafc; padding: 16px 20px; border-bottom: 2px solid #e2e8f0; color: #475569; font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
.cat-table td { padding: 14px 20px; border-bottom: 1px solid #f1f5f9; font-weight: 600; color: #1e293b; font-size: 15px; }
.cat-table tr:last-child td { border-bottom: none; }
.cat-table tr:hover td { background-color: #f8fafc; }

/* =========================================================
   NOWOŚĆ: LOGIKA DLA TELEFONÓW KOMÓRKOWYCH (RESPANSYWNOŚĆ) 
   ========================================================= */
@media (max-width: 768px) {
    /* 1. Odpinamy menu od góry ekranu, żeby chowało się podczas przewijania */
    section[data-testid="stMain"] div[data-testid="stElementContainer"]:has(div[data-testid="stRadio"]) {
        position: relative !important;
        top: 0 !important;
        padding: 5px !important;
        margin-top: 0 !important;
        box-shadow: none !important;
        border: none !important;
        background-color: transparent !important;
    }
    
    /* 2. Zamiast budować wielki kwadrat z przycisków, robimy jeden poziomy pasek (scrollowalny na boki) */
    section[data-testid="stMain"] div[data-testid="stRadio"] > div {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        padding-bottom: 10px !important; /* miejsce na pasek przewijania */
        -webkit-overflow-scrolling: touch; /* płynne przewijanie na iOS */
    }
    
    /* 3. Zabezpieczamy przyciski przed ściśnięciem na pasku */
    section[data-testid="stMain"] div[data-testid="stRadio"] > div > label {
        flex: 0 0 auto !important; 
        padding: 8px 16px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- PAMIĘĆ APLIKACJI I LOGIKA PRZEŁĄCZANIA WIDOKÓW ---
if "edit_stale_id" not in st.session_state: st.session_state["edit_stale_id"] = None
if "edit_zmienne_id" not in st.session_state: st.session_state["edit_zmienne_id"] = None
if "edit_kategoria_id" not in st.session_state: st.session_state["edit_kategoria_id"] = None
if "edit_def_stale_id" not in st.session_state: st.session_state["edit_def_stale_id"] = None
if "pokaz_globalne" not in st.session_state: st.session_state["pokaz_globalne"] = False

# --- ZMIENNE GLOBALNE ---
LISTA_MIESIECY = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", 
                  "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]

# AKTUALIZACJA - Funkcja sprawdzająca czy pole jest faktycznie wypełnione (> 0)
def get_status_html(is_filled, netto=0.0, vat=0.0, label="Netto"):
    if is_filled:
        return f"<div style='background-color: #ECFDF5; padding: 6px 10px; border-radius: 6px; border: 1px solid #A7F3D0; font-weight: 600; color: #065F46; font-size: 13px; margin-bottom: 10px;'>✅ Zapisano: {label} {netto:.2f} PLN | VAT {vat:.2f} PLN</div>"
    else:
        return f"<div style='background-color: #FEF2F2; padding: 6px 10px; border-radius: 6px; border: 1px solid #FECACA; font-weight: 600; color: #991B1B; font-size: 13px; margin-bottom: 10px;'>⚠️ Brak danych! Uzupełnij kwoty.</div>"

# --- BAZY DANYCH I MIGACJA LAT ---
PLIK_LATA = "lata.csv"
PLIK_ZMIENNE = "moje_koszty.csv"
PLIK_STALE = "koszty_stale.csv"
PLIK_DEF_STALE = "definicje_stale.csv" 
PLIK_PODATKI = "podatki.csv"
PLIK_REKLAMA = "reklama.csv"
PLIK_ALLEGRO = "allegro.csv"
PLIK_INPOST = "inpost.csv"
PLIK_KATEGORIE = "kategorie.csv"
PLIK_ZAROBKI = "zarobki.csv" 

def load_data(file, cols):
    if os.path.exists(file): 
        df = pd.read_csv(file)
        if "Rok" in cols and "Rok" not in df.columns:
            df.insert(0, "Rok", 2024)
            df.to_csv(file, index=False)
        return df
    return pd.DataFrame(columns=cols)

df_lata = load_data(PLIK_LATA, ["Rok"])
if df_lata.empty:
    df_lata = pd.DataFrame([{"Rok": 2024}])
    df_lata.to_csv(PLIK_LATA, index=False)
lista_lat = sorted(df_lata["Rok"].astype(int).unique().tolist(), reverse=True)

if "ostatni_rok" not in st.session_state: st.session_state["ostatni_rok"] = lista_lat[0]

# --- PASEK BOCZNY ---
st.sidebar.header("🗓️ Rok rozliczeniowy")

wybrany_rok = st.sidebar.radio("Wybierz aktywny rok", lista_lat, index=0, horizontal=False, label_visibility="collapsed")

if wybrany_rok != st.session_state["ostatni_rok"]:
    st.session_state["pokaz_globalne"] = False
    st.session_state["ostatni_rok"] = wybrany_rok

st.sidebar.write("")
with st.sidebar.expander("⚙️ Dodaj nowy rok"):
    with st.form("form_nowy_rok", clear_on_submit=True):
        nowy_rok_input = st.number_input("Wpisz rok", min_value=2000, max_value=2100, step=None, format="%d")
        if st.form_submit_button("➕ Dodaj do bazy"):
            if nowy_rok_input not in lista_lat:
                df_lata = pd.concat([df_lata, pd.DataFrame([{"Rok": nowy_rok_input}])], ignore_index=True)
                df_lata.to_csv(PLIK_LATA, index=False)
                st.session_state["pokaz_globalne"] = False
                st.rerun()

st.sidebar.write("---")

if st.sidebar.button("📊 Podsumowanie Całościowe", use_container_width=True, type="primary"):
    st.session_state["pokaz_globalne"] = True

# Wczytywanie baz i aktualizacja schematu kategorii
df_zmienne = load_data(PLIK_ZMIENNE, ["Rok", "Miesiąc", "Nazwa", "Kwota", "Kategoria", "Kwota_Brutto"])
df_stale = load_data(PLIK_STALE, ["Rok", "Miesiąc", "Nazwa", "Kwota", "Kwota_Brutto"])
df_def_stale = load_data(PLIK_DEF_STALE, ["Rok", "Nazwa", "Miesiace"]) 
df_podatki = load_data(PLIK_PODATKI, ["Rok", "Miesiąc", "ZUS", "Podatek", "VAT"])
df_reklama = load_data(PLIK_REKLAMA, ["Rok", "Miesiąc", "Facebook_ADS", "Google_ADS", "Facebook_ADS_Brutto", "Google_ADS_Brutto"])
df_allegro = load_data(PLIK_ALLEGRO, ["Rok", "Miesiąc", "HannDesign", "HannDesign_pl", "HannDesign_Brutto", "HannDesign_pl_Brutto"])
df_inpost = load_data(PLIK_INPOST, ["Rok", "Miesiąc", "InPost_1", "InPost_2", "InPost_1_Brutto", "InPost_2_Brutto"])
df_zarobki = load_data(PLIK_ZAROBKI, ["Rok", "Miesiąc", "Dochod", "Przychod", "VAT", "Zysk"])

df_kategorie = load_data(PLIK_KATEGORIE, ["Nazwa", "Kolor"])
if df_kategorie.empty:
    df_kategorie = pd.DataFrame([{"Nazwa": k, "Kolor": "#f8fafc"} for k in ["Dom", "Własne", "Biuro", "Księgowość", "IT/Oprogramowanie", "Marketing", "Leasingi", "Inne"]])
    df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
else:
    if "Kolor" not in df_kategorie.columns:
        df_kategorie["Kolor"] = "#f8fafc"
        df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
    df_kategorie["Kolor"] = df_kategorie["Kolor"].fillna("#f8fafc")

LISTA_KATEGORII = df_kategorie["Nazwa"].tolist()


# ==========================================
# WIDOK SPECJALNY: PODSUMOWANIE GLOBALNE 
# ==========================================
if st.session_state["pokaz_globalne"]:
    st.title("Mój Firmowy Dashboard Kosztów 💰")
    st.write("---")
    st.subheader("🌐 Całościowe Podsumowanie Firmy (Wszystkie Lata)")
    
    all_stale_brutto = pd.to_numeric(df_stale["Kwota_Brutto"], errors='coerce').fillna(0).sum() if not df_stale.empty else 0.0
    all_zmienne_brutto = pd.to_numeric(df_zmienne["Kwota_Brutto"], errors='coerce').fillna(0).sum() if not df_zmienne.empty else 0.0
    all_zus = pd.to_numeric(df_podatki["ZUS"], errors='coerce').fillna(0).sum() if not df_podatki.empty else 0.0
    all_podatek = pd.to_numeric(df_podatki["Podatek"], errors='coerce').fillna(0).sum() if not df_podatki.empty else 0.0
    all_vat_koszt = pd.to_numeric(df_podatki["VAT"], errors='coerce').fillna(0).sum() if not df_podatki.empty else 0.0
    
    all_fb_b = pd.to_numeric(df_reklama["Facebook_ADS_Brutto"], errors='coerce').fillna(0).sum() if not df_reklama.empty else 0.0
    all_gg_b = pd.to_numeric(df_reklama["Google_ADS_Brutto"], errors='coerce').fillna(0).sum() if not df_reklama.empty else 0.0
    all_reklama_brutto = all_fb_b + all_gg_b
    
    all_allegro_brutto = (pd.to_numeric(df_allegro["HannDesign_Brutto"], errors='coerce').fillna(0).sum() + pd.to_numeric(df_allegro["HannDesign_pl_Brutto"], errors='coerce').fillna(0).sum()) if not df_allegro.empty else 0.0
    all_allegro_netto = (pd.to_numeric(df_allegro["HannDesign"], errors='coerce').fillna(0).sum() + pd.to_numeric(df_allegro["HannDesign_pl"], errors='coerce').fillna(0).sum()) if not df_allegro.empty else 0.0
    
    all_inpost_brutto = (pd.to_numeric(df_inpost["InPost_1_Brutto"], errors='coerce').fillna(0).sum() + pd.to_numeric(df_inpost["InPost_2_Brutto"], errors='coerce').fillna(0).sum()) if not df_inpost.empty else 0.0
    all_inpost_netto = (pd.to_numeric(df_inpost["InPost_1"], errors='coerce').fillna(0).sum() + pd.to_numeric(df_inpost["InPost_2"], errors='coerce').fillna(0).sum()) if not df_inpost.empty else 0.0
    
    all_przychod = pd.to_numeric(df_zarobki["Przychod"], errors='coerce').fillna(0).sum() if not df_zarobki.empty else 0.0
    all_dochod = pd.to_numeric(df_zarobki["Dochod"], errors='coerce').fillna(0).sum() if not df_zarobki.empty else 0.0
    
    all_suma_calkowita = all_stale_brutto + all_zmienne_brutto + all_zus + all_podatek + all_vat_koszt + all_reklama_brutto + all_allegro_brutto + all_inpost_brutto
    all_zysk_globalny = all_przychod - all_suma_calkowita

    col1, col2, col3, col_suma = st.columns(4)
    col1.metric("Wszystkie Koszty Stałe", f"{all_stale_brutto:.2f} PLN")
    col2.metric("Wszystkie Koszty Dodatk.", f"{all_zmienne_brutto:.2f} PLN")
    col3.metric("Cały ZUS i Podatki", f"{(all_zus + all_podatek + all_vat_koszt):.2f} PLN")
    col_suma.metric("GLOBALNY KOSZT (Wszystkie Lata)", f"{all_suma_calkowita:.2f} PLN")

    st.write("")
    col_tax1, col_tax2, col_tax3, col_ads, col_all, col_inp = st.columns(6)
    col_tax1.metric("Globalny ZUS", f"{all_zus:.2f} PLN")
    col_tax2.metric("Globalny Podatek", f"{all_podatek:.2f} PLN")
    col_tax3.metric("Globalny VAT (Koszty)", f"{all_vat_koszt:.2f} PLN")
    col_ads.metric("Globalna Reklama", f"{all_reklama_brutto:.2f} PLN")
    col_all.markdown(f"<div class=\"custom-metric\"><div style=\"font-size: 14px; color: rgba(49, 51, 63, 0.6); margin-bottom: 2px;\">Globalne Allegro</div><div style=\"font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 4px;\">Netto: {all_allegro_netto:.2f} PLN</div><div style=\"font-size: 1.8rem; color: rgb(49, 51, 63);\">{all_allegro_brutto:.2f} PLN</div></div>", unsafe_allow_html=True)
    col_inp.markdown(f"<div class=\"custom-metric\"><div style=\"font-size: 14px; color: rgba(49, 51, 63, 0.6); margin-bottom: 2px;\">Globalny InPost</div><div style=\"font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 4px;\">Netto: {all_inpost_netto:.2f} PLN</div><div style=\"font-size: 1.8rem; color: rgb(49, 51, 63);\">{all_inpost_brutto:.2f} PLN</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📈 Skumulowany Wynik Finansowy")
    col_p1, col_p2, col_p4 = st.columns(3)
    col_p1.metric("Globalny Przychód", f"{all_przychod:.2f} PLN")
    col_p2.metric("Globalny Dochód", f"{all_dochod:.2f} PLN")
    col_p4.metric("GLOBALNY ZYSK (Wszystkie Lata)", f"{all_zysk_globalny:.2f} PLN", delta=f"{all_zysk_globalny:.2f} PLN")
    
    st.write("---")
    if st.button("⬅️ Powrót do widoku rocznego"):
        st.session_state["pokaz_globalne"] = False
        st.rerun()

# ==========================================
# WIDOK STANDARDOWY: ZAKŁADKI (MIESIĄCE / ROK)
# ==========================================
else:
    st.title("Mój Firmowy Dashboard Kosztów 💰")

    df_zmienne_rok = df_zmienne[df_zmienne["Rok"] == wybrany_rok]
    df_stale_rok = df_stale[df_stale["Rok"] == wybrany_rok]
    df_podatki_rok = df_podatki[df_podatki["Rok"] == wybrany_rok]
    df_reklama_rok = df_reklama[df_reklama["Rok"] == wybrany_rok]
    df_allegro_rok = df_allegro[df_allegro["Rok"] == wybrany_rok]
    df_inpost_rok = df_inpost[df_inpost["Rok"] == wybrany_rok]
    df_zarobki_rok = df_zarobki[df_zarobki["Rok"] == wybrany_rok]

    if not df_stale_rok.empty:
        df_stale_rok.loc[:, "Kwota_Brutto"] = pd.to_numeric(df_stale_rok["Kwota_Brutto"], errors='coerce').fillna(0)
        df_stale_rok.loc[:, "Kwota"] = pd.to_numeric(df_stale_rok["Kwota"], errors='coerce').fillna(0)
        pure_stale_rok_brutto = df_stale_rok["Kwota_Brutto"].sum()
    else: 
        pure_stale_rok_brutto = 0.0

    suma_zmienne_rok_brutto = df_zmienne_rok["Kwota_Brutto"].sum() if not df_zmienne_rok.empty else 0.0

    roczny_zus = df_podatki_rok["ZUS"].sum() if not df_podatki_rok.empty else 0.0
    roczny_podatek = df_podatki_rok["Podatek"].sum() if not df_podatki_rok.empty else 0.0
    roczny_vat_koszt = df_podatki_rok["VAT"].sum() if not df_podatki_rok.empty else 0.0

    roczny_fb_n = df_reklama_rok["Facebook_ADS"].sum() if not df_reklama_rok.empty else 0.0
    roczny_google_n = df_reklama_rok["Google_ADS"].sum() if not df_reklama_rok.empty else 0.0
    roczna_reklama_netto = roczny_fb_n + roczny_google_n

    roczny_fb_b = df_reklama_rok["Facebook_ADS_Brutto"].sum() if not df_reklama_rok.empty else 0.0
    roczny_google_b = df_reklama_rok["Google_ADS_Brutto"].sum() if not df_reklama_rok.empty else 0.0
    roczna_reklama_brutto = roczny_fb_b + roczny_google_b

    roczne_allegro_netto = (df_allegro_rok["HannDesign"].sum() + df_allegro_rok["HannDesign_pl"].sum()) if not df_allegro_rok.empty else 0.0
    roczne_allegro_brutto = (df_allegro_rok["HannDesign_Brutto"].sum() + df_allegro_rok["HannDesign_pl_Brutto"].sum()) if not df_allegro_rok.empty else 0.0

    roczne_inpost_netto = (df_inpost_rok["InPost_1"].sum() + df_inpost_rok["InPost_2"].sum()) if not df_inpost_rok.empty else 0.0
    roczne_inpost_brutto = (df_inpost_rok["InPost_1_Brutto"].sum() + df_inpost_rok["InPost_2_Brutto"].sum()) if not df_inpost_rok.empty else 0.0

    roczny_przychod = df_zarobki_rok["Przychod"].sum() if not df_zarobki_rok.empty else 0.0
    roczny_dochod = df_zarobki_rok["Dochod"].sum() if not df_zarobki_rok.empty else 0.0

    suma_stale_rok = pure_stale_rok_brutto + suma_zmienne_rok_brutto + roczny_zus + roczny_podatek + roczny_vat_koszt + roczna_reklama_brutto + roczne_allegro_brutto + roczne_inpost_brutto
    suma_calkowita_rok = pure_stale_rok_brutto + suma_zmienne_rok_brutto + roczny_zus + roczny_podatek + roczny_vat_koszt + roczna_reklama_brutto + roczne_allegro_brutto + roczne_inpost_brutto
    roczny_zysk_globalny = roczny_przychod - suma_calkowita_rok

    # --- MENU GŁÓWNE ---
    opcje_menu = ["📊 Podsumowanie"] + LISTA_MIESIECY
    wybor = st.radio("Zakładki", opcje_menu, horizontal=True, label_visibility="collapsed")

    if wybor == "📊 Podsumowanie":
        st.write("---")
        st.subheader(f"🌍 Podsumowanie Firmy (Rok {wybrany_rok})")
        col1, col2, col3, col_suma = st.columns(4)
        col1.metric("Koszty Stałe", f"{suma_stale_rok:.2f} PLN")
        col2.metric("Koszty Dodatkowe", f"{suma_zmienne_rok_brutto:.2f} PLN")
        col3.metric("ZUS i Podatki", f"{(roczny_zus + roczny_podatek + roczny_vat_koszt):.2f} PLN")
        col_suma.metric("ŁĄCZNY KOSZT ROCZNY", f"{suma_calkowita_rok:.2f} PLN")

        st.write("")
        col_tax1, col_tax2, col_tax3, col_ads, col_all, col_inp = st.columns(6)
        col_tax1.metric("Roczny ZUS", f"{roczny_zus:.2f} PLN")
        col_tax2.metric("Roczny Podatek", f"{roczny_podatek:.2f} PLN")
        col_tax3.metric("Roczny VAT (Koszty)", f"{roczny_vat_koszt:.2f} PLN")

        col_ads.metric("Roczna Reklama", f"{roczna_reklama_brutto:.2f} PLN")

        col_all.markdown(f"<div class=\"custom-metric\"><div style=\"font-size: 14px; color: rgba(49, 51, 63, 0.6); margin-bottom: 2px;\">Roczne Allegro</div><div style=\"font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 4px;\">Netto: {roczne_allegro_netto:.2f} PLN</div><div style=\"font-size: 1.8rem; color: rgb(49, 51, 63);\">{roczne_allegro_brutto:.2f} PLN</div></div>", unsafe_allow_html=True)
        col_inp.markdown(f"<div class=\"custom-metric\"><div style=\"font-size: 14px; color: rgba(49, 51, 63, 0.6); margin-bottom: 2px;\">Roczny InPost</div><div style=\"font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 4px;\">Netto: {roczne_inpost_netto:.2f} PLN</div><div style=\"font-size: 1.8rem; color: rgb(49, 51, 63);\">{roczne_inpost_brutto:.2f} PLN</div></div>", unsafe_allow_html=True)

        st.write("")
        st.markdown(f"#### 📈 Wynik Finansowy Firmy (Rok {wybrany_rok})")
        col_p1, col_p2, col_p4 = st.columns(3)
        col_p1.metric("Przychód", f"{roczny_przychod:.2f} PLN")
        col_p2.metric("Dochód", f"{roczny_dochod:.2f} PLN")
        col_p4.metric("REALNY ZYSK", f"{roczny_zysk_globalny:.2f} PLN", delta=f"{roczny_zysk_globalny:.2f} PLN")
        
        st.write("---")
        
        # --- ZARZĄDZANIE KOSZTAMI STAŁYMI ---
        st.subheader("📌 Szablony Kosztów Stałych (Automatyzacja)")
        col_def_lewa, col_def_prawa = st.columns([1.5, 2.5])
        
        with col_def_lewa:
            with st.form("form_nowa_def_stale", clear_on_submit=True):
                nowa_def_nazwa = st.text_input("Nazwa stałego kosztu", placeholder="np. Księgowość, Leasing...")
                nowe_def_miesiace = st.multiselect("Wybierz miesiące przydziału", LISTA_MIESIECY, default=LISTA_MIESIECY)
                zapisz_def = st.form_submit_button("➕ Dodaj do listy")
                
                if zapisz_def and nowa_def_nazwa.strip() != "":
                    if nowa_def_nazwa.strip() not in df_def_stale[df_def_stale["Rok"] == wybrany_rok]["Nazwa"].values:
                        miesiace_str = "|".join(nowe_def_miesiace)
                        nowy_wiersz = pd.DataFrame([{"Rok": wybrany_rok, "Nazwa": nowa_def_nazwa.strip(), "Miesiace": miesiace_str}])
                        df_def_stale = pd.concat([df_def_stale, nowy_wiersz], ignore_index=True)
                        df_def_stale.to_csv(PLIK_DEF_STALE, index=False)
                        st.rerun()
                    else:
                        st.error("Szablon o tej nazwie już istnieje w tym roku!")

        with col_def_prawa:
            st.markdown(f"#### Zdefiniowane szablony w {wybrany_rok} roku")
            df_def_rok = df_def_stale[df_def_stale["Rok"] == wybrany_rok]
            
            if not df_def_rok.empty:
                for i, (index, row) in enumerate(df_def_rok.iterrows()):
                    if st.session_state["edit_def_stale_id"] == index:
                        with st.form(key=f"edit_form_def_{index}"):
                            e_def_nazwa = st.text_input("Zmień nazwę", value=row["Nazwa"])
                            stare_miesiace = str(row["Miesiace"]).split("|") if pd.notna(row["Miesiace"]) else LISTA_MIESIECY
                            e_def_miesiace = st.multiselect("Miesiące", LISTA_MIESIECY, default=stare_miesiace)
                            c_db1, c_db2 = st.columns(2)
                            if c_db1.form_submit_button("💾 Zapisz"):
                                df_def_stale.at[index, "Nazwa"] = e_def_nazwa.strip()
                                df_def_stale.at[index, "Miesiace"] = "|".join(e_def_miesiace)
                                df_def_stale.to_csv(PLIK_DEF_STALE, index=False)
                                st.session_state["edit_def_stale_id"] = None
                                st.rerun()
                            if c_db2.form_submit_button("❌ Anuluj"):
                                st.session_state["edit_def_stale_id"] = None
                                st.rerun()
                    else:
                        c1, c_up, c_dn, c_ed, c_del = st.columns([3.5, 0.4, 0.4, 0.4, 0.4])
                        mies_list = str(row['Miesiace']).replace('|', ', ')
                        c1.markdown(f"<div style='background-color: #f1f5f9; padding: 8px 12px; border-radius: 6px; border: 1px solid #cbd5e1; margin-bottom: 8px;'><b style='color:#0f172a;'>{row['Nazwa']}</b><br><span style='color: #475569; font-size: 13px;'>{mies_list}</span></div>", unsafe_allow_html=True)
                        
                        if c_up.button("⬆️", key=f"up_def_{index}"):
                            if i > 0:
                                prev_index = df_def_rok.index[i-1]
                                temp = df_def_stale.loc[index].copy()
                                df_def_stale.loc[index] = df_def_stale.loc[prev_index]
                                df_def_stale.loc[prev_index] = temp
                                df_def_stale.to_csv(PLIK_DEF_STALE, index=False)
                                st.rerun()
                                
                        if c_dn.button("⬇️", key=f"dn_def_{index}"):
                            if i < len(df_def_rok) - 1:
                                next_index = df_def_rok.index[i+1]
                                temp = df_def_stale.loc[index].copy()
                                df_def_stale.loc[index] = df_def_stale.loc[next_index]
                                df_def_stale.loc[next_index] = temp
                                df_def_stale.to_csv(PLIK_DEF_STALE, index=False)
                                st.rerun()

                        if c_ed.button("✏️", key=f"edit_def_{index}"):
                            st.session_state["edit_def_stale_id"] = index
                            st.rerun()
                        if c_del.button("🗑️", key=f"del_def_{index}"):
                            df_def_stale.drop(index).to_csv(PLIK_DEF_STALE, index=False)
                            st.rerun()
            else:
                st.info("Brak zdefiniowanych szablonów kosztów stałych na ten rok.")
                
            st.write("---")
            st.markdown("#### 📊 Małe podsumowanie opłaconych kosztów stałych")
            if not df_stale_rok.empty:
                df_stale_sum = df_stale_rok.groupby("Nazwa").agg({"Kwota": "sum", "Kwota_Brutto": "sum"}).reset_index()
                df_stale_sum["Suma VAT"] = (df_stale_sum["Kwota_Brutto"] - df_stale_sum["Kwota"]).round(2)
                df_stale_sum = df_stale_sum.rename(columns={"Nazwa": "Nazwa kosztu stałego", "Kwota": "Suma Netto (PLN)", "Kwota_Brutto": "Suma Brutto (PLN)"})
                df_stale_sum = df_stale_sum[["Nazwa kosztu stałego", "Suma Netto (PLN)", "Suma Brutto (PLN)", "Suma VAT"]]
                st.dataframe(df_stale_sum, hide_index=True, use_container_width=True)
            else:
                st.info("Brak opłaconych kosztów stałych do zliczenia w tym roku.")

        st.write("---")

        # --- ZARZĄDZANIE KATEGORIAMI ---
        st.subheader("🗂️ Zarządzaj Kategoriami (Koszty Dodatkowe)")
        col_kat_lewa, col_kat_prawa = st.columns([1.5, 2.5])
        
        with col_kat_lewa:
            with st.form("form_nowa_kategoria", clear_on_submit=True):
                nowa_kat_nazwa = st.text_input("Nazwa nowej kategorii", placeholder="np. Wyposażenie")
                nowy_kolor_kat = st.color_picker("Kolor podświetlenia wiersza", "#f8fafc")
                zapisz_kat = st.form_submit_button("➕ Dodaj kategorię")
                
            if zapisz_kat and nowa_kat_nazwa.strip() != "":
                if nowa_kat_nazwa.strip() not in LISTA_KATEGORII:
                    nowy_wiersz_kat = pd.DataFrame([{"Nazwa": nowa_kat_nazwa.strip(), "Kolor": nowy_kolor_kat}])
                    df_kategorie = pd.concat([df_kategorie, nowy_wiersz_kat], ignore_index=True)
                    df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
                    st.rerun()
                else: st.error("Taka kategoria już istnieje!")

        with col_kat_prawa:
            st.markdown("#### Twoja lista kategorii (Wspólna dla wszystkich lat)")
            if not df_kategorie.empty:
                for i, (index, row) in enumerate(df_kategorie.iterrows()):
                    if st.session_state["edit_kategoria_id"] == index:
                        with st.form(key=f"edit_form_kat_{index}"):
                            e_kat_nazwa = st.text_input("Zmień nazwę", value=row["Nazwa"])
                            e_kat_kolor = st.color_picker("Zmień kolor wiersza", value=row.get("Kolor", "#f8fafc"))
                            c_kb1, c_kb2 = st.columns(2)
                            if c_kb1.form_submit_button("💾 Zapisz"):
                                df_kategorie.at[index, "Nazwa"] = e_kat_nazwa.strip()
                                df_kategorie.at[index, "Kolor"] = e_kat_kolor
                                df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
                                st.session_state["edit_kategoria_id"] = None
                                st.rerun()
                            if c_kb2.form_submit_button("❌ Anuluj"):
                                st.session_state["edit_kategoria_id"] = None
                                st.rerun()
                    else:
                        ck1, ck_up, ck_dn, ck_ed, ck_del = st.columns([3, 0.5, 0.5, 0.5, 0.5])
                        bg_k_color = row.get("Kolor", "#f8fafc")
                        ck1.markdown(f"<div style='background-color: {bg_k_color}; padding: 6px 12px; border-radius: 4px; border: 1px solid #e2e8f0; margin-bottom: 8px;'>{row['Nazwa']}</div>", unsafe_allow_html=True)
                        
                        if ck_up.button("⬆️", key=f"up_kat_{index}"):
                            if i > 0:
                                prev_index = df_kategorie.index[i-1]
                                temp = df_kategorie.loc[index].copy()
                                df_kategorie.loc[index] = df_kategorie.loc[prev_index]
                                df_kategorie.loc[prev_index] = temp
                                df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
                                st.rerun()
                                
                        if ck_dn.button("⬇️", key=f"dn_kat_{index}"):
                            if i < len(df_kategorie) - 1:
                                next_index = df_kategorie.index[i+1]
                                temp = df_kategorie.loc[index].copy()
                                df_kategorie.loc[index] = df_kategorie.loc[next_index]
                                df_kategorie.loc[next_index] = temp
                                df_kategorie.to_csv(PLIK_KATEGORIE, index=False)
                                st.rerun()

                        if ck_ed.button("✏️", key=f"edit_kat_{index}"): 
                            st.session_state["edit_kategoria_id"] = index
                            st.rerun()
                        if ck_del.button("🗑️", key=f"del_kat_{index}"):
                            df_kategorie.drop(index).to_csv(PLIK_KATEGORIE, index=False)
                            st.session_state["edit_kategoria_id"] = None
                            st.rerun()

    else:
        wybrany_miesiac = wybor
        st.subheader(f"📅 Pulpit miesiąca: {wybrany_miesiac} {wybrany_rok}")
        
        def get_val(df, m): return df[df["Miesiąc"] == m].iloc[0] if not df.empty and m in df["Miesiąc"].values else None
        
        p_row = get_val(df_podatki_rok, wybrany_miesiac)
        m_zus, m_pod, m_vat = (p_row["ZUS"], p_row["Podatek"], p_row["VAT"]) if p_row is not None else (0,0,0)
        
        r_row = get_val(df_reklama_rok, wybrany_miesiac)
        m_fb = r_row["Facebook_ADS"] if r_row is not None else 0.0
        m_gg = r_row["Google_ADS"] if r_row is not None else 0.0
        m_fb_b = r_row["Facebook_ADS_Brutto"] if r_row is not None else 0.0
        m_gg_b = r_row["Google_ADS_Brutto"] if r_row is not None else 0.0
        
        z_row = get_val(df_zarobki_rok, wybrany_miesiac)
        m_dochod, m_przychod, m_vat_zarobek, m_zysk = (z_row["Dochod"], z_row["Przychod"], z_row["VAT"], z_row["Zysk"]) if z_row is not None else (0,0,0,0)

        df_stale_m = df_stale_rok[df_stale_rok["Miesiąc"] == wybrany_miesiac] if not df_stale_rok.empty else df_stale_rok
        s_stale_brutto = df_stale_m["Kwota_Brutto"].sum() if not df_stale_m.empty else 0.0
        
        df_zm_m = df_zmienne_rok[df_zmienne_rok["Miesiąc"] == wybrany_miesiac]
        s_zmienne_brutto = df_zm_m["Kwota_Brutto"].sum() if not df_zm_m.empty else 0.0
        
        a_row = get_val(df_allegro_rok, wybrany_miesiac)
        m_h_b = a_row["HannDesign_Brutto"] if a_row is not None else 0.0
        m_hp_b = a_row["HannDesign_pl_Brutto"] if a_row is not None else 0.0
        m_h = a_row["HannDesign"] if a_row is not None else 0.0
        m_hp = a_row["HannDesign_pl"] if a_row is not None else 0.0
        
        i_row = get_val(df_inpost_rok, wybrany_miesiac)
        m_i1_b = i_row["InPost_1_Brutto"] if i_row is not None else 0.0
        m_i2_b = i_row["InPost_2_Brutto"] if i_row is not None else 0.0
        m_i1 = i_row["InPost_1"] if i_row is not None else 0.0
        m_i2 = i_row["InPost_2"] if i_row is not None else 0.0

        suma_kosztow_m = s_stale_brutto + s_zmienne_brutto + m_zus + m_pod + m_vat + m_fb_b + m_gg_b + m_h_b + m_hp_b + m_i1_b + m_i2_b
        aktualny_zysk_m = m_przychod - suma_kosztow_m
        m_vat_pulpit_obliczony = m_przychod - m_dochod

        col_a, col_b, col_c, col_vat, col_d = st.columns(5)
        col_a.metric("Wszystkie Koszty Miesiąca", f"{suma_kosztow_m:.2f} PLN")
        col_b.metric("Miesięczny Przychód", f"{m_przychod:.2f} PLN")
        col_c.metric("Miesięczny Dochód", f"{m_dochod:.2f} PLN")
        col_vat.metric("VAT", f"{m_vat_pulpit_obliczony:.2f} PLN")
        col_d.metric("REALNY ZYSK MIESIĄCA", f"{aktualny_zysk_m:.2f} PLN", delta=f"{aktualny_zysk_m:.2f} PLN")
        
        st.write("---")
        
        st.subheader("💰 Zarobki")
        if z_row is not None and m_przychod > 0:
            st.markdown(f"<div style='background-color: #ECFDF5; padding: 8px 12px; border-radius: 6px; border: 1px solid #A7F3D0; font-weight: bold; color: #065F46; font-size: 14px; margin-bottom: 10px;'>✅ Zapisano Przychód w wysokości {m_przychod:.2f} PLN</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #FEF2F2; padding: 8px 12px; border-radius: 6px; border: 1px solid #FECACA; font-weight: bold; color: #991B1B; font-size: 14px; margin-bottom: 10px;'>⚠️ Brak danych! Uzupełnij zarobki dla tego miesiąca.</div>", unsafe_allow_html=True)

        with st.form(f"form_zarobki_{wybrany_miesiac}"):
            input_przychod = st.number_input("Przychód (PLN)", min_value=0.0, format="%.2f", value=float(m_przychod), step=None)
            cb_1, cb_2 = st.columns([1, 4])
            zapisz_zarobki = cb_1.form_submit_button("Zapisz Przychód")
            reset_zarobki = cb_2.form_submit_button("🗑️ Wyczyszcz Zarobki")
            
        if zapisz_zarobki:
            wyliczony_dochod = round(input_przychod / 1.23, 2)
            wyliczony_vat_z = round(input_przychod - wyliczony_dochod, 2)
            new_zarobki = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "Dochod": wyliczony_dochod, "Przychod": input_przychod, "VAT": wyliczony_vat_z, "Zysk": 0.0}])
            df_zarobki = df_zarobki[~((df_zarobki["Rok"] == wybrany_rok) & (df_zarobki["Miesiąc"] == wybrany_miesiac))]
            df_zarobki = pd.concat([df_zarobki, new_zarobki])
            df_zarobki.to_csv(PLIK_ZAROBKI, index=False)
            st.rerun()
            
        if reset_zarobki:
            df_zarobki = df_zarobki[~((df_zarobki["Rok"] == wybrany_rok) & (df_zarobki["Miesiąc"] == wybrany_miesiac))]
            df_zarobki.to_csv(PLIK_ZAROBKI, index=False)
            st.rerun()

        st.write("---")
        
        st.subheader("⚙️ Koszty stałe (zdefiniowane szablony)")

        col_st1, col_st2, col_st3, col_st4, col_st5 = st.columns([3.5, 1.5, 1.5, 1.5, 2])
        col_st1.markdown("**Nazwa**")
        col_st2.markdown("**Kwota Brutto**")
        col_st3.markdown("**Kwota Netto**")
        col_st4.markdown("**VAT**")
        col_st5.markdown("**Akcje**")

        wymagane_stale = df_def_stale[(df_def_stale["Rok"] == wybrany_rok) & (df_def_stale["Miesiace"].astype(str).str.contains(wybrany_miesiac))]
        lista_wymaganych = wymagane_stale["Nazwa"].tolist() if not wymagane_stale.empty else []
        lista_zapisanych = df_stale_m["Nazwa"].tolist() if not df_stale_m.empty else []
        
        wszystkie_nazwy_stale = list(set(lista_wymaganych + lista_zapisanych))
        wszystkie_nazwy_stale.sort()

        if wszystkie_nazwy_stale:
            for i, nazwa in enumerate(wszystkie_nazwy_stale):
                saved_row = df_stale_m[df_stale_m["Nazwa"] == nazwa]
                is_saved = not saved_row.empty
                idx = saved_row.index[0] if is_saved else f"new_{nazwa}"
                
                if st.session_state["edit_stale_id"] == idx:
                    with st.form(key=f"es_{idx}"):
                        c_es1, c_es2, c_es3, c_es4, c_es5 = st.columns([3.5, 1.5, 1.5, 1.5, 2])
                        c_es1.markdown(f"<div style='padding-top:8px; font-weight:bold; color:#1E40AF;'>{nazwa}</div>", unsafe_allow_html=True)
                        
                        def_b = float(saved_row.iloc[0]["Kwota_Brutto"]) if is_saved else 0.0
                        def_n = float(saved_row.iloc[0]["Kwota"]) if is_saved else 0.0
                        
                        ek_s_b = c_es2.number_input("Kwota Brutto", value=def_b, label_visibility="collapsed", step=None)
                        ek_s_n = c_es3.number_input("Kwota Netto", value=def_n, label_visibility="collapsed", step=None)
                        c_es4.markdown("<div style='padding-top:8px; color:gray; text-align:center;'>Auto</div>", unsafe_allow_html=True)
                        
                        if c_es5.form_submit_button("💾 Zapisz"):
                            final_n = ek_s_n if ek_s_n > 0 else round(ek_s_b / 1.23, 2)
                            final_b = ek_s_b if ek_s_b > 0 else round(final_n * 1.23, 2)
                            
                            if is_saved:
                                df_stale.at[idx, "Kwota"] = final_n
                                df_stale.at[idx, "Kwota_Brutto"] = final_b
                                df_stale.to_csv(PLIK_STALE, index=False)
                            else:
                                new_s = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "Nazwa": nazwa, "Kwota": final_n, "Kwota_Brutto": final_b}])
                                df_stale = pd.concat([df_stale, new_s], ignore_index=True)
                                df_stale.to_csv(PLIK_STALE, index=False)
                                
                            st.session_state["edit_stale_id"] = None
                            st.rerun()
                else:
                    s_n_val = float(saved_row.iloc[0]["Kwota"]) if is_saved else 0.0
                    s_b_val = float(saved_row.iloc[0]["Kwota_Brutto"]) if is_saved else 0.0
                    s_v_val = round(s_b_val - s_n_val, 2)
                    
                    bg_color = "#f8fafc" if i % 2 == 0 else "#ffffff"
                    status_color = "#000000"
                    prefix = ""
                    
                    if not is_saved:
                        bg_color = "#FEF2F2"
                        status_color = "#991B1B"
                        prefix = "⚠️ Brak kwoty: "
                        
                    cell_style = f"background-color: {bg_color}; padding: 8px 12px; border-radius: 4px; border: 1px solid #e2e8f0; color: {status_color}; min-height: 40px; display: flex; align-items: center;"
                    
                    c1, c2, c3, c4, c5 = st.columns([3.5, 1.5, 1.5, 1.5, 2])
                    c1.markdown(f"<div style='{cell_style}'>{prefix}<b>{nazwa}</b></div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='{cell_style}'>{s_b_val:.2f} PLN</div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='{cell_style}'>{s_n_val:.2f} PLN</div>", unsafe_allow_html=True)
                    c4.markdown(f"<div style='{cell_style}'>{s_v_val:.2f} PLN</div>", unsafe_allow_html=True)
                    
                    with c5:
                        btn1, btn2 = st.columns(2)
                        if is_saved:
                            if btn1.button("✏️", key=f"esb_{idx}"): st.session_state["edit_stale_id"] = idx; st.rerun()
                            if btn2.button("🗑️", key=f"dsb_{idx}"): 
                                df_stale = df_stale.drop(idx)
                                df_stale.to_csv(PLIK_STALE, index=False)
                                st.session_state["edit_stale_id"] = None
                                st.rerun()
                        else:
                            if btn1.button("✍️ Uzupełnij", key=f"esb_{idx}"): st.session_state["edit_stale_id"] = idx; st.rerun()
        else:
            st.info("💡 Brak przypisanych szablonów kosztów stałych do tego miesiąca. Zdefiniuj je w zakładce '📊 Podsumowanie'.")

        if not df_stale_m.empty:
            total_s_m_netto = df_stale_m["Kwota"].sum()
            total_s_m_brutto = df_stale_m["Kwota_Brutto"].sum()
            total_s_m_vat = round(total_s_m_brutto - total_s_m_netto, 2)
            
            st.write("")
            c_ts1, c_ts2, c_ts3, c_ts4, c_ts5 = st.columns([3.5, 1.5, 1.5, 1.5, 2])
            summary_style = "background-color: #e2e8f0; padding: 8px 12px; border-radius: 4px; font-weight: bold; color: #000000; min-height: 40px; display: flex; align-items: center;"
            c_ts1.markdown(f"<div style='{summary_style}'>RAZEM OPŁACONE:</div>", unsafe_allow_html=True)
            c_ts2.markdown(f"<div style='{summary_style}'>{total_s_m_brutto:.2f} PLN</div>", unsafe_allow_html=True)
            c_ts3.markdown(f"<div style='{summary_style}'>{total_s_m_netto:.2f} PLN</div>", unsafe_allow_html=True)
            c_ts4.markdown(f"<div style='{summary_style}'>{total_s_m_vat:.2f} PLN</div>", unsafe_allow_html=True)
            with c_ts5:
                if st.button("🗑️ Wyczyść Wszystkie", key=f"del_all_s_{wybrany_miesiac}"):
                    df_stale = df_stale[~((df_stale["Rok"] == wybrany_rok) & (df_stale["Miesiąc"] == wybrany_miesiac))]
                    df_stale.to_csv(PLIK_STALE, index=False)
                    st.rerun()

        st.write("---")

        v_fb = round(m_fb_b - m_fb, 2)
        v_gg = round(m_gg_b - m_gg, 2)
        v_h = round(m_h_b - m_h, 2)
        v_hp = round(m_hp_b - m_hp, 2)
        v_i1 = round(m_i1_b - m_i1, 2)
        v_i2 = round(m_i2_b - m_i2, 2)
        
        v_zmienne = (df_zm_m["Kwota_Brutto"] - df_zm_m["Kwota"]).sum() if not df_zm_m.empty else 0.0
        v_stale = (df_stale_m["Kwota_Brutto"] - df_stale_m["Kwota"]).sum() if not df_stale_m.empty else 0.0

        sugerowany_podatek = m_dochod * 0.03
        sugerowany_vat = m_vat_pulpit_obliczony - v_fb - v_gg - v_h - v_hp - v_i1 - v_i2 - v_zmienne - v_stale

        st.subheader("🏛️ Podatki")
        if p_row is not None and (m_zus > 0 or m_pod > 0 or m_vat > 0):
            st.markdown(f"<div style='background-color: #ECFDF5; padding: 8px 12px; border-radius: 6px; border: 1px solid #A7F3D0; font-weight: bold; color: #065F46; font-size: 14px; margin-bottom: 10px;'>✅ Zapisano ZUS: {m_zus:.2f} PLN | Podatek: {m_pod:.2f} PLN | VAT: {m_vat:.2f} PLN</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #FEF2F2; padding: 8px 12px; border-radius: 6px; border: 1px solid #FECACA; font-weight: bold; color: #991B1B; font-size: 14px; margin-bottom: 10px;'>⚠️ Brak wprowadzonych podatków! Uzupełnij dane.</div>", unsafe_allow_html=True)

        with st.form(f"f_pod_{wybrany_miesiac}"):
            cz, cp, cv = st.columns(3)
            nz = cz.number_input("ZUS", value=float(m_zus), step=None)
            np = cp.number_input(f"Podatek (sugerowany: {sugerowany_podatek:.2f})", value=float(m_pod), step=None)
            nv = cv.number_input(f"VAT (sugerowany: {sugerowany_vat:.2f})", value=float(m_vat), step=None)
            
            cb_p1, cb_p2 = st.columns([1, 4])
            zapisz_podatki = cb_p1.form_submit_button("Zapisz Podatki")
            reset_podatki = cb_p2.form_submit_button("🗑️ Wyzeruj Podatki")
            
        if zapisz_podatki:
            new = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "ZUS": nz, "Podatek": np, "VAT": nv}])
            df_podatki = df_podatki[~((df_podatki["Rok"] == wybrany_rok) & (df_podatki["Miesiąc"] == wybrany_miesiac))]
            pd.concat([df_podatki, new]).to_csv(PLIK_PODATKI, index=False)
            st.rerun()
            
        if reset_podatki:
            df_podatki = df_podatki[~((df_podatki["Rok"] == wybrany_rok) & (df_podatki["Miesiąc"] == wybrany_miesiac))]
            df_podatki.to_csv(PLIK_PODATKI, index=False)
            st.rerun()

        st.write("---")

        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            st.subheader("📢 Reklama")
            with st.form(f"f_rek_{wybrany_miesiac}"):
                st.markdown("**Facebook ADS**")
                col_fb_b, col_fb_n = st.columns(2)
                fb_b = col_fb_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_fb_b), key=f"fb_b_{wybrany_miesiac}", step=None)
                fb_n = col_fb_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"fb_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(r_row is not None and m_fb > 0, m_fb, v_fb, "FB Netto:"), unsafe_allow_html=True)
                
                st.markdown("**Google ADS**")
                col_gg_b, col_gg_n = st.columns(2)
                gg_b = col_gg_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_gg_b), key=f"gg_b_{wybrany_miesiac}", step=None)
                gg_n = col_gg_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"gg_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(r_row is not None and m_gg > 0, m_gg, v_gg, "Google Netto:"), unsafe_allow_html=True)
                
                cb_r1, cb_r2 = st.columns([1, 2])
                zapisz_reklamy = cb_r1.form_submit_button("Zapisz")
                reset_reklamy = cb_r2.form_submit_button("🗑️ Wyzeruj")
                
                if zapisz_reklamy:
                    final_fb_n = fb_n if fb_n > 0 else round(fb_b / 1.23, 2)
                    final_fb_b = fb_b if fb_b > 0 else round(final_fb_n * 1.23, 2)
                    final_gg_n = gg_n if gg_n > 0 else round(gg_b / 1.23, 2)
                    final_gg_b = gg_b if gg_b > 0 else round(final_gg_n * 1.23, 2)
                    new = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "Facebook_ADS": final_fb_n, "Google_ADS": final_gg_n, "Facebook_ADS_Brutto": final_fb_b, "Google_ADS_Brutto": final_gg_b}])
                    df_reklama = df_reklama[~((df_reklama["Rok"] == wybrany_rok) & (df_reklama["Miesiąc"] == wybrany_miesiac))]
                    pd.concat([df_reklama, new]).to_csv(PLIK_REKLAMA, index=False)
                    st.rerun()
                    
                if reset_reklamy:
                    df_reklama = df_reklama[~((df_reklama["Rok"] == wybrany_rok) & (df_reklama["Miesiąc"] == wybrany_miesiac))]
                    df_reklama.to_csv(PLIK_REKLAMA, index=False)
                    st.rerun()

        with cf2:
            st.subheader("🛒 Allegro")
            with st.form(f"f_all_{wybrany_miesiac}"):
                st.markdown("**HannDesign**")
                col_h_b, col_h_n = st.columns(2)
                h_b = col_h_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_h_b), key=f"h_b_{wybrany_miesiac}", step=None)
                h_n = col_h_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"h_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(a_row is not None and m_h > 0, m_h, v_h, "Hann Netto:"), unsafe_allow_html=True)
                
                st.markdown("**HannDesign_pl**")
                col_hp_b, col_hp_n = st.columns(2)
                hp_b = col_hp_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_hp_b), key=f"hp_b_{wybrany_miesiac}", step=None)
                hp_n = col_hp_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"hp_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(a_row is not None and m_hp > 0, m_hp, v_hp, "Hann_pl Netto:"), unsafe_allow_html=True)
                
                cb_a1, cb_a2 = st.columns([1, 2])
                zapisz_allegro = cb_a1.form_submit_button("Zapisz")
                reset_allegro = cb_a2.form_submit_button("🗑️ Wyzeruj")
                
                if zapisz_allegro:
                    final_h_n = h_n if h_n > 0 else round(h_b / 1.23, 2)
                    final_h_b = h_b if h_b > 0 else round(final_h_n * 1.23, 2)
                    final_hp_n = hp_n if hp_n > 0 else round(hp_b / 1.23, 2)
                    final_hp_b = hp_b if hp_b > 0 else round(final_hp_n * 1.23, 2)
                    new = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "HannDesign": final_h_n, "HannDesign_pl": final_hp_n, "HannDesign_Brutto": final_h_b, "HannDesign_pl_Brutto": final_hp_b}])
                    df_allegro = df_allegro[~((df_allegro["Rok"] == wybrany_rok) & (df_allegro["Miesiąc"] == wybrany_miesiac))]
                    pd.concat([df_allegro, new]).to_csv(PLIK_ALLEGRO, index=False)
                    st.rerun()
                    
                if reset_allegro:
                    df_allegro = df_allegro[~((df_allegro["Rok"] == wybrany_rok) & (df_allegro["Miesiąc"] == wybrany_miesiac))]
                    df_allegro.to_csv(PLIK_ALLEGRO, index=False)
                    st.rerun()

        with cf3:
            st.subheader("📦 InPost")
            with st.form(f"f_inp_{wybrany_miesiac}"):
                st.markdown("**InPost 1**")
                col_i1_b, col_i1_n = st.columns(2)
                i1_b = col_i1_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_i1_b), key=f"i1_b_{wybrany_miesiac}", step=None)
                i1_n = col_i1_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"i1_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(i_row is not None and m_i1 > 0, m_i1, v_i1, "InPost 1 Netto:"), unsafe_allow_html=True)
                
                st.markdown("**InPost 2**")
                col_i2_b, col_i2_n = st.columns(2)
                i2_b = col_i2_b.number_input("Kwota Brutto", min_value=0.0, format="%.2f", value=float(m_i2_b), key=f"i2_b_{wybrany_miesiac}", step=None)
                i2_n = col_i2_n.number_input("Kwota Netto (0.00 dla auto)", min_value=0.0, format="%.2f", value=0.0, key=f"i2_n_{wybrany_miesiac}", step=None)
                st.markdown(get_status_html(i_row is not None and m_i2 > 0, m_i2, v_i2, "InPost 2 Netto:"), unsafe_allow_html=True)
                
                cb_i1, cb_i2 = st.columns([1, 2])
                zapisz_inpost = cb_i1.form_submit_button("Zapisz")
                reset_inpost = cb_i2.form_submit_button("🗑️ Wyzeruj")
                
                if zapisz_inpost:
                    final_i1_n = i1_n if i1_n > 0 else round(i1_b / 1.23, 2)
                    final_i1_b = i1_b if i1_b > 0 else round(final_i1_n * 1.23, 2)
                    final_i2_n = i2_n if i2_n > 0 else round(i2_b / 1.23, 2)
                    final_i2_b = i2_b if i2_b > 0 else round(final_i2_n * 1.23, 2)
                    new = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "InPost_1": final_i1_n, "InPost_2": final_i2_n, "InPost_1_Brutto": final_i1_b, "InPost_2_Brutto": final_i2_b}])
                    df_inpost = df_inpost[~((df_inpost["Rok"] == wybrany_rok) & (df_inpost["Miesiąc"] == wybrany_miesiac))]
                    pd.concat([df_inpost, new]).to_csv(PLIK_INPOST, index=False)
                    st.rerun()
                    
                if reset_inpost:
                    df_inpost = df_inpost[~((df_inpost["Rok"] == wybrany_rok) & (df_inpost["Miesiąc"] == wybrany_miesiac))]
                    df_inpost.to_csv(PLIK_INPOST, index=False)
                    st.rerun()

        st.write("---")
        st.subheader("📝 Dodatkowe koszty w tym miesiącu")

        cz1, cz2, cz3, cz4, cz5, cz6 = st.columns([2.5, 1.2, 1.2, 1.1, 1.5, 1.5])
        cz1.markdown("**Nazwa**")
        cz2.markdown("**Kwota Brutto**")
        cz3.markdown("**Kwota Netto**")
        cz4.markdown("**VAT**")
        cz5.markdown("**Kategoria**")
        cz6.markdown("**Akcje**")
        
        if not df_zm_m.empty:
            for i, (idx, r) in enumerate(df_zm_m.iterrows()):
                if st.session_state["edit_zmienne_id"] == idx:
                    with st.form(key=f"ez_{idx}"):
                        c_ez1, c_ez2, c_ez3, c_ez4, c_ez5, c_ez6 = st.columns([2.5, 1.2, 1.2, 1.1, 1.5, 1.5])
                        en = c_ez1.text_input("Nazwa", r["Nazwa"], label_visibility="collapsed")
                        ek_b = c_ez2.number_input("Kwota Brutto", float(r["Kwota_Brutto"]), label_visibility="collapsed", step=None)
                        ek_n = c_ez3.number_input("Kwota Netto", float(r["Kwota"]), label_visibility="collapsed", step=None)
                        c_ez4.markdown("<div style='padding-top:8px; color:gray; text-align:center;'>Auto</div>", unsafe_allow_html=True)
                        current_kat_z = r["Kategoria"] if r["Kategoria"] in LISTA_KATEGORII else LISTA_KATEGORII[0]
                        ekat = c_ez5.selectbox("Kategoria", LISTA_KATEGORII, index=LISTA_KATEGORII.index(current_kat_z), label_visibility="collapsed")
                        if c_ez6.form_submit_button("💾 Zapisz"):
                            df_zmienne.at[idx, "Nazwa"] = en
                            df_zmienne.at[idx, "Kwota"] = ek_n
                            df_zmienne.at[idx, "Kwota_Brutto"] = ek_b
                            df_zmienne.at[idx, "Kategoria"] = ekat
                            df_zmienne.to_csv(PLIK_ZMIENNE, index=False)
                            st.session_state["edit_zmienne_id"] = None
                            st.rerun()
                else:
                    kwota_netto_val = float(r["Kwota"])
                    kwota_brutto_val = float(r["Kwota_Brutto"])
                    kwota_vat_val = round(kwota_brutto_val - kwota_netto_val, 2)
                    
                    # LOGIKA KOLOROWANIA WIERSZA NA BAZIE KATEGORII
                    kat_szukana = df_kategorie[df_kategorie['Nazwa'] == r['Kategoria']]
                    bg_color = kat_szukana.iloc[0]['Kolor'] if not kat_szukana.empty else "#f8fafc"
                    
                    cell_style = f"background-color: {bg_color}; padding: 8px 12px; border-radius: 4px; border: 1px solid #e2e8f0; color: #000000; min-height: 40px; display: flex; align-items: center;"
                    
                    c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.2, 1.2, 1.1, 1.5, 1.5])
                    c1.markdown(f"<div style='{cell_style}'>{r['Nazwa']}</div>", unsafe_allow_html=True)
                    c2.markdown(f"<div style='{cell_style}'>{kwota_brutto_val:.2f} PLN</div>", unsafe_allow_html=True)
                    c3.markdown(f"<div style='{cell_style}'>{kwota_netto_val:.2f} PLN</div>", unsafe_allow_html=True)
                    c4.markdown(f"<div style='{cell_style}'>{kwota_vat_val:.2f} PLN</div>", unsafe_allow_html=True)
                    c5.markdown(f"<div style='{cell_style}'>{r['Kategoria']}</div>", unsafe_allow_html=True)
                    
                    with c6:
                        btn1, btn2 = st.columns(2)
                        if btn1.button("✏️", key=f"ezb_{idx}"): st.session_state["edit_zmienne_id"] = idx; st.rerun()
                        if btn2.button("🗑️", key=f"dzb_{idx}"): 
                            df_zmienne = df_zmienne.drop(idx)
                            df_zmienne.to_csv(PLIK_ZMIENNE, index=False)
                            st.session_state["edit_zmienne_id"] = None
                            st.rerun()
        
        with st.form(f"form_add_zm_{wybrany_miesiac}", clear_on_submit=True):
            ca1, ca2, ca3, ca4, ca5, ca6 = st.columns([2.5, 1.2, 1.2, 1.1, 1.5, 1.5])
            nazwa_z = ca1.text_input("Nazwa", placeholder="Wpisz nazwę...", label_visibility="collapsed")
            kwota_z_brutto = ca2.number_input("Brutto", min_value=0.0, format="%.2f", label_visibility="collapsed", step=None)
            kwota_z_netto = ca3.number_input("Netto (0=Auto)", min_value=0.0, format="%.2f", label_visibility="collapsed", step=None)
            ca4.markdown("<div style='padding-top:8px; color:gray; font-size:14px; text-align:center;'>Wyliczy się</div>", unsafe_allow_html=True)
            kategoria_z = ca5.selectbox("Kategoria", LISTA_KATEGORII, label_visibility="collapsed")
            zapisz_z = ca6.form_submit_button("➕ Dodaj")
            
            if zapisz_z and nazwa_z.strip() != "":
                finalna_z_netto = kwota_z_netto if kwota_z_netto > 0 else round(kwota_z_brutto / 1.23, 2)
                finalne_z_brutto = kwota_z_brutto if kwota_z_brutto > 0 else round(finalna_z_netto * 1.23, 2)
                new_z = pd.DataFrame([{"Rok": wybrany_rok, "Miesiąc": wybrany_miesiac, "Nazwa": nazwa_z.strip(), "Kwota": finalna_z_netto, "Kategoria": kategoria_z, "Kwota_Brutto": finalne_z_brutto}])
                df_zmienne = pd.concat([df_zmienne, new_z], ignore_index=True)
                df_zmienne.to_csv(PLIK_ZMIENNE, index=False)
                st.rerun()

        if not df_zm_m.empty:
            total_z_netto = df_zm_m["Kwota"].sum()
            total_z_brutto = df_zm_m["Kwota_Brutto"].sum()
            total_z_vat = round(total_z_brutto - total_z_netto, 2)
            
            st.write("")
            c_tz1, c_tz2, c_tz3, c_tz4, c_tz5, c_tz6 = st.columns([2.5, 1.2, 1.2, 1.1, 1.5, 1.5])
            summary_style = "background-color: #e2e8f0; padding: 8px 12px; border-radius: 4px; font-weight: bold; color: #000000; min-height: 40px; display: flex; align-items: center;"
            c_tz1.markdown(f"<div style='{summary_style}'>RAZEM:</div>", unsafe_allow_html=True)
            c_tz2.markdown(f"<div style='{summary_style}'>{total_z_brutto:.2f} PLN</div>", unsafe_allow_html=True)
            c_tz3.markdown(f"<div style='{summary_style}'>{total_z_netto:.2f} PLN</div>", unsafe_allow_html=True)
            c_tz4.markdown(f"<div style='{summary_style}'>{total_z_vat:.2f} PLN</div>", unsafe_allow_html=True)
            c_tz5.markdown(f"<div style='{summary_style}'>-</div>", unsafe_allow_html=True)
            with c_tz6:
                if st.button("🗑️ Wyczyść", key=f"del_all_z_{wybrany_miesiac}"):
                    df_zmienne = df_zmienne[~((df_zmienne["Rok"] == wybrany_rok) & (df_zmienne["Miesiąc"] == wybrany_miesiac))]
                    df_zmienne.to_csv(PLIK_ZMIENNE, index=False)
                    st.rerun()

        st.write("---")
        
        st.subheader("📊 Podsumowanie wydatków według kategorii (Faktury i inne)")
        df_stale_m_copy = df_stale_m.copy() if not df_stale_m.empty else pd.DataFrame(columns=["Kwota"])
        if not df_stale_m_copy.empty:
            df_stale_m_copy["Kategoria"] = "Koszty Stałe"
        
        df_miesiac_calosc = pd.concat([df_stale_m_copy, df_zm_m], ignore_index=True)
        if not df_miesiac_calosc.empty:
            podsumowanie_kategorii = df_miesiac_calosc.groupby("Kategoria")["Kwota"].sum().reset_index()
            podsumowanie_kategorii = podsumowanie_kategorii.sort_values(by="Kwota", ascending=False)
            
            # NOWA: Piękna tabela podsumowania w HTML zamiast standardowego dataframe
            html_table = "<div style='overflow-x:auto;'><table class='cat-table'>"
            html_table += "<tr><th>Kategoria Kosztów</th><th style='text-align: right;'>Łączna Kwota Netto (PLN)</th></tr>"
            
            for idx_cat, row_cat in podsumowanie_kategorii.iterrows():
                kat_nazwa = row_cat['Kategoria']
                kwota_suma = row_cat['Kwota']
                
                # Ustalenie koloru kwadracika
                if kat_nazwa == "Koszty Stałe":
                    bg_col = "#e0f2fe"  # Kolor specjalny dla kosztów stałych (błękitny)
                else:
                    kat_sz = df_kategorie[df_kategorie['Nazwa'] == kat_nazwa]
                    bg_col = kat_sz.iloc[0]['Kolor'] if not kat_sz.empty else "#f8fafc"
                
                html_table += f"<tr><td style='display: flex; align-items: center; gap: 12px;'><div style='width: 16px; height: 16px; border-radius: 4px; background-color: {bg_col}; border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 1px 2px rgba(0,0,0,0.05);'></div><span style='color: #1e293b;'>{kat_nazwa}</span></td><td style='text-align: right; color: #0f172a;'>{kwota_suma:.2f} PLN</td></tr>"
            
            suma_calkowita_kategorii = podsumowanie_kategorii['Kwota'].sum()
            html_table += f"<tr style='background-color: #f8fafc;'><td style='text-align: right; font-weight: 700; color: #475569;'>RAZEM:</td><td style='text-align: right; font-weight: 800; color: #0f172a; font-size: 16px;'>{suma_calkowita_kategorii:.2f} PLN</td></tr>"
            html_table += "</table></div>"
            
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.info("Brak kosztów z faktur do podsumowania w tym miesiącu.")
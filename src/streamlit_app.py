import streamlit as st
import requests

st.set_page_config(page_title="Twitter Bot Avcısı", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(124, 58, 237, 0.35), transparent 28%),
            radial-gradient(circle at 85% 18%, rgba(14, 165, 233, 0.30), transparent 24%),
            radial-gradient(circle at 50% 85%, rgba(236, 72, 153, 0.18), transparent 30%),
            linear-gradient(180deg, #030712 0%, #071226 45%, #081a33 100%);
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 980px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #ffffff !important;
        font-size: 4rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 0.6rem !important;
        text-shadow: 0 0 24px rgba(59,130,246,0.22);
    }

    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-top: 1.2rem !important;
    }

    p, label, .stMarkdown, .stCaption {
        color: #dbe7ff !important;
    }

    div[data-testid="stNumberInput"],
    div[data-testid="stDateInput"],
    div[data-testid="stSelectbox"],
    div[data-testid="stCheckbox"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
    }

    div[data-baseweb="input"] > div,
    .stDateInput > div > div,
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 14px !important;
    }

    .stNumberInput input,
    .stDateInput input,
    .stSelectbox input {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    .stCheckbox label {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        font-size: 1.08rem;
        font-weight: 800;
        color: white;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 55%, #ec4899 100%);
        box-shadow: 0 12px 28px rgba(124, 58, 237, 0.35);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 34px rgba(236, 72, 153, 0.28);
        background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 55%, #db2777 100%);
    }

    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 18px !important;
    }

    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Twitter Bot Avcısı")
st.write("Twitter/X kullanıcı özelliklerine göre hesabın bot olma olasılığını tahmin eder.")

st.subheader("Kullanıcı Bilgileri")

gonderi_sayisi = st.number_input("Gönderi Sayısı", min_value=0, value=34)
takipci_sayisi = st.number_input("Takipçi Sayısı", min_value=0, value=1)
takip_edilen_sayisi = st.number_input("Takip Edilen Sayısı", min_value=0, value=0)
begeni_sayisi = st.number_input("Beğeni Sayısı", min_value=0, value=0)
listelenme_sayisi = st.number_input("Listelenme Sayısı", min_value=0, value=0)

st.subheader("Profil Özellikleri")

geo_enabled = st.checkbox("Konum özelliği açık", value=False)
default_profile = st.checkbox("Varsayılan profil kullanıyor", value=False)
profile_background_tile = st.checkbox("Profil arka plan deseni var", value=False)
profile_use_background_image = st.checkbox("Profil arka plan görseli kullanıyor", value=False)

has_url = st.checkbox("Profilinde bağlantı (URL) var", value=False)
has_location = st.checkbox("Profilinde konum bilgisi var", value=False)
has_description = st.checkbox("Profil açıklaması var", value=False)
has_time_zone = st.checkbox("Saat dilimi bilgisi var", value=False)
has_profile_banner = st.checkbox("Profil banner görseli var", value=False)

from datetime import date

hesap_acilis_tarihi = st.date_input(
    "Hesabın Açılış Tarihi",
    value=date(2021, 1, 1)
)

hesap_yasi_gun = (date.today() - hesap_acilis_tarihi).days

st.caption(f"Hesap yaşı otomatik hesaplandı: {hesap_yasi_gun} gün")

if st.button("Tahmin Yap"):
    payload = {
        "statuses_count": int(gonderi_sayisi),
        "followers_count": int(takipci_sayisi),
        "friends_count": int(takip_edilen_sayisi),
        "favourites_count": int(begeni_sayisi),
        "listed_count": int(listelenme_sayisi),
        "geo_enabled": int(geo_enabled),
        "default_profile": int(default_profile),
        "profile_background_tile": int(profile_background_tile),
        "profile_use_background_image": int(profile_use_background_image),
        "has_url": int(has_url),
        "has_location": int(has_location),
        "has_description": int(has_description),
        "has_time_zone": int(has_time_zone),
        "has_profile_banner": int(has_profile_banner),
        "account_age_days_fixed": float(hesap_yasi_gun)
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            bot_probability = result["bot_probability"]
            bot_yuzde = round(bot_probability * 100, 2)

            st.subheader("Tahmin Sonucu")

            if prediction == 1:
                st.error(f"Bu hesabın bot olma olasılığı yüksek. Bot olasılığı: %{bot_yuzde}")
            else:
                st.success(f"Bu hesap daha çok gerçek kullanıcı gibi görünüyor. Bot olasılığı: %{bot_yuzde}")

            st.json(result)

        else:
            st.warning(f"API hata döndürdü. Durum kodu: {response.status_code}")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error("FastAPI servisine bağlanılamadı. Önce API'yi çalıştır.")
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
import streamlit as st
import requests

st.set_page_config(page_title="Twitter Bot Avcısı", page_icon="🤖", layout="centered")

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
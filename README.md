# Twitter Bot Avcısı

Twitter/X kullanıcılarının bot olasılığını tahmin eden uçtan uca veri bilimi ve makine öğrenmesi projesi.

## Proje Amacı

Bu proje, Twitter/X kullanıcı profillerinden elde edilen sayısal ve profil tabanlı özellikleri kullanarak bir hesabın bot mu yoksa gerçek kullanıcı mı olduğunu tahmin etmeyi amaçlar.

## Kullanılan Veri Seti

- Cresci-2017
- Kaynak: Bot Repository

## Proje Kapsamı

Bu projede şu adımlar uygulanmıştır:

- farklı bot ve gerçek kullanıcı veri setlerinin birleştirilmesi
- veri temizleme ve eksik değer analizi
- feature engineering
- model karşılaştırması
- Random Forest, Logistic Regression ve XGBoost ile sınıflandırma
- FastAPI ile tahmin servisi geliştirme

## Kullanılan Özellikler

İlk model sürümünde kullanılan başlıca özellikler:

- statuses_count
- followers_count
- friends_count
- favourites_count
- listed_count
- geo_enabled
- default_profile
- profile_background_tile
- profile_use_background_image
- has_url
- has_location
- has_description
- has_time_zone
- has_profile_banner
- account_age_days_fixed

## Denenen Modeller

- Logistic Regression
- Random Forest
- XGBoost

## Model Sonuçları

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
| --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.9610 | 0.9721 | 0.9766 | 0.9744 | 0.9763 |
| Random Forest | 0.9889 | 0.9940 | 0.9913 | 0.9926 | 0.9981 |
| XGBoost | 0.9885 | 0.9940 | 0.9908 | 0.9924 | 0.9981 |

## En İyi Model

En iyi performans Random Forest modeli ile elde edilmiştir.

## Proje Yapısı

```bash
twitter-bot-avcisi/
│
├── notebooks/
├── src/
├── models/
├── data/
├── requirements.txt
└── README.md
```

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Uygulamayı Çalıştırma

Önce API servisini başlat:

```bash
uvicorn src.app:app --reload
```

Ardından yeni bir terminal açıp Streamlit arayüzünü çalıştır:

```bash
streamlit run src/streamlit_app.py
```

## API Dokümantasyonu

Swagger arayüzü:
`http://127.0.0.1:8000/docs`

Streamlit arayüzü:
`http://localhost:8501`

## Not

Bu projede kullanılan model, kullanıcı profiline ait belirli öznitelikler üzerinden tahmin üretmektedir. Sonuçlar veri setinin yapısına bağlıdır ve gerçek dünya genellemesi için ek doğrulama çalışmaları yapılmalıdır.

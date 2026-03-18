from fastapi import FastAPI
from pydantic import BaseModel

from src.predict import predict_bot


app = FastAPI(
    title="Twitter Bot Avcısı API",
    description="Twitter/X kullanıcılarının bot olasılığını tahmin eden API",
    version="1.0.0"
)


class UserFeatures(BaseModel):
    statuses_count: int
    followers_count: int
    friends_count: int
    favourites_count: int
    listed_count: int
    geo_enabled: int
    default_profile: int
    profile_background_tile: int
    profile_use_background_image: int
    has_url: int
    has_location: int
    has_description: int
    has_time_zone: int
    has_profile_banner: int
    account_age_days_fixed: float


@app.get("/")
def root():
    return {"message": "Twitter Bot Avcısı API çalışıyor."}


@app.post("/predict")
def predict(user: UserFeatures):
    result = predict_bot(user.model_dump())
    return result
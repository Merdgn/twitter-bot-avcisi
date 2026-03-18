import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_bot_detector.joblib"
FEATURES_PATH = BASE_DIR / "models" / "random_forest_feature_list.joblib"


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    return model, features


def prepare_input(input_data: dict, feature_list: list) -> pd.DataFrame:
    df = pd.DataFrame([input_data])

    for feature in feature_list:
        if feature not in df.columns:
            df[feature] = 0

    df = df[feature_list]
    return df


def predict_bot(input_data: dict) -> dict:
    model, feature_list = load_artifacts()
    prepared_df = prepare_input(input_data, feature_list)

    pred_class = int(model.predict(prepared_df)[0])
    pred_proba = float(model.predict_proba(prepared_df)[0][1])

    return {
        "prediction": pred_class,
        "bot_probability": round(pred_proba, 4)
    }


if __name__ == "__main__":
    sample_user = {
        "statuses_count": 34,
        "followers_count": 1,
        "friends_count": 0,
        "favourites_count": 0,
        "listed_count": 0,
        "geo_enabled": 0,
        "default_profile": 0,
        "profile_background_tile": 0,
        "profile_use_background_image": 1,
        "has_url": 0,
        "has_location": 1,
        "has_description": 1,
        "has_time_zone": 1,
        "has_profile_banner": 0,
        "account_age_days_fixed": 1518.397049
    }

    result = predict_bot(sample_user)
    print(result)
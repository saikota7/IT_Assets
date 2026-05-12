import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "IT_Assets_Data.xlsx")


def load_data():
    df = pd.read_excel(FILE_PATH)
    df.columns = df.columns.str.strip()
    return df


def save_data(df):
    df.to_excel(FILE_PATH, index=False)


# -------------------------
# ADD ASSET
# -------------------------
def add_asset(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_data(df)


# -------------------------
# UPDATE STATUS
# -------------------------
def update_status(asset_tag, column, value):
    df = load_data()
    df.loc[df["Laptop Asset Tag"] == asset_tag, column] = value
    save_data(df)
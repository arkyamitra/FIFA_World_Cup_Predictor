import pandas as pd
df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

print(df["date"].head())

df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

print(df[["date","year"]].head())

print(df["year"].min())
print(df["year"].max())

recent_matches = df[df["year"] >= 2016]
print(recent_matches.shape)
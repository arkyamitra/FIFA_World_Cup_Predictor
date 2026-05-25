import pandas as pd
df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

print(df.head())
print(df.shape)
print(df.columns)
print(df["home_team"].head())
print(df[["home_team", "away_team"]].head())
print(type(df["home_team"].head()))
print(type(df[["home_team", "away_team"]].head()))
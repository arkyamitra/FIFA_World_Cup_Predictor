import pandas as pd
df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

df["result"] = "Draw"

df.loc[df["home_score"] > df["away_score"], "result"] = "Home Win"
df.loc[df["home_score"] < df["away_score"], "result"] = "Away Win"
df["goal_difference"] = df["home_score"] - df["away_score"]

print(df[["home_team","away_team","home_score","away_score","goal_difference"]].head())

print(df["goal_difference"].describe())
print(df["goal_difference"].value_counts())
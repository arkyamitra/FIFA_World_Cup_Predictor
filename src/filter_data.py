import pandas as pd
df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

world_cup_matches = df[df["tournament"] == "FIFA World Cup"]

print(world_cup_matches.head())
print(world_cup_matches.shape)

brazil_matches = df[df["home_team"] == "Brazil"]
print(brazil_matches.head())

argentina_matches = df[df["home_team"] == "Argentina"]
print(argentina_matches.head())

home_score_greater_5 = df[df["home_score"] > 5]
print(home_score_greater_5.head())

friendly_matches = df[df["tournament"] == "Friendly"]
print(friendly_matches.head())
print(friendly_matches.shape)
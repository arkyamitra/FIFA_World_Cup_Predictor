import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

df["goal_difference"] = df["home_score"] - df["away_score"]

plt.figure(figsize=(12,6))
sns.histplot(df["goal_difference"],bins=30)

plt.title("Distribution of Goal Difference")
plt.xlabel("Goal Difference")
plt.ylabel("Number of Matches")
plt.show()
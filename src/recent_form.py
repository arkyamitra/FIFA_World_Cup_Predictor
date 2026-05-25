import pandas as pd
df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

df["date"]= pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df= df.sort_values("date")

df["home_win"] = (df["home_score"] > df["away_score"]).astype(int)

df["home_team_recent_wins"] = (
    df.groupby("home_team")["home_win"]
    .transform(lambda x: x.shift().rolling(5,min_periods=1).sum())
)

df["home_team_recent_goals"] = (
    df.groupby("home_team")["home_score"]
    .transform(lambda x: x.shift().rolling(5,min_periods=1).mean())
)

df["home_team_recent_goals_conceded"] = (
    df.groupby("home_team")["away_score"]
    .transform(lambda x: x.shift().rolling(5,min_periods=1).mean())
)

df["goal_difference"] = (
    df["home_score"] - df["away_score"]
)

df["recent_goal_difference"] = (
    df.groupby("home_team")["goal_difference"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).mean()
    )
)

df["away_win"] = (df["away_score"] > df["home_score"]).astype(int)

df["away_team_recent_wins"] =(
    df.groupby("away_team")["away_win"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).sum()
    )
)

df["away_team_recent_goals"] = (
    df.groupby("away_team")["away_score"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).mean()
    )
)

df["away_team_recent_goal_conceded"] = (
    df.groupby("away_team")["home_score"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).mean()
    )
)

df["away_goal_difference"] = (
    df["away_score"] - df["home_score"]
)

df["away_recent_goal_difference"] = (
    df.groupby("away_team")["away_goal_difference"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).mean() 
        )
)

df["form_difference"] = (
    df["home_team_recent_wins"] - df["away_team_recent_wins"]
)

df["attack_difference"] = (
    df["home_team_recent_goals"] - df["away_team_recent_goals"]
)

df["defence_difference"] = (
    df["away_team_recent_goal_conceded"] - df["home_team_recent_goals_conceded"]
)

df["dominance_difference"] = (
    df["recent_goal_difference"] - df["away_recent_goal_difference"]
)

recent_matches = df[df["year"] >= 2016]

print(recent_matches[[ "home_team","away_team","form_difference","attack_difference","defence_difference","dominance_difference"]].head(20))
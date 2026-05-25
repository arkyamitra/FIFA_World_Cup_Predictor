import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

df["date"]= pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df= df.sort_values("date")

df["goal_difference"] = (
    df["home_score"] - df["away_score"]
)

df["home_win"] =(
    df["home_score"] > df["away_score"]
).astype(int)

df["away_win"] = (
    df["away_score"] > df["home_score"]
).astype(int)

df["home_team_recent_wins"] = (
    df.groupby("home_team")["home_win"]
    .transform(
        lambda x: x.shift().rolling(5,min_periods=1).sum()
    )
)

df["away_team_recent_wins"] = (
    df.groupby("away_team")["away_win"]
    .transform(
        lambda x: x.shift().rolling(5,min_periods=1).sum()
    )
)

df["home_team_recent_goals"] = (
    df.groupby("home_team")["home_score"]
    .transform(lambda x: x.shift().rolling(5,min_periods=1).mean())
)

df["home_team_recent_goals_conceded"] = (
    df.groupby("home_team")["away_score"]
    .transform(lambda x: x.shift().rolling(5,min_periods=1).mean())
)

df["recent_goal_difference"] = (
    df.groupby("home_team")["goal_difference"]
    .transform(
        lambda x:x.shift().rolling(5,min_periods=1).mean()
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

df["dominance_closeness"] = abs(
    df["dominance_difference"]
)

df["defence_closeness"] = abs(
    df["defence_difference"]
)
df["target"] = 1

df.loc[
    df["home_score"] > df["away_score"],
    "target"
] = 2

df.loc[
    df["home_score"] < df["away_score"],
    "target"
] = 0

features = ["defence_difference",
            "dominance_difference",
            "dominance_closeness",
            "defence_closeness"]

x = df[features]
y = df["target"]

x = x.fillna(0)

x_train, x_test, y_train, y_test = train_test_split(
    x ,
    y ,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(
    class_weight="balanced",
    max_iter= 1000
)

model.fit(x_train,y_train)

predictions = model.predict(x_test)

probabilities = model.predict_proba(x_test)


probability_df = pd.DataFrame(
    probabilities,
    columns=[
        "Away Win Probability",
        "Draw Probability",
        "Home Win Probability"
    ]
)

def predict_match(
        home_team,
        away_team
) :
    home_data = df[
        df["home_team"] == home_team
    ].tail(1)

    away_data = df[
        df["away_team"] == away_team
    ].tail(1)

    input_data = pd.DataFrame({
        "defence_difference": [
            home_data["defence_difference"].values[0]
        ],
        "dominance_difference": [
            home_data["dominance_difference"].values[0]
        ],
        "dominance_closeness" : [
            home_data["dominance_closeness"].values[0]
        ],
        "defence_closeness": [
            home_data["defence_closeness"].values[0]
        ]
    })

    probabilities = model.predict_proba(
        input_data
    )

    print(f"\n{home_team} vs {away_team}\n")

    print(
        f"Away Win Probability: "
        f"{probabilities[0][0]: .2%}"
    )

    print(
        f"Draw Probability: "
        f"{probabilities[0][1]: .2%}"
    )

    print(
        f"Home Win Probability: "
        f"{probabilities[0][2]: .2%}"
    )

predict_match(
    "Brazil",
    "France"
)
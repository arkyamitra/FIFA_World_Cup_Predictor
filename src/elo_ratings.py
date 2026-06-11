import pandas as pd

df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/results.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

elo_ratings = {}

def get_elo(team) :
    if team not in elo_ratings:
        elo_ratings[team] = 1500
    return elo_ratings[team]

def expected_result(
        team_elo,
        opponent_elo
) :
    
    return 1/ (
        1 + 10 ** (
            (opponent_elo - team_elo) / 400
        )
    )

def update_elo(
        current_elo,
        expected,
        actual,
        k = 30
) :
    
    return current_elo + k * (
        actual - expected
    )

home_elo_list = []
away_elo_list = []

for index, row in df.iterrows():
    home_team = row["home_team"]
    away_team = row["away_team"]
    
    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)
    
    home_elo_list.append(home_elo)
    away_elo_list.append(away_elo)
    
    expected_home = expected_result(
    home_elo,
    away_elo
)
    
    expected_away = expected_result(
    away_elo,
    home_elo
)
    
    if row["home_score"] > row["away_score"]:

        actual_home = 1
        actual_away = 0

    elif row["home_score"] < row["away_score"]:

        actual_home = 0
        actual_away = 1

    else:

        actual_home = 0.5
        actual_away = 0.5
    
    new_home_elo = update_elo(
    home_elo,
    expected_home,
    actual_home
)
    
    new_away_elo = update_elo(
    away_elo,
    expected_away,
    actual_away
)
    
    elo_ratings[home_team] = new_home_elo
    elo_ratings[away_team] = new_away_elo

df["home_elo"] = home_elo_list
df["away_elo"] = away_elo_list

df["elo_difference"] =(
    df["home_elo"] - df["away_elo"]
)

print(df[
    [
        "home_team",
        "away_team",
        "home_elo",
        "away_elo",
        "elo_difference"
    ]
].tail(20)
)
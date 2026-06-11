import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


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


df["target"] = 1

df.loc[
    df["home_score"] > df["away_score"],
    "target"
] = 2

df.loc[
    df["home_score"] < df["away_score"],
    "target"
] = 0

print(df["target"].value_counts())

features = ["attack_difference",
            "defence_difference",
            "dominance_difference",
            "dominance_closeness",
            "defence_closeness",
            "form_difference",
            "home_elo",
            "away_elo",
            "elo_difference"]

x = df[features]
y = df["target"]

x = x.fillna(0)
scaler = StandardScaler()
x_scaled = pd.DataFrame(
    scaler.fit_transform(x),
    columns = x.columns
)

x_train, x_test, y_train, y_test = train_test_split(
    x_scaled ,
    y ,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(
    class_weight="balanced",
    max_iter= 2000
)

model.fit(x_train,y_train)

def get_latest_team_data(team):

    team_matches = df[

        (df["home_team"] == team)

        |

        (df["away_team"] == team)

    ].tail(1)

    return team_matches

def get_match_probabilities(
    home_team,
    away_team):
    
    team_mapping = {
        "Czechia": "Czech Republic",
        "Türkiye": "Turkey",
        "IR Iran": "Iran",
        "Côte d'Ivoire": "Ivory Coast",
        "Congo DR": "DR Congo",
        "Curacao": "Curaçao",
        "Bosnia-Herzegovina": "Bosnia and Herzegovina",
        "USA": "United States",
        "Cabo Verde": "Cape Verde"
        }

    home_team = team_mapping.get(
        home_team,
        home_team
    )

    away_team = team_mapping.get(
        away_team,
        away_team
    )

    home_data = get_latest_team_data(
        home_team
    )

    away_data = get_latest_team_data(
        away_team
    )

    if home_data.empty:
        print(
            "Missing Home Team:",
            home_team
        )
    
    if away_data.empty:
        print(
            "Missing Away Team:",
            away_team
        )

    if home_data.empty or away_data.empty:
               print(
                   "Missing team data:",
                   home_team,
                   away_team
               )
               return[0.33,0.34,0.33]

    input_data = pd.DataFrame({
        "attack_difference": [
            home_data["attack_difference"].values[0]
            -
            away_data["attack_difference"].values[0]
        ],
        "defence_difference": [
            home_data["defence_difference"].values[0]
            -
            away_data["defence_difference"].values[0]
        ],
        "dominance_difference": [
            home_data["dominance_difference"].values[0]
            -
            away_data["dominance_difference"].values[0]
        ],
        "dominance_closeness": [
            home_data["dominance_closeness"].values[0]
        ],
        "defence_closeness": [
            home_data["defence_closeness"].values[0]
        ],
        "form_difference": [
            home_data["form_difference"].values[0]
            -
            away_data["form_difference"].values[0]
        ],
        "home_elo": [
            get_elo(home_team)
        ],
        "away_elo": [
            get_elo(away_team)
        ],
        "elo_difference": [
            get_elo(home_team)
            -
            get_elo(away_team)
        ]
    })

    input_scaled = pd.DataFrame(
        scaler.transform(input_data),
        columns = input_data.columns
    )

    probabilities = model.predict_proba(
        input_scaled
    )[0]

    return probabilities

def simulate_match(
    home_team,
    away_team):

    probabilities = get_match_probabilities(
        home_team,
        away_team
    )

    away_win_probability = probabilities[0]
    draw_probability = probabilities[1]
    home_win_probability = probabilities[2]

    random_number = random.random()

    if random_number < away_win_probability:

        return "Away Win"

    elif random_number < (
        away_win_probability + draw_probability
    ):

        return "Draw"

    else:

        return "Home Win"
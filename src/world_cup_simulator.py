import pandas as pd
import random
from prediction_engine import (
    simulate_match,
    get_match_probabilities)

groups_df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/world_cup_groups.csv")

fixtures_df = pd.read_csv("C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/data/world_cup_fixtures.csv")

def run_tournament():

    standings = {}

    for team in groups_df["Team"]:
        standings[team] = {
            "Points":0,
            "Played":0,
            "Wins":0,
            "Draws":0,
            "Losses":0,
            "Goals_For":0,
            "Goals_Against":0,
            "Goal_Difference":0
        }

    def generate_score(
            result,
            home_team,
            away_team
            ):
            probabilities = get_match_probabilities(
                home_team,
                away_team
            )
            
            home_strength = probabilities[2]
            away_strength = probabilities[0]
            
            if result == "Home Win":
                
                if home_strength > 0.60:
                    return random.choice([
                        (2,0),
                        (3,0),
                        (3,1),
                        (4,1)
                    ])
                
                return random.choice([
                    (1,0),
                    (2,1),
                    (2,0),
                    (3,1)
                ])
            
            elif result == "Away Win":
                
                if away_strength > 0.60:
                    return random.choice([
                        (0,2),
                        (0,3),
                        (1,3),
                        (1,4)
                    ])
                return random.choice([
                    (0,1),
                    (1,2),
                    (0,2),
                    (1,3)
                ])
            
            else:
                return random.choice([
                    (0,0),
                    (1,1),
                    (2,2)
                ])


    def update_standings(
        home_team,
        away_team,
        result,
        home_goals,
        away_goals
    ):

        standings[home_team]["Goals_For"] += home_goals
        standings[home_team]["Goals_Against"] += away_goals
        standings[away_team]["Goals_For"] += away_goals
        standings[away_team]["Goals_Against"] += home_goals
        standings[home_team]["Played"] += 1
        standings[away_team]["Played"] += 1

        if result == "Home Win":

            standings[home_team]["Wins"] += 1
            standings[away_team]["Losses"] += 1

            standings[home_team]["Points"] += 3

        elif result == "Away Win":

            standings[away_team]["Wins"] += 1
            standings[home_team]["Losses"] += 1

            standings[away_team]["Points"] += 3

        else:

            standings[home_team]["Draws"] += 1
            standings[away_team]["Draws"] += 1

            standings[home_team]["Points"] += 1
            standings[away_team]["Points"] += 1

        standings[home_team]["Goal_Difference"] = (
                standings[home_team]["Goals_For"] -
                standings[home_team]["Goals_Against"])
            
        standings[away_team]["Goal_Difference"] = (
                standings[away_team]["Goals_For"] -
                standings[away_team]["Goals_Against"]
    )

    for _, fixture in fixtures_df.iterrows():

        home_team = fixture["Home Team"]
        away_team = fixture["Away_Team"]

        result = simulate_match(
            home_team,
            away_team
        )

        home_goals, away_goals = generate_score(
            result,
            home_team,
            away_team
        )

        update_standings(
            home_team,
            away_team,
            result,
            home_goals,
            away_goals
        )

    standings_df = pd.DataFrame.from_dict(
        standings,
        orient="index"
    )

    #print(
        #standings_df.sort_values(
            #by=["Points",
                #"Goal_Difference",
                #"Goals_For"],
            #ascending=False
        #)
    #)

    for group in groups_df["Group"].unique():

        teams = groups_df[
            groups_df["Group"] == group
        ]["Team"]

        group_table = standings_df.loc[
            teams
        ]

        group_table = group_table.sort_values(
            by=[
                "Points",
                "Goal_Difference",
                "Goals_For"
            ],
            ascending=False
        )



        #print("\n")
        #print(group)

        #print(group_table)

    group_winners = {}
    group_runners_up = {}
    qualified_teams = []
    third_place_teams = []

    for group in groups_df["Group"].unique():

        teams = groups_df[
            groups_df["Group"] == group
        ]["Team"]

        group_table = standings_df.loc[
            teams
        ]

        group_table = group_table.sort_values(
            by=[
                "Points",
                "Goal_Difference",
                "Goals_For"
            ],
            ascending=False
        )

        group_letter = group.split()[-1]

        group_winners[group_letter] = (
            group_table.index[0]
        )

        group_runners_up[group_letter] = (
            group_table.index[1]
        )

        qualified_teams.extend(
            group_table.index[:2].tolist()
        )

        third_place_teams.append({

            "Team": group_table.index[2],

            "Points":
                group_table.iloc[2]["Points"],

            "Goal_Difference":
                group_table.iloc[2]["Goal_Difference"],

            "Goals_For":
                group_table.iloc[2]["Goals_For"]

        })

    third_place_df = pd.DataFrame(
        third_place_teams
    )

    third_place_df = third_place_df.sort_values(
        by=[
            "Points",
            "Goal_Difference",
            "Goals_For"
        ],
        ascending=False
    )

    best_third_place_teams = third_place_df.head(8)

    best_third_place_teams = (
        best_third_place_teams["Team"].tolist()
    )

    qualified_teams.extend(
        best_third_place_teams
    )

    #print("\nGroup Winners")

    #print(group_winners)

    #print("\nGroup Runners Up")

    #print(group_runners_up)

    #print("\nBest Third Place Teams")

    #print(best_third_place_teams)

    #print("\nQualified Teams:")

    #for team in qualified_teams:

        #print(team)

    #print(
        #"\nTotal Qualified:",
        #len(qualified_teams)
    #)

    random.shuffle(
        best_third_place_teams
    )

    def play_knockout_round(
        matches,
        round_name
    ):

        #print(
            #f"\n{round_name}"
        #)

        winners = {}

        #for match, teams in matches.items():

            #print(
                #f"Match {match}:"
                #f"{teams[0]} vs {teams[1]}"
            #)

        for match, teams in matches.items():

            result = simulate_match(
                teams[0],
                teams[1]
            )

            if result == "Home Win":

                winner = teams[0]

            elif result == "Away Win":

                winner = teams[1]

            else:

                probabilities = get_match_probabilities(
                    teams[0],
                    teams[1]
                )

                home_win_prob = probabilities[2]
                away_win_prob = probabilities[0]

                winner = random.choices(
                    [teams[0],teams[1]],
                    weights=[
                        home_win_prob,
                        away_win_prob
                    ]
                )[0]
            

            winners[match] = winner

            #print(
                #f"Match {match}: "
                #f"{winner} advances"
            #)

        return winners

    round_of_32 = {
            73: (
            group_runners_up["A"],
            group_runners_up["B"]
        ),

        74: (
            group_winners["C"],
            group_runners_up["F"]
        ),

        75: (
            group_winners["E"],
            best_third_place_teams[0]
        ),

        76: (
            group_winners["F"],
            group_runners_up["C"]
        ),

        77: (
            group_runners_up["E"],
            group_runners_up["I"]
        ),

        78: (
            group_winners["I"],
            best_third_place_teams[1]
        ),

        79: (
            group_winners["A"],
            best_third_place_teams[2]
        ),

        80: (
            group_winners["L"],
            best_third_place_teams[3]
        ),

        81: (
            group_winners["G"],
            best_third_place_teams[4]
        ),

        82: (
            group_winners["D"],
            best_third_place_teams[5]
        ),

        83: (
            group_winners["H"],
            group_runners_up["J"]
        ),

        84: (
            group_runners_up["K"],
            group_runners_up["L"]
        ),

        85: (
            group_winners["B"],
            best_third_place_teams[6]
        ),

        86: (
            group_runners_up["D"],
            group_runners_up["G"]
        ),

        87: (
            group_winners["J"],
            group_runners_up["H"]
        ),

        88: (
            group_winners["K"],
            best_third_place_teams[7]
        )
    }



    round_of_32_winners = play_knockout_round(
        round_of_32,
        "ROUND OF 32"
    )

    #print("\nROUND OF 32 WINNERS")

    round_of_16 = {
        89: [
            round_of_32_winners[73],
            round_of_32_winners[74]
        ],

        90: [
            round_of_32_winners[75],
            round_of_32_winners[76]
        ],

        91: [
            round_of_32_winners[77],
            round_of_32_winners[78]
        ],

        92: [
            round_of_32_winners[79],
            round_of_32_winners[80]
        ],

        93: [
            round_of_32_winners[81],
            round_of_32_winners[82]
        ],

        94: [
            round_of_32_winners[83],
            round_of_32_winners[84]
        ],

        95: [
            round_of_32_winners[85],
            round_of_32_winners[86]
        ],

        96: [
            round_of_32_winners[87],
            round_of_32_winners[88]
        ]
    }



    round_of_16_winners = play_knockout_round(
        round_of_16,
        "ROUND OF 16"
    )

    quarter_finals = {

        97: [
            round_of_16_winners[89],
            round_of_16_winners[90]
        ],

        98: [
            round_of_16_winners[91],
            round_of_16_winners[92]
        ],

        99: [
            round_of_16_winners[93],
            round_of_16_winners[94]
        ],

        100: [
            round_of_16_winners[95],
            round_of_16_winners[96]
        ]
    }



    quarter_final_winners = play_knockout_round(
        quarter_finals,
        "QUARTER FINALS"
    )

    semi_finals = {

        101: [
            quarter_final_winners[97],
            quarter_final_winners[98]
        ],

        102: [
            quarter_final_winners[99],
            quarter_final_winners[100]
        ]
    }



    semi_final_winners = play_knockout_round(
        semi_finals,
        "SEMI FINALS"
    )


    finalists = list(
        semi_final_winners.values()
    )

    #print("\nFINAL")

    #print(
        #finalists[0],
       # "vs",
        #finalists[1]
    #)

    result = simulate_match(
        finalists[0],
        finalists[1]
    )

    if result == "Home Win":

        champion = finalists[0]

    elif result == "Away Win":

        champion = finalists[1]

    else:

        probabilities = get_match_probabilities(
            finalists[0],
            finalists[1]
        )

        champion = random.choices(
            finalists,
            weights=[
                probabilities[2],
                probabilities[0]
            ]
        )[0]

    #print(
        #"\nWORLD CUP CHAMPION:"
    #)

    #print(champion)
    
    return champion

champions =[]

num_simulations = 1000

for i in range(num_simulations):
    champion = run_tournament()
    champions.append(champion)

champion_counts = pd.Series(
    champions
).value_counts()

results_df = pd.DataFrame({
    "Team": champion_counts.index,
    "Titles": champion_counts.values
})

results_df["Win Probability"] = (
    results_df["Titles"]
    /
    num_simulations
)

print(results_df)

results_df = results_df.sort_values(
    by="Win Probability",
    ascending=False
)

results_df["Win Probability"] = (
    results_df["Win Probability"] * 100
).round(2)

results_df.to_csv(
    "C:/Users/arkya.mitra/OneDrive - OneWorkplace/Projects/FIFA_World_Cup_Predictor/output/world_cup_predictions.csv",
    index=False
)

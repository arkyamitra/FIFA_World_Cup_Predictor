# FIFA World Cup Prediction Engine

A machine learning-based football match prediction engine built using Python and Logistic Regression.

This project predicts football match outcomes using:

* team form
* defensive strength
* dominance metrics
* rolling performance indicators
* probabilistic multiclass forecasting

The model predicts:

* Away Win
* Draw
* Home Win

along with outcome probabilities for each match.

---

# Project Motivation

As a football fan and aspiring sports analyst, I wanted to combine:

* football intuition
* data analysis
* machine learning

to build a realistic football forecasting system from scratch while learning Python, GitHub, and sports analytics.

This project represents my first end-to-end machine learning project.

---

# Features Used

The model currently uses engineered football features such as:

* Recent Team Form
* Rolling Goal Difference
* Defensive Strength
* Dominance Difference
* Matchup Closeness Indicators
* Rolling Goals Scored
* Rolling Goals Conceded

---

# Machine Learning Approach

### Model

* Logistic Regression (Multiclass Classification)

### Prediction Classes

| Class | Meaning  |
| ----- | -------- |
| 0     | Away Win |
| 1     | Draw     |
| 2     | Home Win |

### Key ML Concepts Used

* Feature Engineering
* Rolling Statistics
* Multiclass Classification
* Probability Forecasting
* Correlation Analysis
* Multicollinearity Detection
* Class Balancing
* Confusion Matrix Evaluation

---

# Sample Match Prediction

### Brazil vs France

| Outcome    | Probability |
| ---------- | ----------- |
| France Win | 30.83%      |
| Draw       | 35.85%      |
| Brazil Win | 33.31%      |

The model identifies this matchup as highly balanced with significant draw probability due to structural similarity between elite teams.

---

# Key Insights From The Model

* Defensive structure strongly impacts match outcomes.
* Balanced elite teams tend to increase draw probability.
* Home advantage remains statistically important.
* Dominance metrics are more predictive than raw attacking output.

---

# 🛠️ Tech Stack

* Python
* pandas
* scikit-learn
* seaborn
* matplotlib
* Git
* GitHub

---

# Project Structure

```bash
FIFA_World_Cup_Predictor/
│
├── data/
├── src/
│   ├── train_model.py
│   ├── predict_match.py
│
├── requirements.txt
├── README.md
```

---

# Future Improvements

Planned Version 2 upgrades include:

* ELO Ratings Integration
* Expected Goals (xG)
* Tournament Importance Weighting
* Neutral Venue Adjustments
* World Cup Simulation Engine
* Streamlit Web App
* Interactive Dashboard
* Player-Level Features
* Lineup Strength Modeling

---

# Installation

Clone the repository:

```bash
git clone https://github.com/arkyamitra/FIFA_World_Cup_Predictor.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run prediction script:

```bash
python src/predict_match.py
```

---

# Current Status

✅ Version 1 Complete

The current version successfully performs:

* multiclass football prediction
* probability forecasting
* draw-aware modeling
* reusable match predictions

---

# Acknowledgements

Built while learning:

* machine learning
* Python
* GitHub
* sports analytics

through hands-on experimentation and iterative improvement.

Football data sourced from publicly available international football match datasets.

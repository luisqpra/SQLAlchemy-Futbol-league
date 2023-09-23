# Football League Simulation

This is a Python project that simulates a football league using SQLAlchemy and SQLite.

## Description

This project simulates a football league where teams compete against each other, matches are scheduled, and teams have different attributes like defense, midfielder, and forward capabilities.

1. [Description](#description)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Models](#models)
6. [Setting up the Database and Populating Teams](#setting-up-the-database-and-populating-teams)
    - [Creating Tables](#creating-tables)
    - [Populating Teams](#populating-teams)
    - [Team Statistics](#team-statistics)
    - [Fixture Calendar](#fixture-calendar)
7. [Utility Functions](#utility-functions)
    - [Explanation of Utility Functions](#explanation-of-utility-functions)
8. [Usage](#usage)
9. [Rules of the Match and Bonus Calculation](#rules-of-the-match-and-bonus-calculation)
    - [Match Rules](#match-rules)
    - [Bonus Calculation](#bonus-calculation)
10. [License](#license)


## Features

- Teams can be created, updated, and deleted using SQLAlchemy.
- Matches are scheduled and simulated, and the results are recorded.
- Teams have attributes like defense, midfielder, and forward capabilities.
---
## Installation

1. Clone the repository:

   ```
   git clone https://github.com/luisqpra/SQLAlchemy-Futbol-league.git
   cd SQLAlchemy-Futbol-league
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Create the configuration:

   ```
   vim config.py
   ```

4. Run the setup:

   ```
   python setup.py
   ```

5. Run the simulation:

   ```
   python __main.py__
   ```
---
## Configuration

You can configure the database connection in the `config.py` file:

```python
# Import the os and sqlalchemy module
import os

# Database configuration
sqlite_file_name = "database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
```
---
## Models

The database models are defined in the `models.py` file. These models describe the structure and relationships of the data in the project's database. Here's an overview of the models:

### Match Model

The `Match` model represents a football match and its details. It has the following attributes:

- `id`: The unique identifier for each match.
- `num_match`: The match number.
- `day_match`: The day on which the match takes place.
- `team_id`: The ID of the team participating in the match.
- `bonus_defence`: Bonus value for defense.
- `bonus_midfielder`: Bonus value for midfielder.
- `bonus_forward`: Bonus value for forward.
- `team_score`: The score of the team in the match.
- `season`: The season of the match.

### Team Model

The `Team` model represents a football team and its attributes. It includes:

- `id`: The unique identifier for each team.
- `name`: The name of the team.
- `defence`: The defensive capability of the team.
- `midfielder`: The midfield capability of the team.
- `forward`: The forward capability of the team.

These models define the core structure of the simulation and allow the project to manage teams, matches, and their associated data.

---
## Setting up the Database and Populating Teams


### Creating Tables

The code creates the required database tables using the SQLAlchemy's declarative base class defined in `models.py`:


### Populating Teams

A list of team names is defined, representing the teams that will participate in the simulation. Each team name is paired with randomly generated statistics for defense, midfield, and forward capabilities. These values are inserted into the database:

```python
harry_potter_teams = [
    "Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw",
    "Quidditch Crushers", "Phoenix Flyers", "Broomstick Blazers",
    "Wizarding Warriors", "Spellcast Strikers", "Enchanted Defenders"
]

```
### Team Statistics

For each team, the code assigns random values between 1 and 9 to attributes such as defense, midfield, and forward capabilities for each team. This approach ensures that each team has unique and varied strengths and weaknesses.
```python
insert_teams_with_random_stats(harry_potter_teams, session=session)
```

### Fixture Calendar

The code creates a fixture calendar where each team plays once a day, ensuring that no matches are repeated. The calendar is generated using the create_season function:

```pytho

list_IDteams = get_team_ids(session)
create_season(teams=list_IDteams, session=session)
```
---
## Utility Functions

Here's an overview of the utility functions included in `utils.py`:

1. **insert_teams_with_random_stats(team_names: List[str], session: Session) -> None**
   
   This function generates random defense, midfield, and forward statistics for teams and stores them in the database table. 

2. **get_team_ids(session: Session) -> List[int]**

   This function retrieves a list of team IDs from the database. 

3. **create_season(teams: list[int], session: Session) -> None**

   The `create_season` function generates a Fixture Calendar for the season and stores it in the database table. The calendar ensures that each team plays once per day without repeated matches.

4. **goal_scoring(goal_probability: float) -> int**

   The `goal_scoring` function simulates whether a play results in a goal (1) or not (0) based on a given probability.

5. **bonus_score(turns_A: int, turns_B: int, goal_score_A: int, goal_score_B: int, team: Team) -> List[int]**

   This function calculates and applies bonus scores for a team based on match statistics and rules. It adjusts the team's stats (defense, midfield, and forward) in the team table and stores the bonus in the match history in the table.

6. **play_match(session: Session, match: int) -> List[int] | List[List[int]]**

   The `play_match` function simulates a match between two teams based on the given match ID. It calculates the match scores, updates bonuses, and stores the results in the database.
---

## Usage

The `__main__.py` file is the primary script that executes the simulation of your football league. When you run this script, it simulates the league matches, calculates scores, and applies bonuses to teams based on their performance. However, before running the script, it's essential to ensure that the database tables are properly set up using the `setup.py` script.

---
## Rules of the Match and Bonus Calculation

### Match Rules:

Match: `Team A vs Team B`

- Each match consists of 12 turns in which teams attempt to score goals.

- The number of turns for each team is determined by their midfield power and their opponent's midfield power. The formula used to calculate turns is: `TURNS * team_A.midfielder / (team_A.midfielder + team_B.midfielder)`

- The probability of scoring a goal in each turn is determined by the forward power of the attacking team and the defense power of the defending team. The formula for goal-scoring probability is: `team_A.forward / (team_A.forward + team_B.defence)`

### Bonus Calculation:


Bonuses are calculated based on the number of turns and goals scored during the match. The bonus values are adjusted for each team's performance and determine changes in their statistics.

For Team A:

Goals Scored:

- `TURNS` represents the total number of turns in a match (set to 12 in this simulation).
- `turns_A`  is equal to  `TURNS*team_A.midfielder/(team_A.midfielder+team_B.midfielder)`
- If `goal_score_A / turns_A` is greater than 0.8, both `bonus_midfielder` and `bonus_forward` receive a bonus of 0.2.
- If it's between 0.7 and 0.8, a bonus of 0.1 is applied to `bonus_midfielder` and `bonus_forward`.
- If it's less than 0.2, a penalty of -0.2 is applied to `bonus_midfielder` and `bonus_forward`.
- If it's between 0.2 and 0.3, a penalty of -0.1 is applied to `bonus_midfielder` and `bonus_forward`.

Goals Conceded:

- If `goal_score_B / turns_B` is greater than 0.8, a penalty of -0.2 is applied to `bonus_defence`.
- If it's between 0.7 and 0.8, a penalty of -0.1 is applied to `bonus_defence`.
- If it's less than 0.2, a bonus of 0.2 is applied to `bonus_defence`.
- If it's between 0.2 and 0.3, a bonus of 0.1 is applied to `bonus_defence`.

It's important to note that if a team's statistic is 1, it cannot receive a negative bonus (bonus is set to 0). Similarly, if a team's statistic is 9, it cannot receive a positive bonus (bonus is set to 0), as the statistic limits are between 1 and 9.

---


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


import random
from models import Team, Match
from typing import List
from sqlalchemy.orm.session import Session
from itertools import combinations


def insert_teams_with_random_stats(
        team_names: List[str],
        session: Session
) -> None:
    '''
    The function inserts teams with randomly generated statistics
    into a database session.

    Example: team_names_to_insert = ["Team A", "Team B", "Team C"]
    '''
    for name in team_names:
        forward = random.randint(1, 9)
        midfielder = random.randint(1, 9)
        defence = random.randint(1, 9)
        team = Team(name=name, forward=forward, midfielder=midfielder,
                    defence=defence)
        session.add(team)
    session.commit()


def get_team_ids(session: Session) -> List[int]:
    """
    The function `get_team_ids` retrieves the IDs of all teams from
    a session object.
    """
    teams = session.query(Team).all()
    team_ids = [team.id for team in teams]
    return team_ids


def create_season(teams: list[int], session: Session) -> None:
    """
    The function creates a season by generating all possible matches
    between teams and adding them to the session.
    """
    if len(teams) % 2:
        teams.append('Day off')
    n = len(teams)
    matchs = []
    for j in range(1, n):
        for i in range(int(n/2)):
            matchs.append((teams[i], teams[n - 1 - i]))
            team_A = Match(num_match=int(n/2)*(j-1)+i+1, day_match=j,
                           team_id=teams[i])
            session.add(team_A)
            team_B = Match(num_match=int(n/2)*(j-1)+i+1, day_match=j,
                           team_id=teams[n - 1 - i])
            session.add(team_B)
            session.commit()


'''
def simulate_match(session: Session, home_team: Team, away_team: Team):
    home_team_goals = 0
    away_team_goals = 0
    TURNS_MAX = 12

    turns_home = TURNS_MAX*(home_team.midfielder+away_team.midfielder)/home_team.midfielder
    turns_away = TURNS_MAX*(home_team.midfielder+away_team.midfielder)/away_team.midfielder
  
    for _ in range(90):
        home_goal_probability = (home_team.forward + home_team.midfielder) / 20
        away_goal_probability = (away_team.forward + away_team.midfielder) / 20
        
        if random.random() < home_goal_probability:
            home_team_goals += 1
        
        if random.random() < away_goal_probability:
            away_team_goals += 1
    
    # Registra el marcador en la tabla Match
    new_match = Match(home_team=home_team, away_team=away_team,
                      goles_equipo_local=home_team_goals,
                      goles_equipo_visitante=away_team_goals)
    session.add(new_match)
    session.commit()

    return home_team_goals, away_team_goals
 
    return turns_home, turns_away
   '''

if __name__ == '__main__':
    possible_matches_round_1 = list(combinations(range(1, 5), 2))
    possible_matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    print(possible_matches_round_1+possible_matches_round_2)

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


def create_season(session: Session) -> None:
    """
    The function creates a season by generating all possible matches
    between teams and adding them to the session.
    """
    list_IDteams = get_team_ids(session)
    matches_round_1 = list(combinations(list_IDteams, 2))
    matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    matches = matches_round_1+matches_round_2
    for match_teams in matches:
        home_team, away_team = match_teams        
        new_match = Match(home_team=home_team, away_team=away_team)
        session.add(new_match)
    session.commit()


if __name__ == '__main__':
    possible_matches_round_1 = list(combinations(range(1, 5), 2))
    possible_matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    print(possible_matches_round_1+possible_matches_round_2)

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
            if 'Day off' in (teams[i], teams[n - 1 - i]):
                continue
            matchs.append((teams[i], teams[n - 1 - i]))
            team_A = Match(num_match=int(n/2)*(j-1)+i+1, day_match=j,
                           team_id=teams[i])
            session.add(team_A)
            team_B = Match(num_match=int(n/2)*(j-1)+i+1, day_match=j,
                           team_id=teams[n - 1 - i])
            session.add(team_B)
            session.commit()


def goal_scoring(goal_probability: float) -> int:
    if goal_probability < 0 or goal_probability > 1:
        raise ValueError("Probability must be between 0 and 1")
    
    result = random.random()  # Generates a random number between 0 and 1
    
    if result < goal_probability:
        return 1
    else:
        return 0


def play_match(session: Session, match: int) -> list[int]:
    A_team_goals = 0
    B_team_goals = 0
    
    A_teamM, B_teamM = session.query(Match).filter_by(num_match=match).all()

    A_team = session.query(Team).filter_by(id=A_teamM.id).first()
    B_team = session.query(Team).filter_by(id=B_teamM.id).first()

    # print(A_team.id, A_team.defence, A_team.midfielder, A_team.forward)
    # print(B_team.id, B_team.defence, B_team.midfielder, B_team.forward)

    TURNS = 12

    turns_A = round(TURNS*A_team.midfielder/(A_team.midfielder+B_team.midfielder))
    turns_B = TURNS - turns_A
    turns = max(turns_A, turns_B)

    A_goal_scoring = A_team.forward/(A_team.forward+B_team.defence)
    B_goal_scoring = B_team.forward/(B_team.forward+A_team.defence)

    for turn in range(1, turns+1):
        if turn <= turns_A:
            A_team_goals += goal_scoring(A_goal_scoring)
        if turn <= turns_B:
            B_team_goals += goal_scoring(B_goal_scoring)

    return [A_team_goals, B_team_goals]


if __name__ == '__main__':
    possible_matches_round_1 = list(combinations(range(1, 5), 2))
    possible_matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    print(possible_matches_round_1+possible_matches_round_2)

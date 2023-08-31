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
        teams.insert(1, teams.pop())


def goal_scoring(goal_probability: float) -> int:
    if goal_probability < 0 or goal_probability > 1:
        raise ValueError("Probability must be between 0 and 1")

    result = random.random()  # Generates a random number between 0 and 1

    if result < goal_probability:
        return 1
    else:
        return 0


def bonus_score(turns_A: int,
                turns_B: int,
                goal_score_A: int,
                goal_score_B: int,
                team: Team) -> List[int]:

    bonus_forward = 0
    bonus_midfielder = 0
    bonus_defence = 0

    if goal_score_A/turns_A > 0.8:
        bonus_midfielder = 0.2
        bonus_forward = 0.2
    elif goal_score_A/turns_A >= 0.7:
        bonus_midfielder = 0.1
        bonus_forward = 0.1
    elif goal_score_A/turns_A < 0.2:
        bonus_midfielder = -0.2
        bonus_forward = -0.2
    elif goal_score_A/turns_A <= 0.3:
        bonus_midfielder = -0.1
        bonus_forward = -0.1

    if goal_score_B/turns_B > 0.8:
        bonus_defence = -0.2
    elif goal_score_B/turns_B >= 0.7:
        bonus_defence = -0.1
    elif goal_score_B/turns_B < 0.2:
        bonus_defence = 0.2
    elif goal_score_B/turns_B <= 0.3:
        bonus_defence = 0.1

    if team.forward + bonus_forward < 1:
        bonus_forward = 0
    elif team.forward + bonus_forward > 9:
        bonus_forward = 9
    if team.midfielder + bonus_midfielder < 1:
        bonus_midfielder = 0
    elif team.midfielder + bonus_midfielder > 9:
        bonus_midfielder = 9
    if team.defence + bonus_defence < 1:
        bonus_midfielder = 0
    elif team.defence + bonus_defence > 9:
        bonus_midfielder = 9

    return [bonus_forward, bonus_midfielder, bonus_defence]


def play_match(session: Session, match: int) -> list[int]:
    team_goals_A = 0
    team_goals_B = 0

    teamM_A, teamM_B = session.query(Match).filter_by(num_match=match).all()

    team_A = session.query(Team).filter_by(id=teamM_A.id).first()
    team_B = session.query(Team).filter_by(id=teamM_B.id).first()

    print(teamM_A.id, team_A.defence)
    print(teamM_B.id, team_B.defence)

    TURNS = 12

    turns_A = round(
        TURNS*team_A.midfielder/(team_A.midfielder+team_B.midfielder)
        )
    turns_B = TURNS - turns_A
    turns = max(turns_A, turns_B)

    goal_scoring_A = team_A.forward/(team_A.forward+team_B.defence)
    goal_scoring_B = team_B.forward/(team_B.forward+team_A.defence)

    for turn in range(1, turns+1):
        if turn <= turns_A:
            team_goals_A += goal_scoring(goal_scoring_A)
        if turn <= turns_B:
            team_goals_B += goal_scoring(goal_scoring_B)

    bonus_A = bonus_score(turns_A, turns_B, team_goals_A, team_goals_B, team_A)
    bonus_B = bonus_score(turns_B, turns_A, team_goals_B, team_goals_A, team_B)

    return [team_goals_A, team_goals_B, bonus_A, bonus_B]


if __name__ == '__main__':
    possible_matches_round_1 = list(combinations(range(1, 5), 2))
    possible_matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    print(possible_matches_round_1+possible_matches_round_2)

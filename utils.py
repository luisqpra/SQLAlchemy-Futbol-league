import random
from models import Team, Match
from typing import List, Optional
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


def create_season(teams: list[int], session: Session, seasons: int) -> None:
    """
    The function creates a season by generating all possible matches
    between teams and adding them to the session.
    """
    for season in range(1, seasons+1):
        if len(teams) % 2:
            teams.append('Day off')
        n = len(teams)
        matchs = []
        nseason = (n/2)*(n-1)*(season-1)
        for j in range(1, n):
            for i in range(int(n/2)):
                if 'Day off' in (teams[i], teams[n - 1 - i]):
                    continue
                matchs.append((teams[i], teams[n - 1 - i]))
                if season % 2:
                    idA = teams[i]
                    idB = teams[n - 1 - i]
                else:
                    idA = teams[n - 1 - i]
                    idB = teams[i]
                team_A = Match(num_match=nseason+int(n/2)*(j-1)+i+1,
                               day_match=j, season=season, team_id=idA)
                team_B = Match(num_match=nseason+int(n/2)*(j-1)+i+1,
                               day_match=j, season=season, team_id=idB)
                session.add(team_A)
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
        bonus_forward = 0
    if team.midfielder + bonus_midfielder < 1:
        bonus_midfielder = 0
    elif team.midfielder + bonus_midfielder > 9:
        bonus_midfielder = 0
    if team.defence + bonus_defence < 1:
        bonus_defence = 0
    elif team.defence + bonus_defence > 9:
        bonus_defence = 0

    return [bonus_forward, bonus_midfielder, bonus_defence]


def play_match(session: Session,
               match: int,
               teamID: int,
               addstrategy: Optional[List] = None
               ) -> List[int] | List[List[int]]:
    team_goals_A = 0
    team_goals_B = 0

    teamM_A, teamM_B = session.query(Match).filter_by(num_match=match).all()

    team_A = session.query(Team).filter_by(id=teamM_A.team_id).first()
    team_B = session.query(Team).filter_by(id=teamM_B.team_id).first()

    TURNS = 12

    if teamID == 1:
        addStats(session, team_A, addstrategy)
    elif teamID == 2:
        addStats(session, team_B, addstrategy)

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

    if teamID == 1:
        lessenStats(session, team_A, addstrategy)
    elif teamID == 2:
        lessenStats(session, team_B, addstrategy)

    # save score and bonus
    saveScoreBonus(session,
                   teamM_A, teamM_B,
                   team_A,  team_B,
                   bonus_A, bonus_B,
                   team_goals_A, team_goals_B)

    return [team_goals_A, bonus_A, team_goals_B, bonus_B]


def addStats(session: Session,
             myTeam: Team,
             addstrategy: List[float]) -> None:
    myTeam.forward = round((myTeam.forward+addstrategy[0])*10)/10
    myTeam.midfielder = round((myTeam.midfielder+addstrategy[1])*10)/10
    myTeam.defence = round((myTeam.defence+addstrategy[2])*10)/10
    session.commit()


def lessenStats(session: Session,
                myTeam: Team,
                addstrategy: List[float]) -> None:
    # remove the strategy
    myTeam.forward = round((myTeam.forward-addstrategy[0])*10)/10
    myTeam.midfielder = round((myTeam.midfielder-addstrategy[1])*10)/10
    myTeam.defence = round((myTeam.defence-addstrategy[2])*10)/10
    session.commit()


def saveScoreBonus(session: Session,
                   teamM_A: Match,
                   teamM_B: Match,
                   team_A: Team,
                   team_B: Team,
                   bonus_A: List[float],
                   bonus_B: List[float],
                   team_goals_A: int,
                   team_goals_B: int
                   ) -> None:
    teamM_A.team_score = team_goals_A
    team_A.defence = round((team_A.defence+bonus_A[2])*10)/10
    teamM_A.bonus_defence = bonus_A[2]
    team_A.midfielder = round((team_A.midfielder+bonus_A[1])*10)/10
    teamM_A.bonus_midfielder = bonus_A[1]
    team_A.forward = round((team_A.forward+bonus_A[0])*10)/10
    teamM_A.bonus_forward = bonus_A[0]

    teamM_B.team_score = team_goals_B
    teamM_B.bonus_defence = bonus_B[2]
    team_B.defence = round((team_B.defence+bonus_B[2])*10)/10
    teamM_B.bonus_midfielder = bonus_B[1]
    team_B.midfielder = round((team_B.midfielder+bonus_B[1])*10)/10
    teamM_B.bonus_forward = bonus_B[0]
    team_B.forward = round((team_B.forward+bonus_B[0])*10)/10
    session.commit()


if __name__ == '__main__':
    possible_matches_round_1 = list(combinations(range(1, 5), 2))
    possible_matches_round_2 = [(i[1], i[0]) for i in possible_matches_round_1]
    print(possible_matches_round_1+possible_matches_round_2)

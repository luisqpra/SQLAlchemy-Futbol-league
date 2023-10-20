from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match, Team
import getch

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()


def main(myTeam: Team) -> None:
    # amound of matches
    num_match = int(session.query(Match).count()/2)

    # Intro
    print(F'***---STACTS {myTeam.name} --***')
    print(f'forward - {myTeam.forward}')
    print(f'midfielder - {myTeam.midfielder}')
    print(f'defence - {myTeam.defence}')
    print('\n')
    print('***--- START LEAGUE --***')
    print('\n')

    # playing mataches
    for i in range(1, 1+num_match):

        teamM_A, teamM_B = session.query(Match).filter_by(num_match=i).all()
        teamA = session.query(Team).filter_by(id=teamM_A.team_id).first()
        teamB = session.query(Team).filter_by(id=teamM_B.team_id).first()
        
        teamID = 0
        if myTeam.id == teamM_A.team_id:
            teamID = 1
        elif myTeam.id == teamM_B.team_id:
            teamID = 2
        # Stats My team vs Foe team
        if teamID > 0:
            print('\t\t***--- STATS --***')
            print(f'stats ({teamA.name}): \t\tstats ({teamB.name}):')
            print(f'forward - {teamA.forward} \t\t\tforward - {teamB.forward}')
            print(f'midfielder - {teamA.midfielder} \t\tmidfielder \
- {teamB.midfielder}')
            print(f'defence - {teamA.defence} \t\t\tdefence - {teamB.defence}')
            print('\n')

            print('Seleccione estrategia (A-C-D)')
            strategy = input('Ataque(A) - Creacion(C) - Defensa(D)\
 - Ninguna (Otra entrada)').lower()
            addstrategy = [0, 0, 0]
            # apply the strategy
            if strategy == 'a':
                addstrategy = [0.4, -0.2, -0.2]
            elif strategy == 'c':
                addstrategy = [-0.2, 0.4, -0.2]
            elif strategy == 'd':
                addstrategy = [-0.2, -0.2, 0.4]

            match_result = play_match(session=session,
                                      match=i,
                                      addstrategy=addstrategy,
                                      teamID=teamID
                                      )
            team_goals_A, bonus_A, team_goals_B, bonus_B = match_result

            print(F'***---MATCH DAY({teamM_B.day_match}) - \
SEASON({teamM_B.season}) --***')
            print(f'{teamA.name}({team_goals_A}) vs\
 {teamB.name}({team_goals_B})')
            print('\n')
            print(f'Bonus {teamA.name}: forward ({bonus_A[0]}) \
midfielder ({bonus_A[1]}) defence ({bonus_A[2]})')
            print(f'Bonus {teamB.name}: forward ({bonus_B[0]}) \
midfielder ({bonus_B[1]}) defence ({bonus_B[2]})')
            print('\n')

            print('Presione cualquier tecla para \
continual al siguiente partido')
            getch.getch()
            print('*-------------------------------------------------*')
            print('\n')
        # Other macthes
        else:
            match_result = play_match(session=session, match=i, teamID=teamID)
            team_goals_A, bonus_A, team_goals_B, bonus_B = match_result

    session.close()


if __name__ == '__main__':

    # Reading team table
    teams = session.query(Team).all()
    
    # Showing team names
    print('Equipos')
    for team in teams:
        print("Opcion:", team.id, "\t- Nombre:", team.name)
    # Checking option
    while True:
        try:
            equipo_id = int(input(f"Elige tu equipo (1 - {len(teams)})\t"))
            break
        except ValueError:
            print('Opcion no disponible vuelve a elegir')
    print('\n')
    # Reading the selected team
    myTeam = session.query(Team).filter_by(id=equipo_id).first()
    print(f'Tu equipo es "{myTeam.name}" -> ({myTeam.id})')
    print('\n')
    # Show time
    main(myTeam)

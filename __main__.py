from utils import play_match
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_url
from models import Match, Team
import getch

engine = create_engine(database_url)

Session = sessionmaker(bind=engine)
session = Session()


def main(myTeam):
    num_match = int(session.query(Match).count()/2)
    for i in range(1, 1+num_match):
        teamM_A, teamM_B = session.query(Match).filter_by(num_match=i).all()
        teamA = session.query(Team).filter_by(id=teamM_A.team_id).first()
        teamB = session.query(Team).filter_by(id=teamM_B.team_id).first()
        match_result = play_match(session=session, match=i)
        team_goals_A, bonus_A, team_goals_B, bonus_B = match_result
        if myTeam.id == teamM_A.team_id or myTeam.id == teamM_B.team_id:
            print(f'{teamA.name}({team_goals_A}) vs {teamB.name}({team_goals_B})\
    -> match {teamM_B.num_match}')
            print(f'Bonus {teamA.name}: forward ({bonus_A[0]}) \
midfielder ({bonus_A[1]}) defence ({bonus_A[2]})')
            print(f'Bonus {teamB.name}: forward ({bonus_B[0]}) \
midfielder ({bonus_B[1]}) defence ({bonus_B[2]})')
            print('Presione cualquier tecla para \
continual al siguiente partido')
            getch.getch()
    session.close()


if __name__ == '__main__':
    teams = session.query(Team).all()
    print('Equipos')
    for team in teams:
        print("Opcion:", team.id, "\t- Nombre:", team.name)
    # Validar que la seleccion del equipo
    while True:
        try:
            equipo_id = int(input(f"Elige tu equipo (1 - {len(teams)})\t"))
            break
        except ValueError:
            print('Opcion no disponible vuelve a elegir')
    myTeam = session.query(Team).filter_by(id=equipo_id).first()
    print(f'Tu equipo es "{myTeam.name}" -> ({myTeam.id})')
    main(myTeam)

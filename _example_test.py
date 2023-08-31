teams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def fixture(teams):
    if len(teams) % 2:
        teams.append('Day off')
    n = len(teams)
    matchs = []
    fixtures = []
    for fixture in range(1, n):
        for i in range(int(n/2)):
            matchs.append((teams[i], teams[n - 1 - i]))
            print((teams[i], teams[n - 1 - i]))
        teams.insert(1, teams.pop())
        fixtures.insert(int(len(fixtures)/2), matchs)
        matchs = []
    for fixture in fixtures:
        print(fixture)


fixture(teams)

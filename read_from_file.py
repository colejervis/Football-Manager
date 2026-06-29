from classes import *

def initialize_stadiums(stadiums, clubs):
    for id, stadium in stadiums.items():
        club = stadium.getClub()
        if club in clubs:
            clubs[club].setStadium(stadium)

def initialize_managers(managers, clubs):
    for id, manager in managers.items():
        club = manager.getClub()
        if club in clubs and club != 0:
            clubs[club].setManager(manager)
        elif club == 0:
            clubs[club].addManager(manager)

def initialize_players(players, clubs):
    for id, player in players.items():
        club = player.getClub()
        if club in clubs:
            clubs[club].addPlayer(player)

def initialize_leagues(clubs, leagues):
    for id, club in clubs.items():
        league = club.getLeague()
        if league in leagues:
            leagues[league].addClub(id, club)

def initialize_positions(players, positions):
    for player in players.values():
        positionID = player.getPosition()
        if positionID in positions.keys():
            player.setPosition(positions[positionID])

def initialize_loans(players, loans):
    for playerID, loanClub in loans.items():

        playerID = int(playerID)
        players[playerID].setLoanClub(loanClub)
        players[playerID].setClub(loanClub)

# NO LONGER IN USE - NATION IDs STORED IN PLAYER / MANAGER OBJECTS INSTEAD OF NATION OBJECT
def initialize_nations(nations, players, managers):
    for id, player in players.items():
        nationID = player.getNationality()
        if nationID in nations.keys():
            player.setNation(nations[nationID])

    for id, manager in managers.items():
        nationID = manager.getNationality()
        if nationID in nations.keys():
            manager.setNation(nations[nationID])




def read_players_from_file():
    players = {}
    with open("data/players.fmdata") as file:
        for line_number, line in enumerate(file, start=1):
            data = line.strip().split("-")

            # USED TO ENSURE CODE DOESN'T BREAK IF A PLAYER HAS AN BAD ENTRY
            if len(data) != 19:
                print(f"Line {line_number} has {len(data)} parts: {data}")
                continue

            p = Player(*data)
            players[int(data[0])] = p

        return players

def read_loans_from_file():
    loans = {}
    with open("data/loans.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            loans[data[0]] = data[1]
    return loans


def read_clubs_from_file():
    clubs = {}
    with open("data/clubs.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Club(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
            clubs[int(data[0])] = c
    return clubs


def read_managers_from_file():
    managers = {}
    with open("data/managers.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Manager(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            managers[int(data[0])] = c
    return managers


def read_stadiums_from_file():
    stadiums = {}
    with open("data/stadiums.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Stadium(data[0], data[1], data[2], data[3], data[4], data[5])
            stadiums[int(data[0])] = c
    return stadiums


def read_leagues_from_file():
    leagues = {}
    with open("data/leagues.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = League(data[0], data[1], data[2], data[3], data[4])
            leagues[int(data[0])] = c
    return leagues


def read_nations_from_file():
    nations = {}
    with open("data/nations.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            c = Nation(data[0], data[1], data[2], data[3])
            nations[int(data[0])] = c
    return nations


def read_positions_from_file():
    positions = {}
    with open("data/positions.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            p = Position(data[0], data[1], data[2])
            positions[int(data[0])] = p
    return positions
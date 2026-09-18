import os
import sqlite3

def initialize_stadiums(stadiums, clubs):
    for id, stadium in stadiums.items():
        club = stadium.getClubID()
        if club in clubs and club != 0:
            clubs[club].setStadiumID(id)

def initialize_managers(managers, clubs):
    for id, manager in managers.items():
        clubID = manager.getClubID()
        if clubID in clubs and clubID != 0:
            clubs[clubID].setManagerID(id)
        elif clubID == 0:
            clubs[clubID].addManager(manager)

def initialize_players(players, clubs):
    for id, player in players.items():
        clubID = player.getClubID()
        if clubID in clubs:
            clubs[clubID].addPlayer(player)

def initialize_leagues(clubs, leagues):
    for id, club in clubs.items():
        leagueID = club.getLeagueID()
        if leagueID in leagues:
            leagues[leagueID].addClub(id, club)






def read_players_from_file(Player):
    players = {}
    with open("data/players.fmdata", "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            data = line.strip().split("-")

            # USED TO ENSURE CODE DOESN'T BREAK IF A PLAYER HAS AN BAD ENTRY
            if len(data) != 34:
                print(f"Line {line_number} has {len(data)} parts: {data}")
                continue

            p = Player(*data)
            players[int(data[0])] = p

        return players





def fetch_from_database(tableName):
    conn = sqlite3.connect(database="data/fmdatabase.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM {tableName}")
    items = c.fetchall()
    conn.close()
    return items




def read_clubs_from_database(Club):
    clubs = {}
    items = fetch_from_database("clubs")
    for item in items:
        c = Club(*item)
        clubs[int(item[0])] = c
    return clubs


def read_managers_from_database(Manager):
    managers = {}
    items = fetch_from_database("managers")
    for item in items:
        c = Manager(*item)
        managers[int(item[0])] = c
    return managers


def read_stadiums_from_database(Stadium):
    stadiums = {}
    items = fetch_from_database("stadiums")
    for item in items:
        c = Stadium(*item)
        stadiums[int(item[0])] = c
    return stadiums


def read_leagues_from_database(League):
    leagues = {}
    items = fetch_from_database("leagues")
    for item in items:
        c = League(*item)
        leagues[int(item[0])] = c
    return leagues


def read_nations_from_database(Nation):
    nations = {}
    items = fetch_from_database("nations")
    for item in items:
        c = Nation(*item)
        nations[int(item[0])] = c
    return nations


def read_positions_from_database(Position):
    positions = {}
    items = fetch_from_database("positions")
    for item in items:
        c = Position(*item)
        positions[int(item[0])] = c
    return positions


def read_names_from_file(nations):
    nation_first_names_last_names = {}
    backup_nation_id = 1

    backup_first_path = os.path.join("data", "names", f"{backup_nation_id}_first.txt")
    backup_surname_path = os.path.join("data", "names", f"{backup_nation_id}_surnames.txt")

    for nation_id in nations.keys():
        first_path = os.path.join("data", "names", f"{nation_id}_first.txt")
        surname_path = os.path.join("data", "names", f"{nation_id}_surnames.txt")

        if not (os.path.exists(first_path) and os.path.exists(surname_path)):
            first_path = backup_first_path
            surname_path = backup_surname_path

        first_names = []
        surnames = []

        try:
            with open(first_path, "r", encoding="utf-8") as file:
                for line in file:
                    first_names.append(line.strip())

            with open(surname_path, "r", encoding="utf-8") as file:
                for line in file:
                    surnames.append(line.strip())

            nation_first_names_last_names[nation_id] = [first_names, surnames]

        except FileNotFoundError:
            print(f"Critical Error: Both primary files for '{nation_id}' and backup files are missing.")

    return nation_first_names_last_names


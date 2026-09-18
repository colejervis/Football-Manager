import sqlite3

def createTables(curs):

    curs.execute("PRAGMA foreign_keys = ON;")


    curs.execute("""CREATE TABLE IF NOT EXISTS nations (
        nation_id integer PRIMARY KEY,
        name text NOT NULL,
        abbreviation text NOT NULL, 
        reputation integer NOT NULL
    )""")

    curs.execute("""CREATE TABLE IF NOT EXISTS leagues (
        league_id integer PRIMARY KEY,
        nation_id integer NOT NULL, 
        name text NOT NULL, 
        reputation integer NOT NULL, 
        start_date integer NOT NULL, 
        promotion_places integer NOT NULL,
        leagueAboveID integer NOT NULL, 
        playoff_qualifying_positions integer NOT NULL,
        relegation_places integer NOT NULL,
        leagueBelowID integer NOT NULL,
        FOREIGN KEY (nation_id) REFERENCES nations(nation_id)
    )""")

    curs.execute("""CREATE TABLE IF NOT EXISTS clubs (
         club_id integer PRIMARY KEY,
         full_name text NOT NULL, 
         short_name text NOT NULL, 
         nickname text NOT NULL,
         founded_date integer NOT NULL,
         transfer_budget integer NOT NULL, 
         primary_color text NOT NULL, 
         secondary_color text NOT NULL, 
         reputation integer NOT NULL, 
         league_id integer NOT NULL,
         FOREIGN KEY (league_id) REFERENCES leagues(league_id)  
    )""")

    curs.execute("""CREATE TABLE IF NOT EXISTS positions (
        position_id integer PRIMARY KEY, 
        abbreviation text NOT NULL, 
        name text NOT NULL
    )""")

    curs.execute("""CREATE TABLE IF NOT EXISTS managers (
         manager_id integer PRIMARY KEY, 
         firstname text NOT NULL, 
         surname text NOT NULL, 
         age integer NOT NULL, 
         nation_id integer NOT NULL, 
         club_id integer NOT NULL, 
         preferred_formation_id integer NOT NULL, 
         preferred_playing_style text NOT NULL,
         FOREIGN KEY (nation_id) REFERENCES nations(nation_id),
         FOREIGN KEY (club_id) REFERENCES clubs(club_id)
    )""")

    curs.execute("""CREATE TABLE IF NOT EXISTS stadiums (
        stadium_id integer PRIMARY KEY,
        name text NOT NULL, 
        club_id integer NOT NULL, 
        capacity integer NOT NULL, 
        opened_date integer NOT NULL, 
        city text NOT NULL
    )""")


def loadDataIntoTables(curs):
    with open("data/nations.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO nations VALUES (?, ?, ?, ?)''', data)

    with open("data/leagues.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO leagues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)


    with open("data/clubs.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO clubs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)

    with open("data/positions.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO positions VALUES (?, ?, ?)''', data)

    with open("data/managers.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO managers VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data)

    with open("data/stadiums.fmdata") as file:
        for line in file:
            data = line.strip().split("-")
            curs.execute(f'''INSERT INTO stadiums VALUES (?, ?, ?, ?, ?, ?)''', data)


def dropAllTables(curs):
    curs.execute("""DROP TABLE IF EXISTS nations""")
    curs.execute("""DROP TABLE IF EXISTS clubs""")
    curs.execute("""DROP TABLE IF EXISTS leagues""")
    curs.execute("""DROP TABLE IF EXISTS managers""")
    curs.execute("""DROP TABLE IF EXISTS positions""")
    curs.execute("""DROP TABLE IF EXISTS stadiums""")




conn = sqlite3.connect(database="data/fmdatabase.db")
c = conn.cursor()

createTables(c)
loadDataIntoTables(c)


conn.commit()
conn.close()

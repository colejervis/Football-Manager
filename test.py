from read_from_file import *
from classes import *
from match_engine import *

def temp():
    game = 1
    players = read_players_from_file()
    positions = read_positions_from_file()
    clubs = read_clubs_from_file()
    leagues = read_leagues_from_file()
    managers = read_managers_from_file()
    stadiums = read_stadiums_from_file()
    loans = read_loans_from_file()

    initialize_loans(players, loans)
    initialize_players(players, clubs)
    initialize_leagues(clubs, leagues)
    initialize_managers(managers, clubs)
    initialize_stadiums(stadiums, clubs)
    initialize_positions(players, positions)

    f = Fixture(1, clubs[randint(1, 44)], clubs[randint(1, 44)], 1, None, "league")
    simulate_match(f)



temp()
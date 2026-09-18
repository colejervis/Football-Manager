from cli import *
from random import randint

from registry import get_class
GameObject = get_class("GameObject")
PlayerManager = get_class("PlayerManager")


def game_loop(game):

    while True:
        dateObject = game.getDateObject()

        game.morningDailyUpdate()

        # RUNS MENU IF NOT AUTO-SIMULATING
        if game.getHolidayStatus() is not True:

            # CHECKS IF USER'S TEAM HAD PLAYED THE DAY BEFORE, before running main menu
            dateObject, players, positions, clubs, leagues, managers, stadiums, nations = game.getAll()
            playerManagerID = game.playerManagerID
            playerManagerClubID = managers[playerManagerID].getClubID()
            clubObject = clubs[playerManagerClubID]
            if dateObject.getYesterdayDate() is not None:
                yDay, yMonth, yYear = dateObject.getYesterdayDate()
                for fixture in clubObject.getFixtures():
                    if fixture.getDate() == (yDay, yMonth, yYear):
                        view_fixture_menu(fixture, game)


            value = game_main_menu(game)
            if value == "Return to main menu":
                break
            elif value == "Advance":
                game.afternoonDailyUpdate()

        # ADVANCES DAYS AUTOMATICALLY WHEN 'HOLIDAYING'
        else:
            game.afternoonDailyUpdate()
            if game.getHolidayDate() == dateObject.getDate():
                game.endHoliday()



# USED FOR TESTING PURPOSES TO BYPASS INITIAL MANAGER CREATION SCREEN IMMEDIATELY
def autoCreateManager(game):

    managers = game.getManagers()

    ID = game.playerManagerID
    firstName = "Cole"
    lastName = "Jervis"
    age = 20
    nationID = 1
    clubID = randint(1,92)
    playerManager = PlayerManager(ID, firstName, lastName, age, nationID, clubID)

    for manager in managers.values():
        if manager.getClubID() == clubID:
            manager.setClubID(0)
            playerManager.setClubID(clubID)

    managers[int(playerManager.getID())] = playerManager

    return managers



def game_start():

    response = initial_menu()

    if response == "test":
        game = GameObject()
        autoCreateManager(game)
        game_loop(game)
    elif response == "start":
        game = GameObject()
        firstName, lastName, age, nationID, clubID = createManager(game)

        ID = game.playerManagerID
        playerManager = PlayerManager(ID, firstName, lastName, age, nationID, clubID)

        for manager in game.managers.values():
            if manager.getClubID() == clubID:
                manager.setClubID(0)
                playerManager.setClubID(clubID)

        game.managers[int(playerManager.getID())] = playerManager

        game_loop(game)



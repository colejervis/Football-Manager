import importlib


def get_class(class_name: str):

    if class_name == "Club":
        # format: importlib.import_module("folder.filename")
        module = importlib.import_module("classes.club")
        return module.Club

    elif class_name == "Date":
        module = importlib.import_module("classes.date")
        return module.Date

    elif class_name == "Fixture":
        module = importlib.import_module("classes.fixture")
        return module.Fixture

    elif class_name == "FreeAgents":
        module = importlib.import_module("classes.freeAgents")
        return module.FreeAgents

    elif class_name == "GameObject":
        module = importlib.import_module("classes.gameObject")
        return module.GameObject

    elif class_name == "Injury":
        module = importlib.import_module("classes.injury")
        return module.Injury

    elif class_name == "KnockoutTournament":
        module = importlib.import_module("classes.knockoutTournament")
        return module.KnockoutTournament

    elif class_name == "League":
        module = importlib.import_module("classes.league")
        return module.League

    elif class_name == "Manager":
        module = importlib.import_module("classes.manager")
        return module.Manager

    elif class_name == "Nation":
        module = importlib.import_module("classes.nation")
        return module.Nation

    elif class_name == "Player":
        module = importlib.import_module("classes.player")
        return module.Player

    elif class_name == "PlayerManager":
        module = importlib.import_module("classes.playerManager")
        return module.PlayerManager

    elif class_name == "Position":
        module = importlib.import_module("classes.position")
        return module.Position

    elif class_name == "PlayerSeasonData":
        module = importlib.import_module("classes.seasonData")
        return module.PlayerSeasonData

    elif class_name == "ClubSeasonData":
        module = importlib.import_module("classes.seasonData")
        return module.ClubSeasonData

    elif class_name == "Stadium":
        module = importlib.import_module("classes.stadium")
        return module.Stadium




    raise ValueError(f"Class {class_name} not recognized by registry helper.")
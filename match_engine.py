
import math
import random
import statistics

from classes import seasonData
from cli import *

CARD_PROBABILITY = 0.10
RED_CARD_PROBABILITY = 0.05
AVERAGE_AGGRESSION = 12

MIDFIELD_INFLUENCE = 0.35
SCALING_CONSTANT = 75
HOME_ADVANTAGE = 1.2
CUTOFF_POINT = 40
MAX_ATTRIBUTE_LIMIT = 20
ASSIST_PROBABILITY = 0.85


POSITION_MAPPING = {
        1: "goalkeeper",
        2: "defender",
        3: "defender",
        4: "defender",
        5: "midfielder",
        6: "midfielder",
        7: "midfielder",
        8: "attacker",
        9: "attacker",
        10: "attacker",
    }


# KNUTH's ALGORITHM
def poisson(lmbda):
    if lmbda <= 0:
        return 0
    L = math.exp(-lmbda)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def assignMinute(MATCH_TIME_RELATED_CONSTANTS):

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    minute = random.randint(start, end)
    return minute

def decreaseCondition(teamA, teamB, minute, MATCH_TIME_RELATED_CONSTANTS):

    players = []

    formationA, starting_elevenA, benchA, playingStyleA = teamA.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = teamB.getTeamSheet()

    for index, player in enumerate(starting_elevenA):
        if player.isSentOff:
            continue
        players.append((player, POSITION_MAPPING[formationA[index]]))

    for index, player in enumerate(starting_elevenB):
        if player.isSentOff:
            continue
        players.append((player, POSITION_MAPPING[formationB[index]]))

    for player, position in players:

        elapsed = minute - MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
        time_factor = 0.8 + 0.4 * (elapsed / MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"])

        if position == "goalkeeper":
            # Goalkeepers lose condition much more slowly
            loss = (
                0.25
                - player.stamina * 0.008
            )
        else:
            # Outfield players
            loss = (
                0.95
                - player.stamina * 0.02
                + player.work_rate * 0.01
            )

        player.condition = max(0, player.condition - loss * time_factor)

def considerInjuries(team, minute):

    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    injuryChancePerMinutePerTeam = 0.001

    if random.random() < injuryChancePerMinutePerTeam:

        # FILTERS OUT SENT OFF PLAYERS
        players_to_remove = []
        starting_eleven_copy = starting_eleven.copy()
        for player in starting_eleven_copy:
            if player.isSentOff:
                players_to_remove.append(player)
        for player in players_to_remove:
            starting_eleven_copy.remove(player)

        player = random.choice(starting_eleven_copy)
        player.isInjured = True

        event = {
            "minute": minute,
            "team": team,
            "type": "injury",
            "outcome": None,
            "player": player
        }

        return event


def considerSubstitution(team, minute):
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()

    # RETURNS INSTANTLY IF NOT ENOUGH SUBS OR BENCH IS EMPTY
    if len(bench) == 0:
        return None

    # CHECKS FOR INJURIES - IF SO, PLAYER WILL BE IMMEDIATELY SUBBED
    for indexPosition, player in enumerate(starting_eleven):
        if player.isSentOff:
            continue
        if player.isInjured:
            return player

    starting_eleven_copy = starting_eleven.copy()

    for player in starting_eleven_copy:
        if player.isSentOff:
            starting_eleven_copy.remove(player)

    starting_eleven_copy.sort(key=lambda p: p.condition)


    player = starting_eleven_copy[random.randint(0, 3)]

    if minute > 50 and player.condition < 40:
        chance = 0.2
        if random.random() < chance:
            return player

    return None



def makeSubstitution(team, player, minute, subCount):

    if subCount <= 0:
        return 0, subCount

    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    for index, playerInList in enumerate(starting_eleven):
        if player.isSentOff:
            continue
        if playerInList == player:
            break

    position = formation[index]

    bench.sort(key=lambda p: p.calculateRating(position) * 0.4 + p.condition * 0.6, reverse=True)
    for candidate in bench:
        if (candidate.calculateRating(position) * candidate.condition > (
                player.calculateRating(position) * player.condition)):
            bench.remove(candidate)
            starting_eleven[index] = candidate

            event = {
                "minute": minute,
                "team": team,
                "type": "substitution",
                "outcome": None,
                "joining-match": candidate,
                "leaving-match": player
            }

            team.setTeamSheet(formation, starting_eleven, bench, playingStyle)
            subCount -= 1
            return event, subCount
        else:
            # FAILED SUBSTITUTION - NO BENEFIT OF MAKING SUB
            return 0, subCount


def calculateFouls(team, MATCH_TIME_RELATED_CONSTANTS):

    playing_style_multipliers = {
        "Possession": 0.85,
        "Tiki Taka": 0.90,
        "Wing Play": 1.00,
        "Gegenpress": 1.30,
        "Counter Attack": 1.10,
        "Route One": 1.20
    }

    teamAggressions = []
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    for player in starting_eleven:
        if player.isSentOff:
            continue
        teamAggressions.append(player.aggression)
    total = sum(teamAggressions)
    multiplier = (total / len(teamAggressions)) / AVERAGE_AGGRESSION

    teamFoulTotal = MATCH_TIME_RELATED_CONSTANTS["BASE_FOUL_TOTAL"] * multiplier * playing_style_multipliers[playingStyle]

    totalFouls = poisson(teamFoulTotal)
    return totalFouls


def evaluateFoul(team, minute, events):
    formation, starting_eleven, bench, playingStyle = team.getTeamSheet()
    candidates = {}

    for index in range(len(starting_eleven)):
        if starting_eleven[index].isSentOff:
            continue
        player = starting_eleven[index]
        weight = (player.aggression * 0.40 + (MAX_ATTRIBUTE_LIMIT - player.decision_making) * 0.20 +
                  (MAX_ATTRIBUTE_LIMIT - player.defending) * 0.20 + (MAX_ATTRIBUTE_LIMIT - player.composure) * 0.20)
        candidates[player] = weight

    totalWeight = 0
    for player, weight in candidates.items():
        totalWeight += weight
    selection = random.uniform(0, totalWeight)
    runningTotal = 0
    for player, weight in candidates.items():
        runningTotal += weight
        if selection <= runningTotal:
            selectedFouler = player
            break

    if random.random() < CARD_PROBABILITY:
        if random.random() < RED_CARD_PROBABILITY:
            foulType = "red"
        else:
            foulType = "yellow"

            # CHECKS FOR DOUBLE YELLOW
            for event in events:
                if event["type"] == "foul" and event["outcome"] == "yellow" and event["player"] == selectedFouler:
                    foulType = "red"

    else:
        foulType = "no-card"

    event = {
        "minute": minute,
        "team": team,
        "type": "foul",
        "outcome": foulType,
        "player": selectedFouler
    }

    if foulType == "red":
        # REMOVES PLAYER FROM MATCH - SENDING OFF
        for index, player in enumerate(starting_eleven):
            if selectedFouler == player:
                selectedFouler.isSentOff = True

    return event


def calculateStyleFitMultiplier(team, game):
    # STYLE FIT CONSIDERS HOW WELL A TEAM'S SQUAD IS SUITED TO A PLAY STYLE, AND IS COMPARED WITH LEAGUE AVERAGE

    STYLE_FIT_PROFILES = {
        "Possession": {"passing": 0.30, "ball_control": 0.25, "vision": 0.20, "composure": 0.15, "decision_making": 0.10},
        "Tiki Taka": {"passing": 0.35, "vision": 0.25, "ball_control": 0.25, "decision_making": 0.15},
        "Wing Play": {"delivery": 0.30, "pace": 0.25, "dribbling": 0.20, "ball_control": 0.15, "decision_making": 0.10},
        "Gegenpress": {"work_rate": 0.25, "stamina": 0.20, "aggression": 0.15, "pace": 0.15, "defending": 0.15, "decision_making": 0.10},
        "Counter Attack": {"pace": 0.30, "decision_making": 0.20, "vision": 0.20, "finishing": 0.15, "composure": 0.15},
        "Route One": {"aerial": 0.35, "strength": 0.25, "pace": 0.25, "composure": 0.15},
    }

    leagues = game.getLeagues()
    leagueObject = leagues[team.getLeague()]
    clubs = leagueObject.getClubs()

    club_styleFitScore = {}

    for club in clubs.values():
        formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

        # IF TEAM SHEET NOT SET YET, IT WILL GET PLAYING STYLE FROM MANAGER INSTEAD
        if playingStyle is None:
            playingStyle = club.manager.getPreferredPlayingStyle()

        players_to_assess = []
        clubPlayers = club.getPlayers()
        clubPlayers.sort(key=lambda p: p.calculateRating(), reverse=True)
        for player in clubPlayers[:15]:
            if player.getPosition().getID() != 1:
                players_to_assess.append(player)
        totalScore = 0
        for player in players_to_assess:
            playerScore = 0
            for attribute, weight in STYLE_FIT_PROFILES[playingStyle].items():
                playerScore += getattr(player, attribute) * weight
            totalScore += playerScore
        averageScore = totalScore / len(players_to_assess)
        club_styleFitScore[club] = averageScore

    running_total = 0
    for club, score in club_styleFitScore.items():
        if club != team:
            running_total += score

    leagueAvg = running_total / (len(club_styleFitScore) - 1)
    teamAvg = club_styleFitScore[team]

    ratio = teamAvg / leagueAvg
    strength = 0.5  # 0 = no effect, 1 = full effect

    return 1 + (ratio - 1) * strength



def calculateChances(clubARatings, clubBRatings, teamObject, homeClub, styleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS):
    formation, starting_eleven, bench, playingStyle = teamObject.getTeamSheet()

    aGoalkeeping, aDefence, aMidfield, aAttack = clubARatings
    bGoalkeeping, bDefence, bMidfield, bAttack = clubBRatings

    threatScore = aAttack - bDefence + ((aMidfield - bMidfield) * MIDFIELD_INFLUENCE)

    if threatScore > CUTOFF_POINT:
        # value the uncapped formula would give exactly at the cutoff
        lmbda_at_cutoff = MATCH_TIME_RELATED_CONSTANTS["DEFAULT_CHANCES"] * 2.7 ** (CUTOFF_POINT / SCALING_CONSTANT)
        excess = threatScore - CUTOFF_POINT
        # grow more slowly beyond the cutoff, starting from that same point
        lmbda = lmbda_at_cutoff * 1.3 ** (excess / SCALING_CONSTANT)
    else:
        lmbda = MATCH_TIME_RELATED_CONSTANTS["DEFAULT_CHANCES"] * 2.7 ** (threatScore / SCALING_CONSTANT)

    if homeClub:
        lmbda = lmbda * HOME_ADVANTAGE

    playing_style_multipliers = {
        "Possession": 1.02,
        "Tiki Taka": 1.05,
        "Wing Play": 1.02,
        "Gegenpress": 1.10,
        "Counter Attack": 0.95,
        "Route One": 0.90
    }

    # BOOSTS / DECREASES AMOUNT OF CHANCES DEPENDING ON HOW GOOD A TEAM IS AT PLAYING A PARTICULAR STYLE COMPARED TO THE LEAGUE
    lmbda *= styleFitMultiplier

    chances = poisson(lmbda * playing_style_multipliers[playingStyle])

    return chances

ROLE_WEIGHT = {"goalkeeper": 0.0, "defender": 0.15, "midfielder": 0.45, "attacker": 1.0}

def evaluateChance(attackingTeam, defendingTeam, minute):

    formation, starting_eleven, bench, playingStyle = attackingTeam.getTeamSheet()
    weights = {}

    for index, position in enumerate(formation):
        player = starting_eleven[index]
        if player.isSentOff:
            continue
        group = POSITION_MAPPING[position]
        weights[player] = ROLE_WEIGHT[group] * player.calculateRating(position)

    total = sum(weights.values())
    number = random.uniform(0, total)
    cumulative = 0
    for player, weight in weights.items():
        cumulative += weight
        if number <= cumulative:
            selectedShooter = player
            break

    # SELECTS GOALKEEPER FROM DEFENDING SIDE

    dFormation, dStarting_eleven, dBench, dPlayingStyle = defendingTeam.getTeamSheet()
    selectedGoalkeeper = dStarting_eleven[0]


    # CALCULATES SHOT QUALITY BY COMPARING ATTACKER WITH GOALKEEPER
    shotQuality = (selectedShooter.finishing * 0.55 + selectedShooter.composure * 0.15 +
                   selectedShooter.football_iq * 0.15 + selectedShooter.positioning * 0.15 -
                   (selectedGoalkeeper.shot_stopping * 0.60 + selectedGoalkeeper.handling * 0.25 + selectedGoalkeeper.command * 0.15))

    playing_style_multipliers = {
        "Possession": 0.95,
        "Tiki Taka": 1.05,
        "Wing Play": 1.00,
        "Gegenpress": 1.05,
        "Counter Attack": 1.05,
        "Route One": 1.05
    }

    # USES SIGMOID FUNCTION TO CONVERT TO PROBABILITY
    scale = 7 # Dictates how much ratings matter
    goalProbability = (1 / (1 + math.exp(-shotQuality / scale))) * playing_style_multipliers[playingStyle]
    if goalProbability > 0.9:
        goalProbability = 0.9

    if random.random() < goalProbability:
        outcome = "goal"
        formation, starting_eleven, bench, playingStyle = attackingTeam.getTeamSheet()
    else:
        outcome = "miss"
        selectedShooter = None
        selectedAssister = None

    if outcome == "goal":
        # ASSIGNS ASSIST TO GOAL IF NEEDED
        assistProbability = 0.75
        if random.random() < assistProbability:
            candidates = {}
            for index in range(len(starting_eleven)):
                if starting_eleven[index].isSentOff:
                    continue
                player = starting_eleven[index]
                weight = player.passing * 0.50 + player.vision * 0.25 + player.decision_making * 0.15 + player.composure * 0.10
                candidates[player] = weight

            goalkeeper = starting_eleven[0]
            if goalkeeper in candidates:
                candidates[goalkeeper] *= 0.2

            if selectedShooter in candidates.keys():
                del candidates[selectedShooter]

            totalWeight = 0
            for player, weight in candidates.items():
                totalWeight += weight
            selection = random.uniform(0, totalWeight)
            runningTotal = 0
            for player, weight in candidates.items():
                runningTotal += weight
                if selection <= runningTotal:
                    selectedAssister = player
                    break
        else:
            selectedAssister = None

    event = {
        "minute": minute,
        "team": attackingTeam,
        "type": "chance",
        "outcome": outcome,
        "scorer": selectedShooter,
        "assister": selectedAssister,
        "xG": goalProbability
    }

    return event

def calculateRatings(club):

    positionRatings = [[], [], [], []]
    formation, starting_eleven, bench, playingStyle = club.getTeamSheet()

    for index, position in enumerate(formation):
        rating = starting_eleven[index].calculateRating(position)
        group = POSITION_MAPPING[position]
        if group == "goalkeeper":
            positionRatings[0].append(rating)
        elif group == "defender":
            positionRatings[1].append(rating)
        elif group == "midfielder":
            positionRatings[2].append(rating)
        elif group == "attacker":
            positionRatings[3].append(rating)

    for index, positionRating in enumerate(positionRatings):
        mean = sum(positionRating) / len(positionRating)
        positionRatings[index] = mean

    return positionRatings


def get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings):

    formationA, starting_elevenA, benchA, playingStyleA = homeTeam.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = awayTeam.getTeamSheet()

    events = fixture.getMatchEvents()

    homeBigChances = 0
    awayBigChances = 0
    homeXG = 0
    awayXG = 0
    homeFouls = 0
    awayFouls = 0
    homeYellowCards = 0
    awayYellowCards = 0
    homeRedCards = 0
    awayRedCards = 0

    homeTeam, awayTeam = fixture.getTeams()

    for event in events:

        # Chances / Fouls
        if event["type"] == "chance" and event["team"] == homeTeam:
            homeBigChances += 1
            homeXG += event["xG"]

        elif event["type"] == "chance" and event["team"] == awayTeam:
            awayBigChances += 1
            awayXG += event["xG"]

        elif event["type"] == "foul" and event["team"] == homeTeam:
            homeFouls += 1
            if event["outcome"] == "yellow":
                homeYellowCards += 1
            elif event["outcome"] == "red":
                homeRedCards += 1

        elif event["type"] == "foul" and event["team"] == awayTeam:
            awayFouls += 1
            if event["outcome"] == "yellow":
                awayYellowCards += 1
            elif event["outcome"] == "red":
                awayRedCards += 1

    # SHOTS

    playing_style_multipliers = {
        "Possession": 0.95,
        "Tiki Taka": 0.90,
        "Wing Play": 1.15,
        "Gegenpress": 1.10,
        "Counter Attack": 1.05,
        "Route One": 1.15
    }

    extraShots = poisson(homeBigChances * 0.5 * playing_style_multipliers[playingStyleA])  # low-quality/speculative efforts beyond the clear-cut chances
    homeShots = homeBigChances + extraShots
    extraShots = poisson(awayBigChances * 0.5 * playing_style_multipliers[playingStyleB])  # low-quality/speculative efforts beyond the clear-cut chances
    awayShots = awayBigChances + extraShots

    # POSSESSION

    playing_style_multipliers = {
        "Possession": 1.13,
        "Tiki Taka": 1.10,
        "Wing Play": 1.00,
        "Gegenpress": 1.05,
        "Counter Attack": 0.90,
        "Route One": 0.85
    }

    playing_style_multiplier = playing_style_multipliers[playingStyleA] - playing_style_multipliers[playingStyleB] + 1

    aGoalkeeping, aDefence, aMidfield, aAttack = homeRatings
    bGoalkeeping, bDefence, bMidfield, bAttack = awayRatings

    diff = aMidfield - bMidfield
    scale = 40  # controls how sharply midfield dominance swings possession
    homePossession = 50 + 50 * math.tanh(diff / scale) # Used over sigmoid as tanh is centered at 50/50
    homePossession += playing_style_multiplier * 10


    # Add a random swing of ±5%
    homePossession += random.uniform(-5, 5)
    homePossession = round(homePossession)

    awayPossession = 100 - homePossession

    # PASSES

    playing_style_multipliers = {
        "Possession": 1.15,
        "Tiki Taka": 1.20,
        "Wing Play": 0.95,
        "Gegenpress": 0.90,
        "Counter Attack": 0.75,
        "Route One": 0.65
    }

    basePasses = 100 + homePossession * 6
    homePasses = poisson(basePasses * playing_style_multipliers[playingStyleA])
    midfieldFactor = 1 + ((homeRatings[2] - awayRatings[2]) / 200)
    homePasses *= midfieldFactor

    basePasses = 100 + awayPossession * 6
    awayPasses = poisson(basePasses * playing_style_multipliers[playingStyleB])
    midfieldFactor = 1 + ((awayRatings[2] - homeRatings[2]) / 200)
    awayPasses *= midfieldFactor


    matchStatistics = {
        "homePossession": homePossession,
        "awayPossession": awayPossession,
        "homePasses": round(homePasses),
        "awayPasses": round(awayPasses),
        "homeShots": homeShots,
        "awayShots": awayShots,
        "homeBigChances": homeBigChances,
        "awayBigChances": awayBigChances,
        "homeXG": round(homeXG, 2),
        "awayXG": round(awayXG, 2),
        "homeFouls": homeFouls,
        "awayFouls": awayFouls,
        "homeYellowCards": homeYellowCards,
        "awayYellowCards": awayYellowCards,
        "homeRedCards": homeRedCards,
        "awayRedCards": awayRedCards,
    }

    return matchStatistics





def simulate_match(fixture, game):

    MATCH_TIME_RELATED_CONSTANTS = {
        "MINUTE_STARTING_FROM": 0,
        "MATCH_LENGTH": 90,
        "BASE_FOUL_TOTAL": 10,
        "DEFAULT_CHANCES": 3
    }

    homeTeam, awayTeam = fixture.getTeams()
    starting_players = []




    formation, starting_eleven, bench, playingStyle = homeTeam.autoPickTeam()
    homeTeam.setTeamSheet(formation, starting_eleven, bench, playingStyle)
    for player in starting_eleven:
        starting_players.append(player)

    formation, starting_eleven, bench, playingStyle = awayTeam.autoPickTeam()
    awayTeam.setTeamSheet(formation, starting_eleven, bench, playingStyle)
    for player in starting_eleven:
        starting_players.append(player)

    tournamentID = fixture.getLeagueID()
    if tournamentID is None:
        tournamentID = fixture.getTournamentID()

    for player in starting_players:
        player.seasonData[tournamentID].appearances += 1


    homeRatings = calculateRatings(homeTeam)
    awayRatings = calculateRatings(awayTeam)

    homeStyleFitMultiplier = calculateStyleFitMultiplier(homeTeam, game)
    awayStyleFitMultiplier = calculateStyleFitMultiplier(awayTeam, game)

    homeChances = calculateChances(homeRatings, awayRatings, homeTeam, True, homeStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)
    awayChances = calculateChances(awayRatings, homeRatings, awayTeam,False, awayStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)

    homeFouls = calculateFouls(homeTeam, MATCH_TIME_RELATED_CONSTANTS)
    awayFouls = calculateFouls(awayTeam, MATCH_TIME_RELATED_CONSTANTS)

    predeterminedEvents = []
    for i in range(homeChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "opposing-team": awayTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(awayChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "opposing-team": homeTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(homeFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    for i in range(awayFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    events = []

    homeSubs = 5
    awaySubs = 5

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    for minute in range(start, end):

        # DECREASING PLAYER CONDITION
        decreaseCondition(homeTeam, awayTeam, minute, MATCH_TIME_RELATED_CONSTANTS)

        # INJURIES

        event = considerInjuries(homeTeam, minute)
        if event is not None:
            events.append(event)

        event = considerInjuries(awayTeam, minute)
        if event is not None:
            events.append(event)


        # CHECKS IF A TEAM WISHES TO MAKE A SUB

        player = considerSubstitution(homeTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(homeTeam, player, minute, homeSubs)
            if event != 0: # FAILED SUBSTITUTION IF NONE IS RETURNED
                events.append(event)
                homeSubs = subCount

        player = considerSubstitution(awayTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(awayTeam, player, minute, awaySubs)
            if event != 0:
                events.append(event)
                awaySubs = subCount

        # EVALUATES EVENTS IF THEY HAPPEN IN THE MINUTE WE'RE IN
        for predeterminedEvent in predeterminedEvents:
            if predeterminedEvent["minute"] == minute:
                if predeterminedEvent["type"] == "chance":
                    event = evaluateChance(predeterminedEvent["team"], predeterminedEvent["opposing-team"], minute)
                    events.append(event)
                elif predeterminedEvent["type"] == "foul":
                    event = evaluateFoul(predeterminedEvent["team"], minute, events)
                    events.append(event)

        # CALCULATES SCORE
        homeScore, awayScore = 0, 0
        for event in events:
            if event["outcome"] == "goal":
                if event["team"] == homeTeam:
                    homeScore += 1
                elif event["team"] == awayTeam:
                    awayScore += 1

    fixture.setMatchEvents(events)
    statistics = get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings)
    fixture.setMatchStatistics(statistics)
    fixture.setScore(homeScore, awayScore)



def simulate_match_extra_time(fixture, game):

    MATCH_TIME_RELATED_CONSTANTS = {
        "MINUTE_STARTING_FROM": 90,
        "MATCH_LENGTH": 30,
        "BASE_FOUL_TOTAL": 3,
        "DEFAULT_CHANCES": 1
    }


    homeTeam, awayTeam = fixture.getTeams()

    homeRatings = calculateRatings(homeTeam)
    awayRatings = calculateRatings(awayTeam)

    homeStyleFitMultiplier = calculateStyleFitMultiplier(homeTeam, game)
    awayStyleFitMultiplier = calculateStyleFitMultiplier(homeTeam, game)

    homeChances = calculateChances(homeRatings, awayRatings, homeTeam, True, homeStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)
    awayChances = calculateChances(awayRatings, homeRatings, awayTeam, False, awayStyleFitMultiplier, MATCH_TIME_RELATED_CONSTANTS)

    homeFouls = calculateFouls(homeTeam, MATCH_TIME_RELATED_CONSTANTS)
    awayFouls = calculateFouls(awayTeam, MATCH_TIME_RELATED_CONSTANTS)

    predeterminedEvents = []
    for i in range(homeChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "opposing-team": awayTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(awayChances):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "opposing-team": homeTeam,
            "type": "chance",
        }
        predeterminedEvents.append(event)

    for i in range(homeFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": homeTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    for i in range(awayFouls):
        event = {
            "minute": assignMinute(MATCH_TIME_RELATED_CONSTANTS),
            "team": awayTeam,
            "type": "foul",
        }
        predeterminedEvents.append(event)

    events = fixture.getMatchEvents()

    homeSubs = 1
    awaySubs = 1

    start = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"]
    end = MATCH_TIME_RELATED_CONSTANTS["MINUTE_STARTING_FROM"] + MATCH_TIME_RELATED_CONSTANTS["MATCH_LENGTH"]

    for minute in range(start, end):

        # DECREASING PLAYER CONDITION
        decreaseCondition(homeTeam, awayTeam, minute, MATCH_TIME_RELATED_CONSTANTS)

        # INJURIES

        event = considerInjuries(homeTeam, minute)
        if event is not None:
            events.append(event)

        event = considerInjuries(awayTeam, minute)
        if event is not None:
            events.append(event)

        # CHECKS IF A TEAM WISHES TO MAKE A SUB

        player = considerSubstitution(homeTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(homeTeam, player, minute, homeSubs)
            if event != 0:  # FAILED SUBSTITUTION IF 0 IS RETURNED
                events.append(event)
                homeSubs = subCount

        player = considerSubstitution(awayTeam, minute)
        if player is not None:
            event, subCount = makeSubstitution(awayTeam, player, minute, awaySubs)
            if event != 0:
                events.append(event)
                awaySubs = subCount

        # EVALUATES EVENTS IF THEY HAPPEN IN THE MINUTE WE'RE IN
        for predeterminedEvent in predeterminedEvents:
            if predeterminedEvent["minute"] == minute:
                if predeterminedEvent["type"] == "chance":
                    event = evaluateChance(predeterminedEvent["team"], predeterminedEvent["opposing-team"], minute)
                    events.append(event)
                elif predeterminedEvent["type"] == "foul":
                    event = evaluateFoul(predeterminedEvent["team"], minute, events)
                    events.append(event)

        # CALCULATES SCORE
        homeScore, awayScore = 0, 0
        for event in events:
            if event["outcome"] == "goal":
                if event["team"] == homeTeam:
                    homeScore += 1
                elif event["team"] == awayTeam:
                    awayScore += 1

    fixture.setScore(homeScore, awayScore)


    fixture.setMatchEvents(events)
    statistics = get_match_statistics(fixture, homeTeam, awayTeam, homeRatings, awayRatings)
    fixture.setMatchStatistics(statistics)


def evaluatePenalty(selectedShooter, selectedGoalkeeper):
    # CALCULATES SHOT QUALITY BY COMPARING ATTACKER WITH GOALKEEPER
    shotQuality = (selectedShooter.finishing * 0.55 + selectedShooter.composure * 0.15 +
               selectedShooter.football_iq * 0.15 + selectedShooter.positioning * 0.15 -
                   (selectedGoalkeeper.shot_stopping * 0.60 + selectedGoalkeeper.handling * 0.25 + selectedGoalkeeper.command * 0.15))

    # USES SIGMOID FUNCTION TO CONVERT TO PROBABILITY
    scale = 15  # Dictates how much ratings matter
    goalProbability = 1 / (1 + math.exp(-shotQuality / scale))

    if random.random() < goalProbability:
        return True
    else:
        return False



def simulate_penalties(fixture):
    homeTeam, awayTeam = fixture.getTeams()

    formationA, starting_elevenA, benchA, playingStyleA = homeTeam.getTeamSheet()
    formationB, starting_elevenB, benchB, playingStyleB = awayTeam.getTeamSheet()

    starting_elevenA_copy = starting_elevenA.copy()
    starting_elevenB_copy = starting_elevenB.copy()

    starting_elevenA_copy.sort(key=lambda p: p.finishing * 0.6 + p.composure * 0.4, reverse=True)
    starting_elevenB_copy.sort(key=lambda p: p.finishing * 0.6 + p.composure * 0.4, reverse=True)

    homeTeamPenaltyTakers = []
    awayTeamPenaltyTakers = []

    events = fixture.getMatchEvents()

    for i in range(len(starting_elevenA_copy)):
        if starting_elevenA_copy[i].isSentOff is True:
            continue
        homeTeamPenaltyTakers.append(starting_elevenA_copy[i])

    for i in range(len(starting_elevenB_copy)):
        if starting_elevenB_copy[i].isSentOff is True:
            continue
        awayTeamPenaltyTakers.append(starting_elevenB_copy[i])

    homeGoalkeeper = starting_elevenA[0]
    awayGoalkeeper = starting_elevenB[0]

    homeScore = 0
    awayScore = 0

    for i in range(5):

        selected_shooter = homeTeamPenaltyTakers[i]
        selected_goalkeeper = awayGoalkeeper

        hasScored = evaluatePenalty(selected_shooter, selected_goalkeeper)
        if hasScored:
            homeScore += 1
            outcome = "scored"
        else:
            outcome = "missed"

        event = {
            "minute": 999,
            "team": homeTeam,
            "type": "penalty",
            "outcome": outcome,
            "taker": selected_shooter,
            "goalkeeper": selected_goalkeeper,
        }

        events.append(event)

        selected_shooter = awayTeamPenaltyTakers[i]
        selected_goalkeeper = homeGoalkeeper

        hasScored = evaluatePenalty(selected_shooter, selected_goalkeeper)
        if hasScored:
            awayScore += 1
            outcome = "scored"
        else:
            outcome = "missed"

        event = {
            "minute": 999,
            "team": awayTeam,
            "type": "penalty",
            "outcome": outcome,
            "taker": selected_shooter,
            "goalkeeper": selected_goalkeeper,
        }

        events.append(event)

        # ENDS SHOOTOUT EARLY IF IMPOSSIBLE TO CATCH UP

        remaining = 5 - (i + 1)

        if homeScore > awayScore + remaining:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return

        if awayScore > homeScore + remaining:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return


    # CHECKS FOR WINNER AFTER FIRST 5

    if homeScore != awayScore:
        fixture.setPenaltyScore(homeScore, awayScore)
        fixture.setMatchEvents(events)
        return

    index = 5

    # SUDDEN DEATH

    while True:

        # Reuse players once everyone has taken one
        if index >= len(homeTeamPenaltyTakers):
            index = 0

        # Home penalty
        homeScored = evaluatePenalty(homeTeamPenaltyTakers[index], awayGoalkeeper)

        events.append({
            "minute": 999,
            "team": homeTeam,
            "type": "penalty",
            "outcome": "scored" if homeScored else "missed",
            "taker": homeTeamPenaltyTakers[index],
            "goalkeeper": awayGoalkeeper,
        })

        if homeScored:
            homeScore += 1

        # Away penalty
        awayScored = evaluatePenalty(awayTeamPenaltyTakers[index], homeGoalkeeper)

        events.append({
            "minute": 999,
            "team": awayTeam,
            "type": "penalty",
            "outcome": "scored" if awayScored else "missed",
            "taker": awayTeamPenaltyTakers[index],
            "goalkeeper": homeGoalkeeper,
        })

        if awayScored:
            awayScore += 1

        # Sudden death
        if homeScored != awayScored:
            fixture.setPenaltyScore(homeScore, awayScore)
            fixture.setMatchEvents(events)
            return

        index += 1





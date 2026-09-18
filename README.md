## Football Manager Simulation

A text-based football management simulation written in Python.

The player takes control of a football club and is responsible for managing the squad, navigating league competitions, and guiding the club through multiple seasons. The project focuses on simulating the football environment using advanced algorithms and modelling techniques rather than recreating matches in real time visually.


### File Structure

#### Classes

* Contains all class definitions in their own isolated files. 
* To prevent circular imports, registry.py is used in conjunction with the importlib library to prevent circular import issues

#### Data

* Contains two files for each nation ID, one file containing first names and the other, last names. These are retrieved using a function inside read_from_file.py
* The fmdatabase.db file is stored here, containing tables for clubs, managers, stadiums, leagues and nations as of the start of the 2025/26 season. These are accessed through SQLLite 3 functions in read_from_file.py

#### Root Level

* main.py - Run this to start the game
* cli.py - Contains all procedures / functions for the command line interface
* game_orchestration.py - Contains the primary game loop
* match_engine.py - Contains all functions relating to the match engine / football match simulation calculations
* mathematical_models.py - Contains reused code such as the statistical modelling functions (softmax, sigmoid, bell curve, Poisson distribution), rounding functions, probability-based random selection
* player_generation_engine.py - Contains functions for the youth intake system, player generation system, and fake player database construction
* read_from_file.py - Used to access data stored in the data folder, such as regen names and primary database
* sqlscripts.py - Used to query and make changes to the primary database

### Features

#### Game Object

* Initializes database by getting club, league, manager, nation and positions data from SQLLite 3 database tables.
* Contains dictionaries for all different types of game objects, which are assigned keys, making lookup instantaneous O(1). 
* Season Update uses a mathematical model which finds an approximate target reputation based on their league finish using a linear equation, and the club will begin to 'home in' on that target every season. It is also responsible for dealing with promotion and relegation

#### Statistical Modelling

* Poisson Distribution using Knuth's algorithm - instead of using deterministic, predictable outcomes, as these events such as  fouls, shots, and chances are independent occurrences inside a fixed time frame, these outcomes are given realistic variance. Whilst extreme outcomes are rare, this prevents the same match outcomes being repeated every time.
* Box-muller transforms for bell curves - the bell curve shape is extremely useful, with the majority of data outcomes being centred inside the first few deviations of the baseline mean. It follows the 68-95-99.7 empirical rule, where with more deviations, extreme data outcomes become more unlikely, and the majority are centered around the mean.
* Softmax Functions are used to dynamically expand or shrink the gaps between probabilities, and normalize them. This can be done by adjusting the temperature, allowing for dynamic use cases such as squad rotation, where temperature could be adjusted based on match importance.
* Sigmoid functions can convert raw data into a probability between 0 and 1, and is mapped onto an 'S' shape, where small differences around the centre have huge impacts but small differences around the extremes have little impact.

#### Club Management

* Features an auto-pick team algorithm which cycles through position from least-depth to most-depth, and either candidates for the position a score and the outcome is determined using a softmax algorithm, or for the media prediction function (measuring the exact strength of the team), will pick the single best suited candidate for each position
* Auto-split players to split the club's roster between the first team and youth team: gives every player a score based on ability, potential, and age, and cycles through each position working through a matrix of target depth for each position. If there are any outliers, they are swapped.
* Calculate Betting Odds function in the League Menu where the user can assess their team strength against other teams in the league. The club's rating score (made of 95% of the average of the starting XI and 5% of the bench using the autoPickTeam best XI) is passed into a softmax function, and converted to fractional odds

#### Player Management

* Uses a position-weighted approach to player rating calculation, where the value of some 'key' attributes, such as dribbling, pace and shooting, are given more importance by passing them into an exponential equation. If the player can play the position as a secondary position, they are given a 5% reduction, and if they can't play there at all, this becomes a 20% reduction.
* Player market value calculation uses a piecewise-exponential approach, with certain waypoints being used at each ability level. After the player's rating is passed into the exponential equation, multipliers for age, contract length, club reputation (the club's bargaining power) are applied.
* Player star rating uses sigmoid function - compares a player relative to other players in your squad. Uses a sigmoid function centred at the club's average player's current ability. The 'S' shape means that small changes around the mean will be noticeable, whereas changes at the extremes are not very noticeable, reflecting how real world managers may assess player development.
* Player development uses a bank system, where points decrease as you get older, before becoming negative at \~32 years old. Factors such as playing percentage and club reputation also change the speed of which a player develops. When the player has more than one point, an attribute is chosen based on the positional weightings, and an exponential which causes probabilities to tail off as the attribute approaches 20. A random physical attribute is decreased for player decline.
* Players may also pick up injuries, is this is flagged in the match engine. In the post match processing, the player is assigned an Injury Object, which is instantiated from the Injury class and the type selected is random, based on the pre-determined probabilities

#### Player Generation

* Wage generation system for fake players (generated players for the fake database) use an exponential equation mapping ability to wage, and uses a further exponential to generate a percentage modifier which reduces players under 21's wage
* Nationality generation uses Sigmoid Logistic functions to map club reputation to amount of foreign players, creating an effect where lower reputation clubs have more english players and this rises steeply to high reputation clubs which recruit more foreign players with increased 'pull-power'
* Uses a mapping system where some nations are assigned their 'geographical neighbors'. This means the weighting of these foreign nations are given a boost based on 60 * the multiplier, before being passed into a softmax function
* Player potentials are modelled using a bell curve shape (box-muller transform) centered around a base mean * a multiplier based on club, nation and league reputation - this creates the effect where most players are bang average, with few outliers and either extreme.
* Player ratings for fake squads for each club are modelled using a bell curve, with starting XI players and reserves using a certain percentage of the club's reputation as the base mean. Players will go through an automatic development phase until their calculated ability matches their pre-assigned ability.

#### Match Engine

* Amount of chances for each team modelled using a threat score between the team's attack and defense, and a small value of the midfield vs opposition midfield. This is passed into an exponential equation, causing high threat scores to result in higher chances, up to a certain point where the effect of this drops. This is multiplied by the base number of chances. This lambda value is put into a poisson distribution to add variance.
* Amount of fouls for each team is modelled by getting a multiplier from dividing the average aggression of the team by the average aggression of the league. This multiplier is applied to the base number of fouls, which is passed into a Poisson distribution.
* These chance / foul events are added to a predeterminedEvents dictionary, and assigned a minute in which they occur. The match loop begins, and if the chance / foul happens, their outcome is evaluated. Every minute player condition decreases. Both teams assess whether they wish to make a substitution.
* Chance evaluation uses a sigmoid function, with a combination of the attacker's finishing and composure being subtracted from the goalkeeper's diving and shot stopping. This is passed into a sigmoid function, which converts it into a probability. This probability acts as xG. If the goal is scored, the shooter is found by using weightings of all player's positions on the pitch and their individual attributes, and an assister is decided by assigning scores to all players that aren't the shooter based on their passing, vision and composure.
* Foul evaluation works by giving every player in the team's starting XI a score based on defending, composure, decision making and aggression. A random player is picked using this weightings. This the outcome of it being a red or yellow is based upon predetermined probabilities. If a player is sent off, they are removed from the game
* When calculating the amount of chances / fouls and evaluating their outcomes, weightings based on the team's playing style are used to modify these. For example, a team that plays counter attacking football may have a lower amount of chances but the chances they do get, they have a higher chance of scoring from.
* The amount of chances can be reduced or increased further based on the style fit multiplier, measuring how effective a team is at their playing style.
* Match statistics are generated. xG is derived from the shot probability used when evaluating a chance. Extra shots are generated from half the number of base chances and added to the number of base chances. Possession is calculated by finding the difference in midfield and multiplying it by the team's style multiplier for possession. This is passed into a sigmoid function, as it mirrors how small margins should result in the midfield battle being won or lost. Passes are derived from possession, and passed into a poisson distribution.

#### Databases

* Uses SQLLite 3 / SQL for pre-game database management of clubs, managers, stadiums, positions, and leagues
* Sources player names for newgens from the Python names-dataset library

#### Performance

* Contains dictionaries for all different types of game objects, which are assigned keys, making lookup instantaneous O(1). 
* Caching of player fit style multipliers (these were previously calculated every match, drastically slowing down performance)
* heavy O(n) processes such as player development and the style fit multiplier calculations are only called once per week

#### Other Features

* Holiday system - non-input simulation into the future - advances into the future without running any CLI elements
* Command Line Interface

#### Technologies

* Python 3
* Object-Oriented Programming
* SQLLite 3 Database Storage

### Project Status

This project is currently in active development as part of an A-Level Computer Science NEA.

#### Upcoming features include:

* Transfer negotiations
* AI Transfers
* Contract renewals
* Player Dynamics
* Cup competitions
* Save/load functionality

#### Future planning

This project will eventually be ported to LUA and the Defold engine, where it will include a GUI, as part of my Computer Science NEA project. I intend to keep developing this in Python until most key features are added.


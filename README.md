## Football Manager Simulation

A text-based football management simulation written in Python.

The player takes control of a football club and is responsible for managing the squad, navigating league competitions, and guiding the club through multiple seasons. The project focuses on simulating the football environment rather than recreating matches in real time.

### Features

#### Club Management

* Manage a football club of your choice
* View club information, players, manager and stadium
* Team sheet management with automatic team selection

#### Player Management

* Detailed player profiles
* Player Ratings and Star Ratings
* Dynamic transfer market values
* Youth academy and first team separation
* Player, club, stadium and manager search database
* Shortlisting system
* Player stat tracking across all competitions (goals, assists, clean sheets, appearances, cards)

#### Match Engine

* Minute-by-minute simulation (90 minutes, plus extra time and penalties for knockout fixtures)
* Poisson-distributed chance and foul events
* Six distinct playing styles (Possession, Tiki-Taka, Wing Play, Gegenpress, Counter Attack, Route One) each with it's own multipliers affecting chance creation, possession, passing volume, and chance quality
* Home advantage and squad style-fit vs league average factored into chance creation volume
* Automatic, formation-aware team selection - key players are selected almost every week while backup options genuinely rotate
* Secondary position eligibility with a familiarity penalty when played out of position
* Goal / shot outcomes determined using sigmoid model comparing attacker against goalkeeper
* Assist attribution weighted by passing, decision-making and composure
* Dynamic player condition/fatigue affecting selection and performance over the course of a match
* In-match injuries and automatic substitutions
* Two-legged knockout ties with aggregate scoring
* Full match statistics / report containing statistics such as possession, passes, shots, big chances, xG, fouls and cards

#### Competitions

* League table simulation
* Full season fixture generation
* Automatic match simulation via Match Engine
* Promotion and relegation
* Promotion playoffs

#### Databases

* Players
* Clubs
* Managers
* Leagues
* Stadiums
* Nations
* Positions

#### Other Features

* Holiday system - non-input simulation into the future
* Seasonal and annual game updates
* Universal search
* Free agent database

#### Technologies

* Python 3
* Object-Oriented Programming
* File-based data storage (.fmdata files)

### Project Status

This project is currently in active development as part of an A-Level Computer Science NEA.

#### Upcoming features include:

* Transfer negotiations
* AI Transfers
* Contract renewals
* 'Newgen' fake player generation
* Player development
* Cup competitions
* Save/load functionality

#### Future planning

This project will eventually be ported to LUA and the Defold engine, where it will include a GUI, as part of my Computer Science NEA project. I intend to keep developing this in Python until most key features are added.
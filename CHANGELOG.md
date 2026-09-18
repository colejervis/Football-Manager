## v0.4.0

### Added
- Player Development + Decline - using a points bank system, which is mostly influenced by age, along with multipliers for club reputation and playing time
- Annual Youth Intakes for clubs 
- Player generation system, where base attributes are determined initially from a base attribute profile by position and shifted from a range of between -2 and 2, then players are given potential abilities, nationalities, names, etc
- 'Temporary' players are generated for a single match only when a team cannot name a starting XI and bench of real players
- If a team gets five players sent off, that team forfeits the match: it is ended early and a 3-0 win is awarded to the opposing team - this avoids edge-case bugs in match engine where the engine assumes the team has sufficient players on the pitch
- Entirely fake database generation
- Sky Bet League One / Two, and their clubs, managers, and stadiums
- The user can now change the formation, playing style, starting eleven and bench themselves, and will be prompted to do so if not on holiday.

### Changed
- Architectural Change - Game initialization is now done inside the game object initialization method
- Architectural Change - Except for players (this is temporary), and player names, the pre-game database now uses SQLLite3 instead of .fmdata files
- Architectural Change - Class definitions are now stored in their own files instead of the unified classes.py file - to prevent circular import issues, a registry system is used.
- Reconfigured club seasonal data to operate similar to players - this data for each competition is now stored in a dictionary rather than static variables and is carried forward beyond the current season
- Overhauled the AI team selection system for matches - split into two separate systems, match (where the team rotates using a softmax function), and best XI, where the team will choose their undisputed best team
- Overhauled AI squad registration / first-team and youth divide - previously, the system only considered age and some extreme cases of ability disparency, whereas now the club will try to build a 22-man first-team squad, considering mainly age, current ability and potential
- Simulation Speed / Performance - Previously the Style fit Multiplier was being run twice for every match, now is only calculated once per week per team
- Simulation Speed / Performance - Youth Intakes use a rolling total for IDs instead of max(self.players.keys()) being run every single time
- Simulation Speed / Performance - Player development now happens weekly, not daily 
- Simulation Speed / Performance - Running total used for scoreline in match engine, rather than iterating through all match events to find goals
- Increased modularity by splitting classes into their own individual files and using a registry to allow a class to import another class if they need it for instantiation

### Fixed
- AI Team selection system will now ensure it has one goalkeeper, defender midfielder and attacker rather than just seven of the best remaining players outside the starting XI
- Promotion / Relegation issue where some teams did not change leagues due to concurrent modification (removal of teams from a list whilst iterating over it)
- Due to club seasonal data system change, playoff games were considered wrongly as being normal league games, leading to incorrect clubs getting promoted - the playoffs are now considered its own entity entirely
- Issue where in extra-time the away club would use the home team's play style fit multiplier instead of their own
- Issue where possession calculation could spill over 100% with enough favourable factors, e.g big midfield gap, style mismatch, high random roll
- Issue where sorting by goal contributions did not change view correctly - this was due to a dictionary key typo
- If a roll was > 0.75 in the player generation nationality system, the foreign nation could be completely random - this was entirely unrealistic and the system now uses softmax with the nation's reputation
- With fake player database generation, defenders were higher rated than attackers in every club as defenders took up the higher ratings before attackers could, this is now fixed as positions are shuffled.
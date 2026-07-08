## v0.2.0

### Added
- Youth academy system - separation system from first-team players
- Championship playoff system and basis for other knockout tournaments
- Automatic promotion and relegation between divisions.

### Changed
- Added EFL Championship clubs, players, stadiums, managers
- Expanded player database using data from Football Manager - attributes for each player are weighted into a smaller, more appropiate number of attributes for a simulation of this size
- Completely redesigned player rating calculation - based on FM's 1-200 CA system where high attribute increases are no longer linear
- Redesigned exponential player rating calculation into three separate equations, to better match the new player rating approach
- Improved season progression and fixture generation.

### Fixed
- Various season transition and playoff scheduling bugs
class Manager:
    def __init__(self, manager_id, firstname, surname, age, nation_id, club_id, preferred_formation_id, preferred_playing_style):
        self.id = int(manager_id)
        self.firstname = firstname
        self.surname = surname
        self.age = int(age)
        self.nationID = int(nation_id)
        self.clubID = int(club_id)
        self.preferred_formation_id = preferred_formation_id
        self.preferred_playing_style = preferred_playing_style

    def getID(self):
        return self.id

    def getName(self):
        return self.firstname + " " + self.surname

    def getSurname(self):
        return self.surname

    def getAge(self):
        return self.age

    def incrementAge(self):
        self.age = self.age + 1

    def getNationID(self):
        return self.nationID

    def setNationID(self, nationID):
        self.nationID = nationID

    def getClubID(self):
        return self.clubID

    def setClubID(self, newID):
        self.clubID = newID

    def getPreferredFormation(self):
        return self.preferred_formation_id

    def getPreferredPlayingStyle(self):
        return self.preferred_playing_style
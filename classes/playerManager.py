class PlayerManager:
    def __init__(self, manager_id, firstname, surname, age, nationID, clubID):
        self.id = int(manager_id)
        self.firstname = firstname
        self.surname = surname
        self.age = int(age)
        self.nationID = int(nationID)
        self.clubID = int(clubID)

        self.playerShortlist = []

        self.preferred_formation = "4231"
        self.preferred_playing_style = "Route One"

    def getPreferredFormation(self):
        return self.preferred_formation

    def getPreferredPlayingStyle(self):
        return self.preferred_playing_style

    def getName(self):
        return self.firstname + " " + self.surname

    def getSurname(self):
        return self.surname

    def getAge(self):
        return self.age

    def incrementAge(self):
        self.age = self.age + 1

    def getNationID(self):
        return self.nationality

    def setNationID(self, nation):
        self.nationality = nation

    def getClubID(self):
        return self.clubID

    def setClubID(self, newID):
        self.clubID = newID

    def getID(self):
        return self.id

    def getShortlist(self):
        return self.playerShortlist

    def shortlistAdd(self, player):
        self.playerShortlist.append(player)

    def shortlistRemove(self, player):
        self.playerShortlist.remove(player)
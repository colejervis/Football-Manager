class Stadium:
    def __init__(self, stadium_id, name, club_id, capacity, opened_date, city):
        self.id = int(stadium_id)
        self.name = name
        self.clubID = int(club_id)
        self.capacity = capacity
        self.opened_date = opened_date
        self.city = city

    def getID(self):
        return self.id

    def getClubID(self):
        return self.clubID

    def getName(self):
        return self.name

    def getCapacity(self):
        return self.capacity

    def getOpenedDate(self):
        return self.opened_date

    def getCity(self):
        return self.city
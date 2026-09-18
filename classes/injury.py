import random
from mathematical_models import random_choices

class Injury:
    football_injuries = [
        ["Knock", 1, 3, 0.25],
        ["Bruise", 1, 7, 0.18],
        ["Muscle fatigue", 1, 4, 0.15],
        ["Tight hamstring", 2, 7, 0.10],
        ["Tight calf", 2, 7, 0.08],
        ["Minor muscle strain", 3, 10, 0.08],
        ["Hamstring strain", 14, 84, 0.07],
        ["Ankle sprain", 7, 84, 0.06],
        ["Groin strain", 14, 84, 0.05],
        ["Quadriceps strain", 7, 56, 0.04],
        ["Calf strain", 14, 70, 0.04],
        ["Hip flexor strain", 14, 56, 0.03],
        ["Knee sprain", 14, 84, 0.03],
        ["MCL injury", 14, 84, 0.02],
        ["Patellar tendinitis", 14, 168, 0.02],
        ["Achilles tendinitis", 14, 168, 0.02],
        ["Shin splints", 14, 84, 0.02],
        ["Concussion", 7, 56, 0.02],
        ["Back injury", 14, 168, 0.02],
        ["Illness", 1, 14, 0.06],
        ["Meniscus tear", 28, 168, 0.01],
        ["Stress fracture", 42, 168, 0.01],
        ["Fracture", 42, 182, 0.01],
        ["Dislocated shoulder", 28, 112, 0.005],
        ["Hernia", 28, 84, 0.005],
        ["PCL injury", 28, 252, 0.003],
        ["High ankle sprain", 42, 112, 0.003],
        ["Achilles rupture", 168, 365, 0.002],
        ["ACL tear", 252, 365, 0.002],
    ]

    def __init__(self, playerID, fixtureSustainedIn):
        self.playerID = playerID

        # SELECTS INJURY

        injuryType = random_choices(Injury.football_injuries, 3)

        self.name = injuryType[0]
        self.min_days = injuryType[1]
        self.max_days = injuryType[2]

        self.fixtureSustainedIn = fixtureSustainedIn

        self.length = random.randint(self.min_days, self.max_days)
        self.timeElapsed = 0

    def getFixtureSustainedIn(self):
        return self.fixtureSustainedIn

    def getName(self):
        return self.name

    def getTimeElapsed(self):
        return self.timeElapsed

    def getLength(self):
        return self.length

    def incrementTimeElapsed(self):
        self.timeElapsed += 1

    def getMinMaxDays(self):
        return self.min_days, self.max_days

    def getMinMaxDaysRemaining(self):
        return self.min_days - self.timeElapsed, self.max_days - self.timeElapsed
class Date:

    def __init__(self):
        self.daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self.day = 0
        self.month = 0
        self.year = 0
        self.yesterdayDate = None

    def setDate(self, day, month, year):

        if not self.validDateChecker(day, month, year):
            raise ValueError("Invalid date")

        self.day = day
        self.month = month
        self.year = year

    def getDate(self):
        return self.day, self.month, self.year

    def getYear(self):
        return self.year

    def isLeapYear(self, year=None):
        if year is None:
            year = self.year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_february(self):
        if self.isLeapYear() == True:
            return 29
        else:
            return 28

    # USED IN HOLIDAY MENU TO CHECK IF PROPOSED DATE IS VALID
    def validDateChecker(self, day, month, year):
        if month < 1 or month > 12:
            return False

        if month == 2:
            if self.isLeapYear(year):
                max_days = 29
            else:
                max_days = 28
        else:
            max_days = self.daysInMonth[month - 1]

        return 1 <= day <= max_days

    def isInFutureChecker(self, day, month, year):

        if year > self.year:
            return True
        elif year < self.year:
            return False
        else:
            if month > self.month:
                return True
            elif month < self.month:
                return False
            else:
                if day > self.day:
                    return True
                elif day < self.day:
                    return False
                elif day == self.day:
                    return False


    def advance(self):
        self.yesterdayDate = (self.day, self.month, self.year)

        if self.month == 2:
            self.daysInMonth[1] = 29 if self.isLeapYear() else 28

        if self.day == self.daysInMonth[self.month - 1] and self.month == 12:
            self.month = 1
            self.day = 1
            self.year += 1

        elif self.day == self.daysInMonth[self.month - 1] and self.month != 12:
            self.month += 1
            self.day = 1
        else:
            self.day += 1


    def getWeekday(self):

        """
        https://en.wikipedia.org/wiki/Zeller%27s_congruence
        Zeller's Congruence - can calculate any day of the week for any Julian or Gregorian calendar date.
        """

        q = self.day
        m = self.month
        y = self.year

        if m == 1 or m == 2:
            m += 12
            y -= 1

        K = y % 100
        J = y // 100

        h = (q + (13 * (m + 1)) // 5 + K + (K // 4) + (J // 4) + (5 * J)) % 7

        # Map result to weekday names
        days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return days[h]

    def getYesterdayDate(self):
        return self.yesterdayDate
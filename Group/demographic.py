class demo():
    behaviorDict = {}
    behaviorDict_wk = {}

    def getAction(self, time):
        # Gegeven een tijd geef terug wat deze agent wil doen en hoe belangrijk hij dit vind
        if time.weekday() < 5:

            return self.behaviorDict.get(time.hour)
        else:
            return self.behaviorDict_wk.get(time.hour)

class Child(demo):
    '''leeftijd: 0-16'''
    behaviorDict = {9: (10, "School"),
                    15: (5, "Park"),
                    17: (10, "House")}

    behaviorDict_wk = {
                    9: (10, "House"),
                    10: (5, "Park"),
                    15: (5, "Shop"),
                    17: (10, "House")}


class Student(demo):
    '''leeftijd: 16-25'''
    behaviorDict = {9: (10, "University"),
                    15: (5, "Park"),
                    18: (5, "Shop"),
                    20: (10, "House")}

    behaviorDict_wk = {
                    9: (10, "House"),
                    11: (5, "Park"),
                    18: (5, "Shop"),
                    20: (10, "House")}

class Adult(demo):
    '''leeftijd: 25-44'''
    behaviorDict = {9: (10, "Work"),
                    17: (5, "Shop"),
                    20: (10, "House")}

    behaviorDict_wk = {
                    9: (10, "House"),
                    13: (5, "Park"),
                    16: (5, "Shop"),
                    22: (10, "House")}


class Elderly(demo):
    '''leeftijd: 65+'''
    behaviorDict = {9: (10, "House"),
                    13: (5, "Park"),
                    16: (5, "Shop"),
                    19: (10, "House")}

    behaviorDict_wk = {
                    9: (10, "House"),
                    13: (5, "Park"),
                    16: (5, "Shop"),
                    19: (10, "House")}

class Infected(demo):
    behaviorDict = {0: (10, "House")}
    behaviorDict_wk = {0: (10, "House")}

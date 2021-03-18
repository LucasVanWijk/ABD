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
    behaviorDict = {9: (100, "School"),
                    15: (50, "Park"),
                    17: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    10: (50, "Park"),
                    15: (50, "Shop"),
                    17: (100, "House")}


class Student(demo):
    '''leeftijd: 16-25'''
    behaviorDict = {9: (100, "University"),
                    15: (50, "Park"),
                    18: (50, "Shop"),
                    20: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    11: (50, "Park"),
                    18: (50, "Shop"),
                    20: (100, "House")}

class Adult(demo):
    '''leeftijd: 25-44'''
    behaviorDict = {9: (100, "Work"),
                    17: (50, "Shop"),
                    20: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    13: (50, "Park"),
                    16: (50, "Shop"),
                    22: (100, "House")}


class Elderly(demo):
    '''leeftijd: 65+'''
    behaviorDict = {9: (100, "House"),
                    13: (50, "Park"),
                    16: (50, "Shop"),
                    19: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    13: (50, "Park"),
                    16: (50, "Shop"),
                    19: (100, "House")}

class Infected(demo):
    behaviorDict = {0: (100, "House")}
    behaviorDict_wk = {0: (100, "House")}

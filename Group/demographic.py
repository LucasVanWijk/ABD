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
                    15: (70, "Park"),
                    17: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    10: (70, "Park"),
                    15: (70, "Shop"),
                    17: (100, "House")}


class Student(demo):
    '''leeftijd: 16-25'''
    behaviorDict = {9: (100, "University"),
                    15: (70, "Park"),
                    18: (70, "Shop"),
                    20: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    11: (70, "Park"),
                    18: (70, "Shop"),
                    20: (100, "House")}

class Adult(demo):
    '''leeftijd: 25-44'''
    behaviorDict = {9: (100, "Work"),
                    17: (70, "Shop"),
                    20: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    13: (70, "Park"),
                    16: (70, "Shop"),
                    22: (100, "House")}


class Elderly(demo):
    '''leeftijd: 65+'''
    behaviorDict = {9: (100, "House"),
                    13: (70, "Park"),
                    16: (70, "Shop"),
                    19: (100, "House")}

    behaviorDict_wk = {
                    9: (100, "House"),
                    13: (70, "Park"),
                    16: (70, "Shop"),
                    19: (100, "House")}

class Infected(demo):
    behaviorDict = {0: (100, "House")}
    behaviorDict_wk = {0: (100, "House")}

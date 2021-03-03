class demo():
    behaviorDict = {}

    def getAction(self, time):
        # Gegeven een tijd geef terug wat deze agent wil doen en hoe belangrijk hij dit vind
        return self.behaviorDict.get(time)


class kind(demo):
    '''leeftijd: 0-16'''
    behaviorDict = {9: (100, "School"),
                    15: (70, "Park"),
                    17: (100, "Home")}

    behaviorDict_wk = {
                    9: (100, "Home"),
                    10: (70, "Park"),
                    15: (70, "Shop"),
                    17: (100, "Home")}


class student(demo):
    '''leeftijd: 16-25'''
    behaviorDict = {9: (100, "School"),
                    15: (70, "Park"),
                    18: (70, "Shops"),
                    20: (100, "Home")}

    behaviorDict_wk = {
                    9: (100, "Home"),
                    11: (70, "Park"),
                    18: (70, "Shops"),
                    20: (100, "Home")}

class volwassen_onder_45(demo):
    '''leeftijd: 25-44'''
    behaviorDict = {9: (100, "Work"),
                    17: (70, "Shops"),
                    20: (100, "Home")}

    behaviorDict_wk = {
                    9: (100, "Home"),
                    13: (70, "Park"),
                    16: (70, "Shops"),
                    22: (100, "Home")}

class volwassen_onder_45(demo):
    '''leeftijd: 45-65'''
    behaviorDict = {9: (100, "Home"),
                    17: (70, "Shops"),
                    20: (100, "Home")}

    behaviorDict_wk = {
                    9: (100, "Home"),
                    13: (70, "Park"),
                    16: (70, "Shops"),
                    20: (100, "Home")}

class senioren(demo):
    '''leeftijd: 65+'''
    behaviorDict = {9: (100, "Home"),
                    13: (70, "Park"),
                    16: (70, "Shops"),
                    19: (100, "Home")}

    behaviorDict_wk = {
                    9: (100, "Home"),
                    13: (70, "Park"),
                    16: (70, "Shops"),
                    19: (100, "Home")}

class geinfecteerd(demo):
    behaviorDict = {0: (100, "Home")}
    behaviorDict_wk = {0: (100, "Home")}

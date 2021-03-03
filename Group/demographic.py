class demo():
    behaviorDict = {}

    def getAction(self, time):
        # Gegeven een tijd geef terug wat deze agent wil doen en hoe belangrijk hij dit vind
        return self.behaviorDict.get(time)

class student(demo):
    behaviorDict = {"9:00": (100, "School"),
                    "15:00": (80, "Recreation")}

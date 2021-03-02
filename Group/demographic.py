class demo():
    behaviorDict = {}

    def getAction(self, time):
        return self.behaviorDict.get(time)

class student(demo):
    behaviorDict = {"9:00": (True, "School"),
                    "15:00": (False, "Recreation")}
